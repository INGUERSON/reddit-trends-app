import os
import sys

# Force UTF-8 encoding for Windows terminals to avoid emoji crashes
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from download_video import download_youtube_audio, download_youtube_video_720p
from transcribe_and_clip import transcribe_audio_with_words, identify_viral_clips, align_clip_timestamps
from video_editor import edit_and_render_clip

def main(url=None):
    print("========================================")
    print("🎬 AI SHORTS GENERATOR (Vídeos Curtos Virais)")
    print("========================================\n")
    
    # 1. Obter link do usuário
    if not url:
        if len(sys.argv) > 1:
            url = sys.argv[1].strip()
        else:
            url = input("🔗 Cole o link do YouTube (ex: Podcast curto): ").strip()
            
    if not url:
        print("❌ Nenhum link fornecido. Encerrando.")
        return []
        
    # 2. Download Turbo Áudio (Muito Rápido)
    audio_path, video_id = download_youtube_audio(url, output_path="downloads")
    if not audio_path:
        print("❌ Falha no download do áudio.")
        return []
        
    # 3. Transcrever e identificar
    transcript_text, words_data = transcribe_audio_with_words(audio_path)
    if not transcript_text:
        print("❌ Falha na transcrição.")
        return []
        
    # 4. Pedir pro GPT-4o caçar os melhores momentos
    raw_clips = identify_viral_clips(transcript_text, num_clips=3)
    if not raw_clips:
        print("❌ A IA não encontrou trechos bons o suficiente.")
        return []
        
    # 5. Alinhar timestamps
    print("⏱️ Alinhando os tempos de corte exatos com o vídeo...")
    final_clips = align_clip_timestamps(raw_clips, words_data)
    
    if not final_clips:
        print("❌ Falha ao alinhar as palavras-chave no roteiro.")
        return []
        
    # 🚀 AGORA BAIXAMOS O VÍDEO (Depois que sabemos que há clips)
    # Baixamos em 720p para velocidade e compatibilidade
    video_path = download_youtube_video_720p(url, video_id, output_path="downloads")
    if not video_path:
        print("❌ Falha no download do vídeo 720p.")
        return []

    print(f"🎬 Foram validados {len(final_clips)} trechos exatos para edição!")
    
    # 6. Renderização Profissional
    if not os.path.exists("output"):
        os.makedirs("output")
        
    generated_videos = []
    for i, clip in enumerate(final_clips, 1):
        print("\n" + "-"*40)
        print(f"🎥 PREPARANDO CLIPE {i}/{len(final_clips)}: {clip.get('title', 'Sem_Nome')}")
        print(f"⏰ Duração estimada: {clip['end_time'] - clip['start_time']:.1f} segundos")
        
        safe_title = str(clip.get('title', f'Clip_0{i}')).replace(":", "").replace(" ", "_").replace("/", "").replace("\\", "")
        safe_title = safe_title[:30]
        output_file = f"output/{safe_title}.mp4"
        
        # 🎨 RENDERIZAÇÃO PROFISSIONAL (Zooms, Captions, Cores)
        success_edit = edit_and_render_clip(
            video_path=video_path,
            audio_path=audio_path,
            start_time=clip['start_time'],
            end_time=clip['end_time'],
            words_data=words_data,
            output_filename=output_file,
            is_already_cut=False # Avisa o editor que ele deve recortar
        )
        
        if success_edit:
            print(f"✅ Finalizado e salvo na pasta output: {output_file}")
            generated_videos.append(output_file)
            
    print("\n✅✅✅ PROCESSO DE CRIAÇÃO ENCERRADO ✅✅✅")
    return generated_videos

if __name__ == "__main__":
    main()
