import os
import sys
import re
import base64
import traceback
import requests
import yt_dlp
import imageio_ffmpeg

def _get_ffmpeg_path():
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def _get_cookies_opts():
    """
    Retorna opcoes de cookies para yt-dlp.
    - No GitHub Actions: usa YT_COOKIES_B64 (base64 do arquivo de cookies)
    """
    # Prioridade 1: secret do GitHub Actions / .env local
    cookies_b64 = os.getenv("YT_COOKIES_B64")
    if cookies_b64:
        cookies_path = "/tmp/yt_cookies.txt"
        try:
            # Cria a pasta caso nao exista (pode faltar no Windows)
            os.makedirs(os.path.dirname(cookies_path), exist_ok=True)
            with open(cookies_path, "wb") as f:
                f.write(base64.b64decode(cookies_b64))
            print("Cookies do YouTube carregados via texto codificado.")
            return {"cookiefile": cookies_path}
        except Exception as e:
            print(f"Erro ao carregar cookies base64: {e}")

    # Sem cookies por padrao. PC local geralmente nao e bloqueado pelo YouTube (IP residencial)
    return {}


def download_pexels_video(url, output_path="downloads"):
    """
    Baixa video diretamente de URL Pexels usando requests.
    Retorna (video_path, None) - Pexels nao tem audio de fala.
    """
    os.makedirs(output_path, exist_ok=True)
    # Extrai nome do arquivo da URL
    filename = url.split("/")[-1].split("?")[0]
    if not filename.endswith(".mp4"):
        filename = f"pexels_{filename}.mp4"
    video_path = os.path.join(output_path, filename)

    print(f"Baixando video Pexels: {filename}")
    try:
        with requests.get(url, stream=True, timeout=120) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(video_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded / total * 100
                        if downloaded % (10 * 1024 * 1024) < 1024 * 1024:
                            print(f"  {pct:.0f}% ({downloaded // 1024 // 1024}MB/{total // 1024 // 1024}MB)")
        print(f"Video Pexels salvo: {video_path} ({os.path.getsize(video_path) // 1024 // 1024}MB)")
        return video_path
    except Exception as e:
        print(f"Erro ao baixar Pexels: {e}")
        return None


def download_youtube_audio_only(url, output_path="downloads"):
    """
    Baixa APENAS o audio de um video YouTube (para transcricao com Whisper).
    Audio-only e muito mais leve e menos bloqueado do que video completo.
    Retorna caminho do arquivo mp3.
    """
    os.makedirs(output_path, exist_ok=True)
    print(f"Baixando audio YouTube: {url}")

    audio_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_path, "%(id)s_audio.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "128",  # 128kbps suficiente para transcricao
        }],
        "quiet": False,
        "no_warnings": False,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        },
        "socket_timeout": 60,
        "retries": 3,
        # Baixa apenas os primeiros 15 minutos (suficiente para 3 clips virais)
        "postprocessor_args": ["-t", "900"],
    }
    
    ffmpeg_exe = _get_ffmpeg_path()
    if ffmpeg_exe:
        audio_opts["ffmpeg_location"] = ffmpeg_exe

    audio_opts.update(_get_cookies_opts())

    try:
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get("id", "audio")
            audio_path = os.path.join(output_path, f"{video_id}_audio.mp3")
            # Busca o arquivo gerado
            if not os.path.exists(audio_path):
                for f in os.listdir(output_path):
                    if f.endswith(".mp3") and "audio" in f:
                        audio_path = os.path.join(output_path, f)
                        break
        if os.path.exists(audio_path):
            size_mb = os.path.getsize(audio_path) / 1024 / 1024
            print(f"Audio YT salvo: {audio_path} ({size_mb:.1f}MB)")
            return audio_path
        else:
            print("Arquivo de audio nao encontrado apos download.")
            return None
    except Exception as e:
        err = str(e)
        if "Sign in" in err or "bot" in err.lower():
            print("YouTube bloqueou download (bot detection). Adicione YT_COOKIES_B64.")
        else:
            print(f"Erro audio YT: {e}")
        return None


def download_youtube_video(url, output_path="downloads"):
    """
    Baixa video E audio de YouTube (modo completo).
    Usado quando YouTube e a unica fonte disponivel.
    Retorna (video_path, audio_path).
    """
    os.makedirs(output_path, exist_ok=True)
    print(f"Download completo YouTube: {url}")

    video_opts = {
        "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
        "outtmpl": os.path.join(output_path, "%(id)s_vid.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": False,
        "no_warnings": False,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        },
        "socket_timeout": 60,
        "retries": 3,
    }

    ffmpeg_exe = _get_ffmpeg_path()
    if ffmpeg_exe:
        video_opts["ffmpeg_location"] = ffmpeg_exe

    video_opts.update(_get_cookies_opts())

    video_path = None
    try:
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get("id", "video")
            video_path = os.path.join(output_path, f"{video_id}_vid.mp4")
            if not os.path.exists(video_path):
                for f in os.listdir(output_path):
                    if f.endswith(".mp4"):
                        video_path = os.path.join(output_path, f)
                        break
        print(f"Video salvo: {video_path}")
    except Exception as e:
        err = str(e)
        if "Sign in" in err or "bot" in err.lower():
            print("YouTube bloqueou download. Adicione YT_COOKIES_B64.")
        else:
            print(f"Erro video YT: {e}")
            traceback.print_exc()
        return None, None

    audio_path = download_youtube_audio_only(url, output_path)
    if not audio_path:
        return None, None

    return video_path, audio_path


def download_dual_source(video_url, audio_url, output_path="downloads"):
    """
    Download dual-fonte:
    - video_url: URL Pexels (background visual)
    - audio_url: URL YouTube (fala para transcricao)
    Retorna (video_path, audio_path).
    """
    is_pexels_video = "pexels.com" in video_url or "videos.pexels.com" in video_url
    is_yt_audio = "youtube.com" in audio_url or "youtu.be" in audio_url

    if is_pexels_video:
        print("Modo dual-fonte: Pexels (visual) + YouTube (audio)")
        video_path = download_pexels_video(video_url, output_path)
    else:
        # YouTube para ambos
        video_path, _ = download_youtube_video(video_url, output_path)

    if not video_path:
        print("Falha no download do video.")
        return None, None

    if is_yt_audio and audio_url != video_url:
        audio_path = download_youtube_audio_only(audio_url, output_path)
    elif is_pexels_video and not is_yt_audio:
        # Pexels para ambos (fallback - pode nao ter fala)
        audio_path = video_path
    else:
        audio_path = download_youtube_audio_only(audio_url, output_path)

    return video_path, audio_path
