import os
import yt_dlp

def download_youtube_video(url, output_path="downloads"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    try:
        print(f"Conectando ao YouTube via YT-DLP: {url}")
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(id)s_vid.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info['id']
            video_filename = os.path.join(output_path, f"{video_id}_vid.mp4")

        print(f"Extraindo audio de alta fidelidade para transcricao...")
        audio_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, f"{video_id}_audio.%(ext)s"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([url])
            audio_filename = os.path.join(output_path, f"{video_id}_audio.mp3")

        print("Download em Alta Fidelidade concluido via YT-DLP!")
        return video_filename, audio_filename
    except Exception as e:
        print(f"Erro Critico YT-DLP: {e}")
        return None, None
