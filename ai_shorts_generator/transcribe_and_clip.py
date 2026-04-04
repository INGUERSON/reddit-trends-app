import os
import json
import math
from openai import OpenAI
from moviepy.editor import AudioFileClip
from dotenv import load_dotenv
from secure_vault import decrypt_value

load_dotenv()

encrypted_key = os.getenv("OPENAI_API_KEY")
api_key = decrypt_value(encrypted_key) if encrypted_key and encrypted_key.startswith("gAAAA") else encrypted_key

client = OpenAI(api_key=api_key)

def split_audio(audio_path, chunk_length_sec=600):
      audio_clip = AudioFileClip(audio_path)
      duration = audio_clip.duration
      chunks = []
      for start_time in range(0, math.ceil(duration), chunk_length_sec):
                end_time = min(start_time + chunk_length_sec, duration)
                out_file = f"{audio_path}_chunk_{start_time}.mp3"
                print(f"Extraindo chunk do audio ({start_time}s - {end_time}s)...")
                new_clip = audio_clip.subclip(start_time, end_time)
                new_clip.write_audiofile(out_file, logger=None)
                chunks.append({"path": out_file, "offset": start_time})
            audio_clip.close()
    return chunks

def transcribe_audio_with_words(audio_path):
      print(f"Iniciando Transcricao via Whisper API: {audio_path}")
    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    chunks = []
    if file_size_mb > 24:
              print(f"Arquivo de audio grande ({file_size_mb:.1f}MB). Dividindo em partes...")
              chunks = split_audio(audio_path)
else:
        chunks = [{"path": audio_path, "offset": 0}]

    full_text = ""
    words_data = []

    for chunk in chunks:
              print(f"Enviando para a OpenAI (offset {chunk['offset']}s)...")
              try:
                            with open(chunk['path'], "rb") as audio_file:
                                              transcript = client.audio.transcriptions.create(
                                                                    model="whisper-1",
                                                                    file=audio_file,
                                                                    response_format="verbose_json",
                                                                    timestamp_granularities=["word"]
                                              )
                                          full_text += transcript.text + " "
                            if hasattr(transcript, 'words') and transcript.words:
                                              for w in transcript.words:
                                                                    if not hasattr(w, 'word'):
                                                                                              continue
                                                                                          words_data.append({
                                                                        "word": w.word,
                                                                        "start": w.start + chunk['offset'],
                                                                        "end": w.end + chunk['offset']
                                                                    })
                                                                print(f"DEBUG: Found {len(transcript.words)} words in this chunk.")
              except Exception as e:
                            print(f"Erro na transcricao do chunk: {e}")

          if file_size_mb > 24:
                    for c in chunks:
                                  try:
                                                    os.remove(c['path'])
                                                except:
                pass

    print("Transcricao e alinhamento concluidos!")
    return full_text, words_data

def identify_viral_clips(transcript_text, num_clips=3):
      print("Analisando roteiro com GPT-4o para encontrar momentos virais...")

    system_prompt = (
              "Voce e um Produtor de Videos Curtos Viral especialista em retencao para TikTok e Instagram Reels. "
              "Sua missao e transformar a transcricao abaixo em CLIPES DE ALTO IMPACTO.\n\n"
              "REGRAS DE ANALISE:\n"
              "1. IDENTIFICACAO DE DESTAQUES: Busque momentos impactantes, controversos, inspiradores ou educativos.\n"
              "2. GANCHO INICIAL (0-3 segundos): O clipe deve comecar IMEDIATAMENTE com uma frase forte.\n"
              "3. DURACAO: O clipe deve ter entre 15 a 60 segundos de duracao.\n"
              "4. FLOW: O corte deve ser um segmento continuo e coerente.\n\n"
              "REGRAS DE SAIDA:\n"
              "1. Retorne EXATAMENTE e APENAS no formato JSON.\n"  "2. Campos: 'title' (Clickbait), 'start_quote' (primeiras 5 palavras EXATAS), 'end_quote' (ultimas 5 palavras EXATAS).\n"
              "3. Selecione os " + str(num_clips) + " melhores momentos."
    )

    try:
              response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                              {"role": "system", "content": system_prompt},
                                              {"role": "user", "content": transcript_text[-90000:]}
                            ],
                            temperature=0.7,
                            response_format={"type": "json_object"}
              )

        result_str = response.choices[0].message.content
  

        print("RAW GPT OUTPUT:", result_str)

        if result_str.startswith("```json"):
                      result_str = result_str[7:]
                  if result_str.startswith("```"):
                                result_str = result_str[3:]
                            if result_str.endswith("```"):
                                          result_str = result_str[:-3]

        data = json.loads(result_str.strip())
        clips = []
        if isinstance(data, list):
                      clips = data
elif isinstance(data, dict):
            for k, v in data.items():
                              if isinstance(v, list):
                                                    clips.extend(v)
elif isinstance(v, dict) and "start_quote" in v:
                    clips.append(v)

        if not clips and isinstance(data, dict) and 'clips' in data:
                      clips = data['clips']

        print(f"A Inteligencia Artificial marcou {len(clips)} cortes em potencial.")
        return clips
except Exception as e:
        print(f"Erro ao analisar trechos com GPT: {e}")
        return []

def align_clip_timestamps(clips, words_data):
      final_clips = []
    full_text = ""
    char_to_word_idx = []

    for i, w in enumerate(words_data):
              clean_word = w['word'].lower().strip()
              start_char = len(full_text)
              full_text += clean_word + " "
              for _ in range(len(full_text) - start_char):
                            char_to_word_idx.append(i)

          for clip in clips:
                    start_q = clip.get('start_quote', '').lower().strip()
                    end_q = clip.get('end_quote', '').lower().strip()
                    start_q = start_q.replace('.', '').replace(',', '').replace('?', '').replace('!', '')
                    end_q = end_q.replace('.', '').replace(',', '').replace('?', '').replace('!', '')

        start_idx = full_text.find(start_q)
        end_idx = full_text.rfind(end_q)

        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
                      first_word_idx = char_to_word_idx[start_idx]
                      last_char_idx = min(end_idx + len(end_q) - 1, len(char_to_word_idx) - 1)
                      last_word_idx = char_to_word_idx[last_char_idx]
                      start_time = words_data[first_word_idx]['start']
                      end_time = words_data[last_word_idx]['end']

            if end_time > start_time:
                              if (end_time - start_time) > 90:
                                                    print(f"Duracao exagerada detectada ({(end_time - start_time):.1f}s). Cortando para 90s...")
                                                    end_time = start_time + 90.0
                                                clip['start_time'] = start_time
                clip['end_time'] = end_time
                final_clips.append(clip)

    if not final_clips and words_data:
              print("Aviso: As palavras do GPT nao sincronizaram. Gerando clipes seguros genericos...")
        total_time = words_data[-1]['end']
        mid_time = total_time / 2
        safe_clip = {
                      'title': "Momento Polemico",
                      'start_time': max(0, mid_time - 15),
                      'end_time': min(total_time, mid_time + 15)
        }
        final_clips.append(safe_clip)

    return final_clips
