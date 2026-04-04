import os
import yt_dlp
import traceback
import random
import json
import urllib.request


# Subreddits com conteudo viral por nicho
REDDIT_NICHES = {
    "marketing digital": ["r/marketing", "r/Entrepreneur", "r/startups"],
    "renda extra e sucesso financeiro": ["r/financialindependence", "r/passive_income", "r/Fire"],
    "tecnologia e inteligencia artificial": ["r/artificial", "r/MachineLearning", "r/technology"],
    "empreendedorismo e negocios": ["r/Entrepreneur", "r/business", "r/smallbusiness"],
    "podcast de cortes milionarios": ["r/Entrepreneur", "r/investing", "r/personalfinance"],
    "AI and future technology": ["r/artificial", "r/Futurology", "r/singularity"],
    "Success mindset and money": ["r/getdisciplined", "r/selfimprovement", "r/financialindependence"],
    "Business scale and automation": ["r/Entrepreneur", "r/automation", "r/SideProject"],
}

# Canais do YouTube de fallback (curtos populares sem bloqueio de geo)
YOUTUBE_FALLBACK_QUERIES = [
    "site:reddit.com podcast viral motivacional",
    "empreendedorismo mindset cortes 2024",
    "business automation success clips",
]


def _get_ydl_opts_base():
    """Opcoes base do yt-dlp com headers realistas para evitar bloqueio."""
    opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        },
    }
    # Se tiver cookies do YouTube configurados, usa
    cookies_b64 = os.getenv("YT_COOKIES_B64")
    if cookies_b64:
        import base64
        cookies_path = "/tmp/yt_cookies.txt"
        with open(cookies_path, "wb") as f:
            f.write(base64.b64decode(cookies_b64))
        opts['cookiefile'] = cookies_path
        print("Usando cookies do YouTube para autenticacao.")
    return opts


def hunt_reddit_videos(subreddit, min_duration=60, max_duration=1800):
    """
    Busca videos virais diretamente no Reddit via API publica.
    Nao requer autenticacao e nao e bloqueado pelo GitHub Actions.
    """
    print(f"Cacando no Reddit: {subreddit} ...")
    url = f"https://www.reddit.com/{subreddit}/hot.json?limit=25&raw_json=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.reddit.com/",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())

        posts = data.get("data", {}).get("children", [])
        video_posts = []
        for post in posts:
            p = post.get("data", {})
            # Filtra posts com video
            is_video = p.get("is_video", False)
            url_hint = p.get("url", "")
            domain = p.get("domain", "")

            # Reddit native video ou links de video externo
            if is_video or domain in ["v.redd.it", "youtube.com", "youtu.be", "streamable.com", "gfycat.com"]:
                permalink = p.get("permalink", "")
                post_url = f"https://www.reddit.com{permalink}" if is_video else url_hint
                score = p.get("score", 0)
                title = p.get("title", "Sem titulo")
                if score > 100:  # So posta conteudo com engajamento real
                    video_posts.append({
                        "url": post_url,
                        "title": title,
                        "score": score,
                        "domain": domain
                    })

        if not video_posts:
            print(f"Nenhum video encontrado com engajamento em {subreddit}.")
            return None

        # Ordena por score (mais viral primeiro)
        video_posts.sort(key=lambda x: x["score"], reverse=True)
        best = video_posts[0]
        print(f"Melhor post Reddit: '{best['title']}' (score: {best['score']})")
        print(f"URL: {best['url']}")
        return best["url"]

    except Exception as e:
        print(f"Erro ao buscar no Reddit ({subreddit}): {e}")
        return None


def hunt_youtube_videos(topic, max_results=5):
    """
    Busca videos no YouTube com configuracoes para evitar bloqueio.
    Usa cookies se disponiveis.
    """
    search_query = f"ytsearch{max_results}:{topic} podcast cortes"
    print(f"Buscando no YouTube: '{search_query}'")

    ydl_opts = _get_ydl_opts_base()
    ydl_opts['playlistend'] = max_results

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            entries = info.get('entries', [])
            valid = [e for e in entries if e and e.get('duration', 0) > 120]
            if not valid:
                return None
            best = sorted(valid, key=lambda x: x.get('view_count', 0) or 0, reverse=True)[0]
            url = f"https://www.youtube.com/watch?v={best.get('id')}"
            print(f"YouTube encontrou: '{best.get('title')}' | views: {best.get('view_count', 0)}")
            return url
    except Exception as e:
        err = str(e)
        if "Sign in" in err or "bot" in err.lower() or "confirm" in err.lower():
            print("YouTube bloqueou acesso (bot detection). Tentando Reddit...")
        else:
            print(f"Erro YouTube: {e}")
        return None


def hunt_viral_videos(topic_or_url, is_profile=False, max_results=5):
    """
    Funcao principal: tenta Reddit primeiro, depois YouTube como fallback.
    Aceita tambem URL direta.
    """
    # URL direta - usa diretamente
    if is_profile or topic_or_url.startswith("http"):
        print(f"URL direta recebida: {topic_or_url}")
        return topic_or_url

    print(f"\nIniciando Cacada Viral para nicho: '{topic_or_url}'")
    print("-" * 40)

    # 1. Tenta Reddit primeiro (mais confiavel em servidores cloud)
    subreddits = REDDIT_NICHES.get(topic_or_url, ["r/Entrepreneur", "r/videos", "r/BeAmazed"])
    random.shuffle(subreddits)

    for subreddit in subreddits:
        url = hunt_reddit_videos(subreddit)
        if url:
            print(f"Reddit retornou URL: {url}")
            return url

    # 2. Fallback: YouTube (funciona se cookies estiverem configurados)
    print("Reddit sem resultados. Tentando YouTube como fallback...")
    url = hunt_youtube_videos(topic_or_url, max_results)
    if url:
        return url

    print(f"Nenhuma fonte encontrou video para: '{topic_or_url}'")
    return None


def feed_video_to_pipeline(video_url):
    with open("input.txt", 'w', encoding='utf-8') as f:
        f.write(video_url)
    print("Video alimentado na Fabrica de Cortes.")
