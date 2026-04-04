import os
import yt_dlp
import traceback
import random
import json
import urllib.request


REDDIT_NICHES = {
    "marketing digital": ["r/marketing", "r/Entrepreneur"],
    "renda extra e sucesso financeiro": ["r/financialindependence", "r/passive_income"],
    "tecnologia e inteligencia artificial": ["r/artificial", "r/MachineLearning"],
    "empreendedorismo e negocios": ["r/Entrepreneur", "r/business"],
    "podcast de cortes milionarios": ["r/Entrepreneur", "r/investing"],
    "AI and future technology": ["r/artificial", "r/Futurology"],
    "Success mindset and money": ["r/getdisciplined", "r/selfimprovement"],
    "Business scale and automation": ["r/Entrepreneur", "r/automation"],
}


def hunt_reddit_videos(subreddit):
    print(f"Cacando no Reddit: {subreddit} ...")
    url = f"https://www.reddit.com/{subreddit}/hot.json?limit=25"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; viral-bot/1.0)"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
        posts = data.get("data", {}).get("children", [])
        video_posts = []
        for post in posts:
            p = post.get("data", {})
            is_video = p.get("is_video", False)
            post_url = p.get("url", "")
            domain = p.get("domain", "")
            score = p.get("score", 0)
            title = p.get("title", "Sem titulo")
            permalink = p.get("permalink", "")
            if is_video or domain in ["v.redd.it", "youtube.com", "youtu.be"]:
                final_url = f"https://www.reddit.com{permalink}" if is_video else post_url
                if score > 50:
                    video_posts.append({"url": final_url, "title": title, "score": score})
        if not video_posts:
            print(f"Nenhum video com engajamento em {subreddit}.")
            return None
        video_posts.sort(key=lambda x: x["score"], reverse=True)
        best = video_posts[0]
        print(f"Reddit encontrou: {best[String.fromCharCode(39)+'title'+String.fromCharCode(39)]} (score: {best[String.fromCharCode(39)+'score'+String.fromCharCode(39)]})")
        return best["url"]
    except Exception as e:
        print(f"Erro Reddit ({subreddit}): {e}")
        return None


def hunt_youtube_videos(topic, max_results=5):
    search_query = f"ytsearch{max_results}:{topic} podcast"
    print(f"Buscando no YouTube: {search_query}")
    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
        "no_warnings": True,
        "playlistend": max_results,
        "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    }
    cookies_b64 = os.getenv("YT_COOKIES_B64")
    if cookies_b64:
        import base64
        with open("/tmp/yt_cookies.txt", "wb") as f:
            f.write(base64.b64decode(cookies_b64))
        ydl_opts["cookiefile"] = "/tmp/yt_cookies.txt"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            entries = info.get("entries", [])
            valid = [e for e in entries if e and e.get("duration", 0) > 120]
            if not valid:
                return None
            best = sorted(valid, key=lambda x: x.get("view_count", 0) or 0, reverse=True)[0]
            vid_id = best.get("id", "")
            url = "https://www.youtube.com/watch?v=" + vid_id
            print(f"YouTube: {best.get(String.fromCharCode(34)+'title'+String.fromCharCode(34))} | views: {best.get(String.fromCharCode(34)+'view_count'+String.fromCharCode(34), 0)}")
            return url
    except Exception as e:
        print(f"YouTube bloqueou ou erro: {e}")
        return None


def hunt_viral_videos(topic_or_url, is_profile=False, max_results=5):
    if is_profile or topic_or_url.startswith("http"):
        return topic_or_url
    print(f"Iniciando Cacada Viral: {topic_or_url}")
    subs = REDDIT_NICHES.get(topic_or_url, ["r/Entrepreneur", "r/videos"])
    random.shuffle(subs)
    for sub in subs:
        url = hunt_reddit_videos(sub)
        if url:
            print(f"Reddit retornou: {url}")
            return url
    print("Reddit sem resultados. Tentando YouTube...")
    url = hunt_youtube_videos(topic_or_url, max_results)
    if url:
        return url
    print(f"Nenhuma fonte encontrou video para: {topic_or_url}")
    return None


def feed_video_to_pipeline(video_url):
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(video_url)
    print("Video alimentado.")