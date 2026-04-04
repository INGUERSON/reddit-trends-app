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
    """
    OpenAI Whisper limits files to 25MB. This function splits a large MP3 into smaller 10-minute chunks.
    Returns a list of temporary audio paths.
    """
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    chunks = []

    for start_time in range(0, math.ceil(duration), chunk_length_sec):
        end_time = min(start_time + chunk_length_sec, duration)
        out_file = f"{audio_path}_chunk_{start_time}.mp3"
        print(f"⏳ Extraindo chunk do áudio ({start_time}s - {end_time}s)...")
        new_clip = audio_clip.subclip(start_time, end_time)
        new_clip.write_audiofile(out_file, logger=None)
        chunks.append({"path": out_file, "offset": start_time})

    audio_clip.close()
    return chunks

def transcribe_audio_with_words(audio_path):
    print(f"🎙️ Iniciando Transcrição via Whisper API: {audio_path}")

    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    chunks = []

    if file_size_mb > 24:
        print(f"⚠️ Arquivo de áudio grande ({file_size_mb:.1f}MB). Dividindo em partes...")
        chunks = split_audio(audio_path)
    else:
        chunks = [{"path": audio_path, "offset": 0}]

    full_text = ""
    words_data = []

    for chunk in chunks:
        print(f"🗣️ Enviando para a OpenAI (offset {chunk['offset']}s)...")
        try:
            with open(chunk['path'], "rb") as audio_file:
                # To get word timestamps, we must use verbose_json and timestamp_granularities="word"
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )

            full_text += transcript.text + " "

            # Adjust word timestamps by adding the chunk offset
            if hasattr(transcript, 'words') and transcript.words:
                for w in transcript.words:
                    if not hasattr(w, 'word'): continue
                    words_data.append({
                        "word": w.word,
                        "start": w.start + chunk['offset'],
                        "end": w.end + chunk['offset']
                    })
                print(f"DEBUG: Found {len(transcript.words)} words in this chunk.")

        except Exception as e:
            print(f"❌ Erro na transcrição do chunk: {e}")

    # Cleanup temp chunks
    if file_size_mb > 24:
        for c in chunks:
            try:
                os.remove(c['path'])
            except:
                pass

    print("✅ Transcrição e alinhamento concluídos!")
    return full_text, words_data

def identify_viral_clips(transcript_text, num_clips=3):
    print("🧠 Analisando roteiro com GPT-4o para encontrar momentos virais...")

    system_prompt = (
        "Você é um Produtor de Vídeos Curtos Viral especialista em retenção para TikTok e Instagram Reels. "
        "Sua missão é transformar a transcrição abaixo em CLIPES DE ALTO IMPACTO.\n\n"
        "REGRAS DE ANÁLISE:\n"
        "1. IDENTIFICAÇÃO DE DESTAQUES: Busque momentos impactantes, controversos, inspiradores ou educativos. O corte deve conter uma 'pepita de ouro'.\n"
        "2. GANCHO INICIAL (0-3 segundos): O clipe deve começar IMEDIATAMENTE com uma frase forte ou pico emocional. Sem introduções lentas.\n"
        "3. DURAÇÃO: O clipe deve ter entre 15 a 60 segundos de duração.\n"
        "4. FLOW: O corte deve ser um segmento contínuo e coerente que faça sentido sozinho.\n\n"
        "REGRAS DE SAÍDA:\n"
        "1. Retorne EXATAMENTE e APENAS no formato JSON.\n"
        "2. Campos: 'title' (Clickbait), 'start_quote' (primeiras 5 palavras EXATAS), 'end_quote' (últimas 5 palavras EXATAS).\n"
        "3. Selecione os " + str(num_clips) + " melhores momentos."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript_text[-90000:]}  # Limit text size to OpenAI limits roughly
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        result_str = response.choices[0].message.content
        print("RAW GPT OUTPUT:", result_str)

        # Clean markdown if present
        if result_str.startswith("```json"):
            result_str = result_str[7:]
        if result_str.startswith("```"):
            result_str = result_str[3:]
        if result_str.endswith("```"):
            result_str = result_str[:-3]

        data = json.loads(result_str.strip())

        # Depending on how the AI packages it, extract the list
        clips = []
        if isinstance(data, list):
            clips = data
        elif isinstance(data, dict):
            # It might return {"clips": [...]} or {"1": {...}, "2": {...}}
            for k, v in data.items():
                if isinstance(v, list):
                    clips.extend(v)
                elif isinstance(v, dict) and "start_quote" in v:
                    clips.append(v)

        # Fallback if wrapping is weird
        if not clips and isinstance(data, dict) and 'clips' in data:
            clips = data['clips']

        print(f"✅ A Inteligência Artificial marcou {len(clips)} cortes em potencial.")
        return clips
    except Exception as e:
        print(f"❌ Erro ao analisar trechos com GPT: {e}")
        return []

def align_clip_timestamps(clips, words_data):
    """
    Since GPT outputs start/end quotes, we must find their exact timestamp seconds 
    by reading the word array generated by Whisper.
    Uses a robust substring search across the transcript.
    """
    final_clips = []

    # Create a full string tracking character index to physical words
    full_text = ""
    char_to_word_idx = []

    for i, w in enumerate(words_data):
        clean_word = w['word'].lower().strip()
        start_char = len(full_text)
        full_text += clean_word + " "

        # Map every character in this word + space back to the word index
        for _ in range(len(full_text) - start_char):
            char_to_word_idx.append(i)

    for clip in clips:
        start_q = clip.get('start_quote', '').lower().strip()
        end_q = clip.get('end_quote', '').lower().strip()

        # Remove strict punctuation to help matching
        start_q = start_q.replace('.', '').replace(',', '').replace('?', '').replace('!', '')
        end_q = end_q.replace('.', '').replace(',', '').replace('?', '').replace('!', '')

        start_idx = full_text.find(start_q)
        end_idx = full_text.rfind(end_q)

        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
            # Safely grab word bounds avoiding out of range
            first_word_idx = char_to_word_idx[start_idx]

            # The end_q index points to the start of the end quote. Add length to get the final word.
            last_char_idx = min(end_idx + len(end_q) - 1, len(char_to_word_idx) - 1)
            last_word_idx = char_to_word_idx[last_char_idx]

            start_time = words_data[first_word_idx]['start']
            end_time = words_data[last_word_idx]['end']

            if end_time > start_time:
                # Prevenção Crítica de Memória: Garantir que o clipe nunca ultrapasse 90 segundos
                if (end_time - start_time) > 90:
                    print(f"⚠️ Duração exagerada detectada ({(end_time - start_time):.1f}s). Cortando para 90s...")
                    end_time = start_time + 90.0

                clip['start_time'] = start_time
                clip['end_time'] = end_time
                final_clips.append(clip)

    # Fallback Mechanism: If AI fails to align completely, safely return a simple clip
    if not final_clips and words_data:
        print("⚠️ Aviso: As palavras do GPT não sincronizaram. Gerando clipes seguros genéricos...")
        total_time = words_data[-1]['end']

        # Safe clip 1: Middle of the video, 30s long
        mid_time = total_time / 2
        safe_clip = {
            'title': "Momento Polêmico",
            'start_time': max(0, mid_time - 15),
            'end_time': min(total_time, mid_time + 15)
        }
        final_clips.append(safe_clip)

    return final_clips
