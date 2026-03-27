import os
import yt_dlp

def get_ffmpeg_bin():
    """Tenta encontrar o executável do ffmpeg (embutido no imageio_ffmpeg ou no PATH)"""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return None

def download_youtube_audio(url, output_path="downloads"):
    """Baixa o áudio para transcrição (Economia de Banda)"""
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        print(f"🎙️ Baixando Áudio para IA: {url}")
        ffmpeg_bin = get_ffmpeg_bin()
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(id)s_audio.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
        if ffmpeg_bin: ydl_opts['ffmpeg_location'] = ffmpeg_bin

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return os.path.join(output_path, f"{info['id']}_audio.mp3"), info['id']
    except Exception as e:
        print(f"❌ Erro Áudio: {e}")
        return None, None

def download_youtube_video_720p(url, video_id, output_path="downloads"):
    """Baixa o vídeo em 720p (Ideal para Reels: Rápido e boa qualidade)"""
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    video_filename = os.path.join(output_path, f"{video_id}_vid.mp4")
    if os.path.exists(video_filename):
        return video_filename

    try:
        print(f"🎬 Baixando Vídeo Principal (720p Otimizado): {video_id}...")
        ffmpeg_bin = get_ffmpeg_bin()
        
        ydl_opts = {
            # Busca especificamente MP4 720p ou menor para máxima velocidade e compatibilidade
            'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
            'outtmpl': video_filename,
            'merge_output_format': 'mp4',
            'quiet': True,
        }
        if ffmpeg_bin: ydl_opts['ffmpeg_location'] = ffmpeg_bin

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return video_filename
    except Exception as e:
        print(f"❌ Erro Vídeo 720p: {e}")
        return None

# Funções Legadas para compatibilidade
def download_youtube_video(url, output_path="downloads"):
    a_path, v_id = download_youtube_audio(url, output_path)
    if not a_path: return None, None
    v_path = download_youtube_video_720p(url, v_id, output_path)
    return v_path, a_path

def download_video_section(url, start_time, end_time, output_filename):
    """Fallback: Não usaremos mais por enquanto devido a dependência de ffprobe no CI"""
    # Retorna falso para avisar o main que ele deve usar o video completo baixado em 720p
    return False
