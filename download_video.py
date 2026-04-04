import os
import re
import base64
import traceback
import yt_dlp


def _get_cookies_file():
    """Cria arquivo de cookies do YouTube a partir do secret do GitHub, se disponivel."""
    cookies_b64 = os.getenv("YT_COOKIES_B64")
    if cookies_b64:
        cookies_path = "/tmp/yt_cookies.txt"
        try:
            with open(cookies_path, "wb") as f:
                f.write(base64.b64decode(cookies_b64))
            print("Cookies do YouTube carregados para download.")
            return cookies_path
        except Exception as e:
            print(f"Erro ao carregar cookies: {e}")
    return None


def _build_ydl_opts(output_path, format_str, extra_opts=None):
    """Constroi opcoes do yt-dlp com headers realistas."""
    opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': format_str,
        'quiet': False,
        'no_warnings': False,
        'http_headers': {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        },
        'retries': 5,
        'fragment_retries': 5,
        'socket_timeout': 60,
    }
    cookies_file = _get_cookies_file()
    if cookies_file:
        opts['cookiefile'] = cookies_file

    if extra_opts:
        opts.update(extra_opts)
    return opts


def download_youtube_video(url, output_path="downloads"):
    """
    Baixa video e audio separadamente.
    Suporta YouTube, Reddit (v.redd.it), e outras plataformas via yt-dlp.
    Retorna (video_path, audio_path) ou (None, None) em caso de falha.
    """
    os.makedirs(output_path, exist_ok=True)
    print(f"Iniciando download: {url}")

    # Para Reddit native video, usa configuracao especial
    is_reddit = "reddit.com" in url or "v.redd.it" in url

    if is_reddit:
        print("Fonte Reddit detectada.")
        video_format = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    else:
        # YouTube: tenta 1080p primeiro, depois 720p
        video_format = (
            "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]"
            "/bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]"
            "/best[ext=mp4]/best"
        )

    # --- Download do VIDEO ---
    video_path = None
    video_opts = _build_ydl_opts(output_path, video_format, {
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    })

    try:
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            # Limpa o titulo para nome de arquivo valido
            safe_title = re.sub(r'[\\/*?:"<>|]', '', title)[:60]
            video_path = os.path.join(output_path, f"{safe_title}.mp4")
            if not os.path.exists(video_path):
                # Tenta encontrar o arquivo pelo padrao gerado
                for f in os.listdir(output_path):
                    if f.endswith('.mp4'):
                        video_path = os.path.join(output_path, f)
                        break
        print(f"Video salvo: {video_path}")
    except Exception as e:
        err = str(e)
        if "Sign in" in err or "bot" in err.lower():
            print("YouTube bloqueou o download (bot detection).")
            print("Solucao: adicione o secret YT_COOKIES_B64 no GitHub.")
        else:
            print(f"Erro no download do video: {e}")
            traceback.print_exc()
        return None, None

    # --- Download do AUDIO separado (para transcricao com Whisper) ---
    audio_path = None
    audio_opts = _build_ydl_opts(output_path, "bestaudio/best", {
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s_audio.%(ext)s'),
    })

    try:
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            safe_title = re.sub(r'[\\/*?:"<>|]', '', title)[:60]
            audio_path = os.path.join(output_path, f"{safe_title}_audio.mp3")
            if not os.path.exists(audio_path):
                for f in os.listdir(output_path):
                    if f.endswith('.mp3'):
                        audio_path = os.path.join(output_path, f)
                        break
        print(f"Audio salvo: {audio_path}")
    except Exception as e:
        print(f"Erro no download do audio: {e}")
        traceback.print_exc()
        return None, None

    if not video_path or not os.path.exists(video_path):
        print("Arquivo de video nao encontrado apos download.")
        return None, None

    if not audio_path or not os.path.exists(audio_path):
        print("Arquivo de audio nao encontrado apos download.")
        return None, None

    return video_path, audio_path
