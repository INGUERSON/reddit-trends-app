import os
import sys

# Force UTF-8 encoding for Windows terminals to avoid emoji crashes
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from download_video import download_youtube_video
from transcribe_and_clip import transcribe_audio_with_words, identify_viral_clips, align_clip_timestamps
from video_editor import edit_and_render_clip

def main(url=None):
    print("========================================")
    print("🎬 AI SHORTS GENERATOR (Vídeos Curtos Virais)")
    print("========================================\n")
    
    # 1. Obter link do usuário (ou por argumento ou por input)
    if not url:
        if len(sys.argv) > 1:
            url = sys.argv[1].strip()
            print(f"🔗 Link recebido por argumento: {url}")
        else:
            url = input("🔗 Cole o link do YouTube (ex: Podcast curto): ").strip()
            
    if not url:
        print("❌ Nenhum link fornecido. Encerrando.")
        return []
        
    # 2. Download (Vídeo e Áudio separado)
    video_path, audio_path = download_youtube_video(url, output_path="downloads")
    if not video_path or not audio_path:
        print("❌ Falha no download. Encerrando.")
        return []
        
    # 3. Transcrever e pegar os timestamps de cada palavra
    transcript_text, words_data = transcribe_audio_with_words(audio_path)
    if not transcript_text:
        print("❌ Falha na transcrição. Encerrando.")
        return []
        
    print(f"\n📝 Transcrição gerou {len(words_data)} palavras.")
    
    # 4. Pedir pro GPT-4o caçar os melhores momentos
    raw_clips = identify_viral_clips(transcript_text, num_clips=3)
    if not raw_clips:
        print("❌ A IA não encontrou trechos bons o suficiente. Encerrando.")
        return []
        
    # 5. Alinhar o texto gerado pelo GPT com o timestamp físico exato do Whisper
    print("⏱️ Alinhando os tempos de corte exatos com o vídeo...")
    final_clips = align_clip_timestamps(raw_clips, words_data)
    
    if not final_clips:
        print("❌ Falha ao alinhar as palavras-chave no roteiro. (Pode ser alucinação do LLM)")
        return []
        
    print(f"🎬 Foram validados {len(final_clips)} trechos exatos para edição!")
    
    # 6. Para cada trecho, rodar o MoviePy e renderizar
    if not os.path.exists("output"):
        os.makedirs("output")
        
    generated_videos = []
    for i, clip in enumerate(final_clips, 1):
        print("\n" + "-"*40)
        print(f"🎥 PREPARANDO CLIPE {i}/{len(final_clips)}: {clip.get('title', 'Sem_Nome')}")
        print(f"⏰ Duração estimada: {clip['end_time'] - clip['start_time']:.1f} segundos")
        
        safe_title = str(clip.get('title', f'Clip_0{i}')).replace(":", "").replace(" ", "_").replace("/", "").replace("\\", "")
        # Shorten extreme long titles
        safe_title = safe_title[:30]
        output_file = f"output/{safe_title}.mp4"
        
        success = edit_and_render_clip(
            video_path=video_path,
            audio_path=audio_path,
            start_time=clip['start_time'],
            end_time=clip['end_time'],
            words_data=words_data,
            output_filename=output_file
        )
        
        if success:
            print(f"✅ Finalizado e salvo na pasta output: {output_file}")
            generated_videos.append(output_file)
            
    print("\n✅✅✅ PROCESSO DE CRIAÇÃO ENCERRADO ✅✅✅")
    print("👉 Verifique a pasta 'output' para postar seus novos vídeos verticais nas redes sociais.")
    
    return generated_videos

if __name__ == "__main__":
    # Teste de API Key
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sua_chave_aqui":
        print("⚠️ ALERTA: OPENAI_API_KEY não foi encontrada ou está vazia no seu arquivo .env!")
        print("Por favor, preencha o arquivo .env primeiro (usando a mesma da inteligência anterior).")
        sys.exit(1)
        
    main()
