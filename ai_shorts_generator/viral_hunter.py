import os
import json
import yt_dlp
import traceback
from datetime import datetime
import random

def hunt_viral_videos(topic_or_url, is_profile=False, max_results=5):
    """
    Usa o yt-dlp para caçar os vídeos mais em alta sobre um tópico (YouTube)
    ou de um perfil específico (TikTok/Instagram).
    """
    print(f"\n🕵️‍♂️ Iniciando Caçada Viral: '{topic_or_url}'")
    
    # Se for uma busca no YouTube
    if not is_profile and not topic_or_url.startswith('http'):
        search_query = f"ytsearch{max_results}:{topic_or_url} podcast"
    else:
        # Se for um link de TikTok ou Instagram de algum perfil
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
            print(f"📡 Varrendo a rede: {search_query}...")
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' in info:
                # É uma playlist ou resultado de busca
                for entry in info['entries']:
                    if entry:
                        results.append({
                            'id': entry.get('id'),
                            'title': entry.get('title'),
                            'url': entry.get('url') if entry.get('url') else f"https://www.youtube.com/watch?v={entry.get('id')}",
                            'view_count': entry.get('view_count', 0),
                            'duration': entry.get('duration', 0)
                        })
            else:
                # É um vídeo único
                results.append({
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'url': info.get('webpage_url', topic_or_url),
                    'view_count': info.get('view_count', 0),
                    'duration': info.get('duration', 0)
                })

    except Exception as e:
        print(f"❌ Erro ao caçar vídeos: {e}")
        traceback.print_exc()
        return None

    # Filtrar e ordenar por visualizações se for busca, ou pegar apenas longa duração (para cortes)
    # Aqui, priorizamos vídeos entre 10 minutos (600s) e 4 horas (14400s) para ter conteúdo rico para cortes.
    valid_videos = []
    for v in results:
        # Pular shorts/vídeos muito curtos se queremos extrair cortes profundos de podcasts
        if v.get('duration') and v['duration'] > 300: # Mais de 5 minutos
            valid_videos.append(v)
            
    if not valid_videos:
        # Fallback: pegar o que tiver maior visualização
        valid_videos = results
        
    if not valid_videos:
        print("❌ Nenhum vídeo válido encontrado.")
        return None

    # Ordenar pelos mais vistos
    valid_videos.sort(key=lambda x: x.get('view_count') or 0, reverse=True)
    
    best_video = valid_videos[0]
    print(f"\n🎯 ALVO ENCONTRADO!")
    print(f" Título: {best_video['title']}")
    print(f" Duração: {best_video['duration']}s")
    print(f" Views: {best_video['view_count']}")
    print(f" Link: {best_video['url']}")
    
    return best_video['url']

def feed_video_to_pipeline(video_url):
    """
    Substitui o link no arquivo input.txt para a pipeline processar.
    """
    input_file = "input.txt"
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(video_url)
    print(f"✅ Vídeo alimentado na Fábrica de Cortes ({input_file}).")

if __name__ == "__main__":
    print("="*50)
    print("🤖 AGENTE CAÇADOR VIRAL (YouTube / TikTok / IG)")
    print("="*50)
    
    # Nichos de exemplo para varredura orgânica
    niches = [
        "marketing digital",
        "renda extra",
        "inteligência artificial",
        "vendas online",
        "gestão de tempo"
    ]
    
    print("Aguardando comando ou selecionando nicho aleatório...")
    chosen_niche = random.choice(niches)
    
    # Você também pode trocar para um perfil específico:
    # url = hunt_viral_videos("https://www.tiktok.com/@mrbeast", is_profile=True, max_results=3)
    
    url = hunt_viral_videos(chosen_niche, is_profile=False, max_results=10)
    
    if url:
        feed_video_to_pipeline(url)
        print("\nPróximo passo:")
        print("Rode o comando: python main.py")
        print("Para que o Agente de Corte inicie a edição deste novo vídeo automaticamente!")
