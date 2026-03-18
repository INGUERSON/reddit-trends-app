import os
import yt_dlp

def download_youtube_video(url, output_path="downloads"):
    """
    Downloads a YouTube video in the best MP4 quality (up to 1080p) using yt-dlp.
    Extracts the audio as a separate MP3 file for easy transcription.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        print(f"📥 Conectando ao YouTube via YT-DLP: {url}")
        
        # Otimizado para GitHub Actions (Cloud IPs)
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

        # 2. Extraindo o Áudio para a IA (Whisper) e edição
        print(f"🎵 Extraindo áudio de alta fidelidade para transcrição...")
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

        print("✅ Download em Alta Fidelidade concluído via YT-DLP!")
        return video_filename, audio_filename

    except Exception as e:
        print(f"❌ Erro Crítico YT-DLP: {e}")
        return None, None

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=M7FIvfx5J10" 
    v_path, a_path = download_youtube_video(test_url)
    print(f"Vídeo salvo em: {v_path}")
    print(f"Áudio salvo em: {a_path}")
