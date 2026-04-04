import os
import sys

from download_video import download_dual_source, download_youtube_video
from transcribe_and_clip import transcribe_audio_with_words, identify_viral_clips, align_clip_timestamps
from video_editor import edit_and_render_clip


def main(url=None):
    print("========================================")
    print("AI SHORTS GENERATOR (Videos Curtos Virais)")
    print("========================================\n")

    # url pode ser string ou dict {"video_url": ..., "audio_url": ...}
    if not url:
        if len(sys.argv) > 1:
            url = sys.argv[1].strip()
            print(f"Link recebido por argumento: {url}")
        else:
            url = input("Cole o link do YouTube (ex: Podcast curto): ").strip()

    if not url:
        print("Nenhum link fornecido. Encerrando.")
        return []

    # Determina se e dual-fonte ou URL simples
    if isinstance(url, dict):
        video_url = url.get("video_url", "")
        audio_url = url.get("audio_url", video_url)
        print(f"Video source: {video_url[:60]}...")
        print(f"Audio source: {audio_url[:60]}...")
        video_path, audio_path = download_dual_source(video_url, audio_url, output_path="downloads")
    else:
        # URL simples - tenta YouTube completo
        video_path, audio_path = download_youtube_video(url, output_path="downloads")

    if not video_path or not audio_path:
        print("Falha no download. Encerrando.")
        return []

    # Transcrever audio com Whisper
    transcript_text, words_data = transcribe_audio_with_words(audio_path)
    if not transcript_text:
        print("Falha na transcricao. Encerrando.")
        return []

    print(f"\nTranscricao gerou {len(words_data)} palavras.")

    # GPT-4o identifica momentos virais
    raw_clips = identify_viral_clips(transcript_text, num_clips=3)
    if not raw_clips:
        print("A IA nao encontrou trechos bons o suficiente. Encerrando.")
        return []

    # Alinha timestamps exatos
    print("Alinhando os tempos de corte exatos com o video...")
    final_clips = align_clip_timestamps(raw_clips, words_data)

    if not final_clips:
        print("Falha ao alinhar as palavras-chave no roteiro.")
        return []

    print(f"Foram validados {len(final_clips)} trechos exatos para edicao!")

    os.makedirs("output", exist_ok=True)

    generated_videos = []
    for i, clip in enumerate(final_clips, 1):
        print("\n" + "-"*40)
        print(f"PREPARANDO CLIPE {i}/{len(final_clips)}: {clip.get('title', 'Sem_Nome')}")
        print(f"Duracao estimada: {clip['end_time'] - clip['start_time']:.1f} segundos")

        safe_title = str(clip.get('title', f'Clip_0{i}')).replace(":", "").replace(" ", "_").replace("/", "").replace("\\", "")
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
            print(f"Finalizado e salvo: {output_file}")
            generated_videos.append(output_file)

    print("\nPROCESSO DE CRIACAO ENCERRADO")
    print(f"Total de clips gerados: {len(generated_videos)}")

    return generated_videos


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sua_chave_aqui":
        print("ALERTA: OPENAI_API_KEY nao foi encontrada ou esta vazia no seu arquivo .env!")
        sys.exit(1)

    main()
