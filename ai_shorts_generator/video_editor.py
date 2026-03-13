import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.all import crop

def make_text_clip(text, duration, max_width, fontsize=75, color="yellow"):
    """
    Cria um clipe de texto (legenda) usando Pillow.
    Estilo Alex Hormozi ULTRA VIRAL: 1 palavra por vez bem grande, borda preta grossa, sem caixa.
    """
    width, height = max_width, int(fontsize * 3.0)
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arialbd.ttf", fontsize)
    except:
        font = ImageFont.load_default()
        
    text_bbox = d.textbbox((0, 0), text, font=font, stroke_width=4)
    text_w = text_bbox[2] - text_bbox[0]
    
    # Reduzir a fonte dinamicamente se a frase for muito larga para a tela
    if text_w > max_width - 60:
        new_fontsize = int(fontsize * ((max_width - 60) / max(text_w, 1)))
        try:
            font = ImageFont.truetype("arialbd.ttf", new_fontsize)
        except:
            pass
        text_bbox = d.textbbox((0, 0), text, font=font, stroke_width=4)
        text_w = text_bbox[2] - text_bbox[0]
        
    text_h = text_bbox[3] - text_bbox[1]
    
    # Centraliza o texto no canvas
    x = (width - text_w) / 2
    y = (height - text_h) / 2 - text_bbox[1] 

    # Letra Amarela chamativa com stroke (borda) preta grossa
    d.text((x, y), text, font=font, fill=color, stroke_width=5, stroke_fill="black")
    
    img_array = np.array(img)
    return ImageClip(img_array).set_duration(duration)

def edit_and_render_clip(video_path, audio_path, start_time, end_time, words_data, output_filename):
    print(f"🎬 Iniciando edição do trecho: {start_time}s até {end_time}s...")
    
    # 1. Carrega o vídeo original e junta o áudio extraído (garante 1080p sem mute)
    try:
        video = VideoFileClip(video_path).subclip(start_time, end_time)
        audio = AudioFileClip(audio_path).subclip(start_time, end_time)
        video = video.set_audio(audio)
    except Exception as e:
        print(f"❌ Falha ao carregar o vídeo ou áudio. Tente novamente: {e}")
        return False

    # 2. Formato Vertical 9:16 (TikTok/Reels/Shorts)
    w, h = video.size
    target_ratio = 9/16
    current_ratio = w/h
    
    if current_ratio > target_ratio:
        # Corta as bordas (paisagem do YouTube para Vertical do TikTok)
        new_w = int(h * target_ratio)
        x_center = w / 2
        y_center = h / 2
        video = crop(video, width=new_w, height=h, x_center=x_center, y_center=y_center)
        
    print(f"✂️ Resolução final definida como Vertical {video.size}...")

    # 3. Gerador dinâmico de Legendas (Subtitles) - Estilo Alex Hormozi (dinâmico e rápido)
    # Filtra apenas as palavras do nosso trecho
    clip_words = [w for w in words_data if w['start'] >= start_time and w['end'] <= end_time]
    
    subtitle_clips = []
    
    # VIRAL STYLE: 1 palavra por vez jogada na tela para prender absoluta atenção
    group_size = 1
    for i in range(0, len(clip_words), group_size):
        chunk = clip_words[i:i+group_size]
        if not chunk: continue
        
        # Junta e limpa pontuações estranhas (opcional) no meio da tela
        # Removemos pontuação do final da palavra para o texto ficar limpo
        raw_word = " ".join([w['word'] for w in chunk]).strip().upper()
        text = raw_word.replace('.', '').replace(',', '').replace('?', '').replace('!', '')
        
        # Ajusta tempo começando do ZERO (porque carregamos como um subclip)
        t_start = chunk[0]['start'] - start_time
        t_end = chunk[-1]['end'] - start_time
        duration = t_end - t_start
        
        # Prevenção: Palavras faladas muito rapidamente
        if duration <= 0:
            duration = 0.4
            
        txt_clip = make_text_clip(text, duration, video.w)
        # Posiciona visualmente no meio da tela um pouquinho para baixo
        txt_clip = txt_clip.set_position(('center', 'center')).set_start(t_start)
        subtitle_clips.append(txt_clip)

    print(f"✍️ {len(subtitle_clips)} frames de legenda animada gerados com sucesso...")

    # 4. Queimando tudo junto no filme
    final_video = CompositeVideoClip([video] + subtitle_clips)
    
    print(f"⚙️ Renderizando (ISSO PODE DEMORAR ALGUNS MINUTOS NESTE PC)...")
    
    try:
        # A magia negra do FFmpeg. Render usando libx264 e limpando sujeira do cache.
        final_video.write_videofile(
            output_filename, 
            codec="libx264", 
            audio_codec="aac", 
            temp_audiofile=f"{output_filename}_temp.m4a", 
            remove_temp=True,
            logger=None,    
            threads=4,     # Multithreading pro PC suar
            preset="fast", # Acelera bastante a taxa de render
            bitrate="8000k" # Qualidade muito maior (High Bitrate)
        )
        print(f"🚀✅ SUCESSO! CLIPE SALVO COMO: {output_filename}")
    except Exception as e:
        print(f"❌ Erro fatal durante a conversão do FFmpeg: {e}")
        
    # Boas práticas: liberar memória
    video.close()
    final_video.close()
    return True
