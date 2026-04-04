import os
import sys

from download_video import download_youtube_video
from transcribe_and_clip import transcribe_audio_with_words, identify_viral_clips, align_clip_timestamps
from video_editor import edit_and_render_clip


def main(url=None):
    print("AI SHORTS GENERATOR")
    print("="*40)

    if not url:
        if len(sys.argv) > 1:
            url = sys.argv[1].strip()
        else:
            url = input("Cole o link do YouTube: ").strip()

    if not url:
        print("Nenhum link fornecido.")
        return []

    video_path, audio_path = download_youtube_video(url, output_path="downloads")
    if not video_path or not audio_path:
        print("Falha no download.")
        return []

    transcript_text, words_data = transcribe_audio_with_words(audio_path)
    if not transcript_text:
        print("Falha na transcricao.")
        return []

    print(f"Transcricao gerou {len(words_data)} palavras.")

    raw_clips = identify_viral_clips(transcript_text, num_clips=3)
    if not raw_clips:
        print("A IA nao encontrou trechos bons.")
        return []

    print("Alinhando tempos de corte...")
    final_clips = align_clip_timestamps(raw_clips, words_data)

    if not final_clips:
        print("Falha ao alinhar palavras-chave.")
        return []

    print(f"Validados {len(final_clips)} trechos para edicao!")

    if not os.path.exists("output"):
        os.makedirs("output")

    generated_videos = []
    for i, clip in enumerate(final_clips, 1):
        print(f"CLIPE {i}/{len(final_clips)}: {clip.get('title', 'Sem_Nome')}")
        print(f"Duracao: {clip['end_time'] - clip['start_time']:.1f}s")

        safe_title = str(clip.get('title', f'Clip_0{i}')).replace(":", "").replace(" ", "_").replace("/", "")
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
            print(f"Salvo: {output_file}")
            generated_videos.append(output_file)

    print("PROCESSO ENCERRADO")
    return generated_videos


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY nao encontrada!")
        sys.exit(1)
    main()
