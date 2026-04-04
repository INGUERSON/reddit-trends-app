import os
import yt_dlp
import random
import json


# Queries de busca no Pexels por nicho (apenas visuais de fundo)
PEXELS_QUERIES = {
    "marketing digital": ["digital marketing office", "business meeting", "entrepreneur work"],
    "renda extra e sucesso financeiro": ["financial success", "money wealth", "business growth"],
    "tecnologia e inteligencia artificial": ["artificial intelligence", "technology future", "robot machine"],
    "empreendedorismo e negocios": ["business startup", "office work", "entrepreneur success"],
    "podcast de cortes milionarios": ["city timelapse", "success lifestyle", "motivation"],
    "AI and future technology": ["artificial intelligence", "future technology", "data center"],
    "Success mindset and money": ["success motivation", "financial freedom", "luxury lifestyle"],
    "Joe Rogan powerful clips": ["podcast studio", "microphone studio", "interview setup"],
    "Business scale and automation": ["business automation", "factory production", "scale"],
}

# Queries de busca no YouTube por nicho (para fala/audio)
YOUTUBE_QUERIES = {
    "marketing digital": "marketing digital podcast motivacao PT",
    "renda extra e sucesso financeiro": "sucesso financeiro podcast motivacional",
    "tecnologia e inteligencia artificial": "inteligencia artificial futuro podcast",
    "empreendedorismo e negocios": "empreendedorismo negocios podcast brasileiro",
    "podcast de cortes milionarios": "flavio augusto pablo marçal cortes podcast",
    "AI and future technology": "artificial intelligence future podcast English",
    "Success mindset and money": "millionaire mindset success podcast motivational",
    "Joe Rogan powerful clips": "joe rogan podcast motivational speech clips",
    "Business scale and automation": "business scale automation entrepreneurship podcast",
}


def hunt_pexels_background(topic):
    """
    Baixa um video de fundo do Pexels (sem fala, apenas visual).
    Retorna a URL direta do arquivo MP4.
    """
    import requests as req_lib

    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        print("PEXELS_API_KEY nao configurada.")
        return None

    print(f"Pexels key: {api_key[:8]}... ({len(api_key)} chars)")

    queries = PEXELS_QUERIES.get(topic, ["city timelapse", "nature landscape", "abstract background"])
    query = random.choice(queries)
    print(f"Buscando background Pexels: '{query}'")

    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": api_key, "User-Agent": "Mozilla/5.0"}
    params = {"query": query, "per_page": 15, "min_duration": 60}

    try:
        r = req_lib.get(url, headers=headers, params=params, timeout=15)
        print(f"Pexels status: {r.status_code}")
        if r.status_code != 200:
            print(f"Pexels erro: {r.text[:200]}")
            return None

        videos = r.json().get("videos", [])
        if not videos:
            print("Nenhum video de fundo encontrado no Pexels.")
            return None

        # Prefere HD (1080p) para economizar espaco e tempo
        videos.sort(key=lambda x: x.get("duration", 0), reverse=True)
        for vid in videos:
            files = vid.get("video_files", [])
            # Filtra arquivos com resolucao 1080p ou menor
            hd_files = [f for f in files if f.get("height", 9999) <= 1080 and f.get("height", 0) >= 720]
            if not hd_files:
                hd_files = files
            hd_files.sort(key=lambda x: x.get("width", 0), reverse=True)
            if hd_files:
                video_url = hd_files[0].get("link", "")
                print(f"Pexels background encontrado: {vid.get('duration')}s ({hd_files[0].get('width')}x{hd_files[0].get('height')})")
                return video_url

    except Exception as e:
        print(f"Erro Pexels: {e}")
    return None


def hunt_youtube_speech(topic, max_results=5):
    """
    Busca no YouTube um podcast/fala para usar como fonte de audio/transcricao.
    Retorna apenas a URL (sem download).
    """
    yt_query = YOUTUBE_QUERIES.get(topic, f"{topic} podcast motivacional")
    search_query = f"ytsearch{max_results}:{yt_query}"
    print(f"Buscando fala YouTube: '{yt_query}'")

    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
        "no_warnings": True,
        "playlistend": max_results,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        },
    }

    cookies_b64 = os.getenv("YT_COOKIES_B64")
    if cookies_b64:
        import base64
        cookies_path = "/tmp/yt_cookies.txt"
        with open(cookies_path, "wb") as f:
            f.write(base64.b64decode(cookies_b64))
        ydl_opts["cookiefile"] = cookies_path
        print("Cookies YT carregados.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            entries = info.get("entries", [])
            # Filtra videos longos (podcasts tem mais conteudo)
            valid = [e for e in entries if e and e.get("duration", 0) > 300]
            if not valid:
                valid = [e for e in entries if e]
            if not valid:
                return None
            best = sorted(valid, key=lambda x: x.get("view_count", 0) or 0, reverse=True)[0]
            yt_url = f"https://www.youtube.com/watch?v={best.get('id')}"
            print(f"YouTube fala: '{best.get('title')}' | {best.get('duration')}s | views: {best.get('view_count', 0)}")
            return yt_url
    except Exception as e:
        print(f"YouTube erro busca: {e}")
        return None


def hunt_viral_videos(topic_or_url, is_profile=False, max_results=5):
    """
    Funcao principal. Retorna um dict com:
      - video_url: URL do video de fundo (Pexels ou YouTube)
      - audio_url: URL da fonte de audio/fala (YouTube)
    
    Se URL direta fornecida: usa ela para ambos.
    """
    if is_profile or topic_or_url.startswith("http"):
        print(f"URL direta: {topic_or_url}")
        return {"video_url": topic_or_url, "audio_url": topic_or_url}

    print(f"\n{'='*50}")
    print(f"CACADA DUAL-FONTE: '{topic_or_url}'")
    print(f"{'='*50}")

    # Fonte 1: Pexels para background visual
    pexels_url = hunt_pexels_background(topic_or_url)

    # Fonte 2: YouTube para fala/audio
    yt_url = hunt_youtube_speech(topic_or_url, max_results)

    if pexels_url and yt_url:
        print(f"Dual-fonte: Pexels (visual) + YouTube (audio)")
        return {"video_url": pexels_url, "audio_url": yt_url}
    elif yt_url:
        print(f"Fonte: YouTube (video + audio)")
        return {"video_url": yt_url, "audio_url": yt_url}
    elif pexels_url:
        print(f"Fonte: Pexels apenas (sem audio de fala)")
        return {"video_url": pexels_url, "audio_url": pexels_url}
    else:
        print(f"Nenhuma fonte encontrada para: '{topic_or_url}'")
        return None


def feed_video_to_pipeline(video_url):
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(video_url if isinstance(video_url, str) else video_url.get("video_url", ""))
    print("Video alimentado na Fabrica de Cortes.")
