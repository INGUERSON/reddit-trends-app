import os
import yt_dlp
import traceback
import random


def hunt_viral_videos(topic_or_url, is_profile=False, max_results=5):
    print(f"Iniciando Cacada Viral: '{topic_or_url}'")
    if not is_profile and not topic_or_url.startswith('http'):
        search_query = f"ytsearch{max_results}:{topic_or_url} podcast"
    else:
        search_query = topic_or_url

    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'playlistend': max_results,
    }

    results = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Varrendo a rede: {search_query}...")
            info = ydl.extract_info(search_query, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        vid_url = entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
                        results.append({
                            'id': entry.get('id'),
                            'title': entry.get('title'),
                            'url': vid_url,
                            'view_count': entry.get('view_count', 0),
                            'duration': entry.get('duration', 0)
                        })
            else:
                results.append({
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'url': info.get('webpage_url', topic_or_url),
                    'view_count': info.get('view_count', 0),
                    'duration': info.get('duration', 0)
                })
    except Exception as e:
        print(f"Erro ao cacar videos: {e}")
        traceback.print_exc()
        return None

    valid_videos = [v for v in results if v.get('duration') and v['duration'] > 300]
    if not valid_videos:
        valid_videos = results
    if not valid_videos:
        print("Nenhum video valido encontrado.")
        return None

    valid_videos.sort(key=lambda x: x.get('view_count') or 0, reverse=True)
    best_video = valid_videos[0]
    print(f"ALVO ENCONTRADO: {best_video['title']}")
    print(f"Duracao: {best_video['duration']}s | Views: {best_video['view_count']}")
    print(f"Link: {best_video['url']}")
    return best_video['url']


def feed_video_to_pipeline(video_url):
    with open("input.txt", 'w', encoding='utf-8') as f:
        f.write(video_url)
    print("Video alimentado na Fabrica de Cortes.")
