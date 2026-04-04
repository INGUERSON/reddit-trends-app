import os
import yt_dlp
import traceback
import random
import json
import urllib.request
import urllib.parse


# Termos de busca por nicho para o Pexels
PEXELS_QUERIES = {
    "marketing digital": ["digital marketing", "business success", "entrepreneur"],
    "renda extra e sucesso financeiro": ["financial freedom", "money success", "wealth"],
    "tecnologia e inteligencia artificial": ["artificial intelligence", "technology future", "robot"],
    "empreendedorismo e negocios": ["entrepreneur success", "business growth", "startup"],
    "podcast de cortes milionarios": ["motivational speech", "success mindset", "millionaire"],
    "AI and future technology": ["artificial intelligence", "future technology", "machine learning"],
    "Success mindset and money": ["success motivation", "financial freedom", "mindset"],
    "Business scale and automation": ["business automation", "scale business", "productivity"],
}


def hunt_pexels_video(topic):
    """
    Busca videos no Pexels (API publica, sem bloqueio de cloud IPs).
    Requer PEXELS_API_KEY no GitHub Secrets.
    """
    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        print("PEXELS_API_KEY nao configurada. Pulando Pexels.")
        return None

    queries = PEXELS_QUERIES.get(topic, ["motivation", "success", "business"])
    query = random.choice(queries)
    print(f"Buscando no Pexels: '{query}'")

    encoded_query = urllib.parse.quote(query)
    url = f"https://api.pexels.com/videos/search?query={encoded_query}&per_page=10&min_duration=60"

    try:
        req = urllib.request.Request(url, headers={"Authorization": api_key})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())

        videos = data.get("videos", [])
        if not videos:
            print("Nenhum video encontrado no Pexels.")
            return None

        # Pega o video mais longo (mais conteudo para cortar)
        videos.sort(key=lambda x: x.get("duration", 0), reverse=True)
        best = videos[0]
        # Pega a URL do arquivo de video (maior qualidade disponivel)
        video_files = best.get("video_files", [])
        video_files.sort(key=lambda x: x.get("width", 0), reverse=True)
        if not video_files:
            return None

        video_url = video_files[0].get("link", "")
        print(f"Pexels encontrou: '{best.get('url')}' ({best.get('duration')}s)")
        return video_url

    except Exception as e:
        print(f"Erro Pexels: {e}")
        return None


def hunt_youtube_search(topic, max_results=5):
    """
    Busca metadados no YouTube (sem download, sem bloqueio).
    Retorna a URL do melhor video encontrado.
    """
    search_query = f"ytsearch{max_results}:{topic} podcast motivacional"
    print(f"Buscando no YouTube: '{search_query}'")

    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
        "no_warnings": True,
        "playlistend": max_results,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        },
    }

    # Usa cookies se disponiveis
    cookies_b64 = os.getenv("YT_COOKIES_B64")
    if cookies_b64:
        import base64
        cookies_path = "/tmp/yt_cookies.txt"
        with open(cookies_path, "wb") as f:
            f.write(base64.b64decode(cookies_b64))
        ydl_opts["cookiefile"] = cookies_path
        print("Cookies do YouTube carregados.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            entries = info.get("entries", [])
            valid = [e for e in entries if e and e.get("duration", 0) > 120]
            if not valid:
                valid = [e for e in entries if e]
            if not valid:
                return None
            best = sorted(valid, key=lambda x: x.get("view_count", 0) or 0, reverse=True)[0]
            url = f"https://www.youtube.com/watch?v={best.get('id')}"
            print(f"YouTube encontrou: '{best.get('title')}' | views: {best.get('view_count', 0)}")
            return url
    except Exception as e:
        print(f"YouTube erro na busca: {e}")
        return None


def hunt_viral_videos(topic_or_url, is_profile=False, max_results=5):
    """
    Funcao principal de busca de videos.
    Ordem de tentativas:
    1. URL direta (se fornecida)
    2. Pexels API (se PEXELS_API_KEY configurada)
    3. YouTube com cookies (se YT_COOKIES_B64 configurada)
    4. YouTube sem autenticacao (pode ser bloqueado em cloud)
    """
    # URL direta
    if is_profile or topic_or_url.startswith("http"):
        print(f"URL direta recebida: {topic_or_url}")
        return topic_or_url

    print(f"\n{'='*50}")
    print(f"CACADA VIRAL: '{topic_or_url}'")
    print(f"{'='*50}")

    # Tentativa 1: Pexels (mais confiavel em cloud)
    url = hunt_pexels_video(topic_or_url)
    if url:
        print(f"Fonte: Pexels | URL: {url}")
        return url

    # Tentativa 2: YouTube (com ou sem cookies)
    url = hunt_youtube_search(topic_or_url, max_results)
    if url:
        print(f"Fonte: YouTube | URL: {url}")
        return url

    print(f"Nenhuma fonte encontrou video para: '{topic_or_url}'")
    return None


def feed_video_to_pipeline(video_url):
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(video_url)
    print("Video alimentado na Fabrica de Cortes.")
