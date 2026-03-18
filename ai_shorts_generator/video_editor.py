import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.all import crop

def make_text_clip(text, duration, max_width, fontsize=85, color="white"):
    """
    Cria um clipe de texto (legenda) usando Pillow.
    Estilo Alex Hormozi: 1-2 palavras grandes, cores vibrantes (amarelo/verde limão), borda preta grossa.
    """
    width, height = max_width, int(fontsize * 4.0)
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Tenta carregar uma fonte robusta, cai no default se falhar
    font_paths = ["arialbd.ttf", "C:/Windows/Fonts/arialbd.ttf", "montserrat-bold.ttf"]
    font = None
    for p in font_paths:
        try:
            font = ImageFont.truetype(p, fontsize)
            break
        except:
            continue
    if not font:
        font = ImageFont.load_default()
        
    text_bbox = d.textbbox((0, 0), text, font=font, stroke_width=5)
    text_w = text_bbox[2] - text_bbox[0]
    
    # Reduzir a fonte drasticamente se a palavra for gigante (ex: palavras compostas)
    if text_w > max_width - 80:
        new_fontsize = int(fontsize * ((max_width - 80) / max(text_w, 1)))
        try:
            font = ImageFont.truetype("arialbd.ttf", new_fontsize)
        except:
            pass
        text_bbox = d.textbbox((0, 0), text, font=font, stroke_width=5)
        text_w = text_bbox[2] - text_bbox[0]
        
    text_h = text_bbox[3] - text_bbox[1]
    
    # Centraliza o texto no canvas
    x = (width - text_w) / 2
    y = (height - text_h) / 2 - text_bbox[1] 

    # Estilo: Cor vibrante com contorno preto grosso (efeito 'The Bold Font')
    # Tons: Amarelo (#FFFF00), Verde Limão (#32CD32), Branco (#FFFFFF)
    d.text((x, y), text, font=font, fill=color, stroke_width=8, stroke_fill="black")
    
    img_array = np.array(img)
    return ImageClip(img_array).set_duration(duration)

def edit_and_render_clip(video_path, audio_path, start_time, end_time, words_data, output_filename):
    print(f"🎬 Iniciando edição do trecho: {start_time}s até {end_time}s...")
    
    # 1. Carrega o vídeo original e junta o áudio extraído (garante 1080p sem mute)
    try:
        video = VideoFileClip(video_path).subclip(start_time, end_time)
        audio = AudioFileClip(audio_path).subclip(start_time, end_time)
        
        # Otimização de Áudio: Normalização de volume para clareza
        from moviepy.audio.fx.all import audio_normalize
        audio = audio_normalize(audio)
        video = video.set_audio(audio)
    except Exception as e:
        print(f"❌ Falha ao carregar o vídeo ou áudio: {e}")
        return False

    # 2. Formato Vertical 9:16 (TikTok/Reels/Shorts)
    w, h = video.size
    target_ratio = 9/16
    
    # Redimensiona para 1080p vertical se necessário
    if w/h > target_ratio:
        new_w = int(h * target_ratio)
        video = crop(video, width=new_w, height=h, x_center=w/2, y_center=h/2)
    
    # EFEITO DINÂMICO: Zoom Punch-In a cada 4 segundos para manter retenção
    # Alterna entre escala 1.0 e 1.15
    duration = video.duration
    segments = []
    zoom_interval = 4.0
    for i in range(int(duration / zoom_interval) + 1):
        t_start = i * zoom_interval
        t_end = min((i + 1) * zoom_interval, duration)
        if t_start >= duration: break
        
        seg = video.subclip(t_start, t_end)
        if i % 2 == 1: # Zoom-in nos segmentos ímpares
            seg = seg.resize(1.15)
            # Centraliza após o resize
            seg = crop(seg, width=video.w, height=video.h, x_center=seg.w/2, y_center=seg.h/2)
        segments.append(seg)
    
    from moviepy.editor import concatenate_videoclips
    video = concatenate_videoclips(segments)
    print(f"✂️ Resolução final: {video.size} com efeitos de Zoom Dinâmico aplicados.")

    # 3. Gerador dinâmico de Legendas com Destaque de Cores
    clip_words = [w for w in words_data if w['start'] >= start_time and w['end'] <= end_time]
    subtitle_clips = []
    
    vibrant_colors = ["#FFFF00", "#32CD32", "#FFFFFF"] # Amarelo, Verde Limão, Branco
    
    for i, word_data in enumerate(clip_words):
        raw_word = word_data['word'].strip().upper()
        if not raw_word: continue
        text = raw_word.replace('.', '').replace(',', '').replace('?', '').replace('!', '')
        
        t_start = word_data['start'] - start_time
        if i < len(clip_words) - 1:
            t_end = clip_words[i+1]['start'] - start_time
        else:
            t_end = word_data['end'] - start_time
            
        dur = max(t_end - t_start, 0.1)
        
        # Lógica de cor: destaque a cada 3 palavras ou palavras longas (> 6 letras)
        color = "#FFFFFF" # Default Branco
        if i % 3 == 0 or len(text) > 7:
            color = vibrant_colors[i % 2] # Alterna entre amarelo e verde
            
        txt_clip = make_text_clip(text, dur, video.w, color=color)
        txt_clip = txt_clip.set_position(('center', video.h * 0.70)).set_start(t_start)
        subtitle_clips.append(txt_clip)

    print(f"✍️ {len(subtitle_clips)} frames de legenda de alto impacto gerados.")

    # 3.5 Marca d'água / CTA Profissional
    cta_text = "AUTO CASH 2026"
    cta_clip = make_text_clip(cta_text, duration=video.duration, max_width=video.w, fontsize=35, color="#00F0FF")
    cta_clip = cta_clip.set_position(('center', video.h * 0.90)).set_opacity(0.8).set_start(0)

    # 4. Composição Final
    final_video = CompositeVideoClip([video] + subtitle_clips + [cta_clip])
    
    print(f"⚙️ Renderizando (ISSO PODE DEMORAR ALGUNS MINUTOS NESTE PC)...")
    
    try:
        # Usando 'ultrafast' para não queimar a CPU do seu PC e bitrate otimizado para celulares
        final_video.write_videofile(
            output_filename, 
            codec="libx264", 
            audio_codec="aac", 
            temp_audiofile=f"{output_filename}_temp.m4a", 
            remove_temp=True,
            logger=None,    
            threads=os.cpu_count() or 4,     # Usa todos os núcleos que o PC permitir
            preset="ultrafast", # Muito mais rápido render
            bitrate="4000k" # Qualidade boa (TikTok) e tamanho de arquivo leve
        )
        print(f"🚀✅ SUCESSO! CLIPE SALVO COMO: {output_filename}")
    except Exception as e:
        print(f"❌ Erro fatal durante a conversão do FFmpeg: {e}")
        
    # Boas práticas: liberar memória
    video.close()
    final_video.close()
    return True
