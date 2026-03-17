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
    
    # VIRAL STYLE: 1 palavra por vez na tela (ajuste para evitar sobreposição)
    for i in range(len(clip_words)):
        word_data = clip_words[i]
        
        raw_word = word_data['word'].strip().upper()
        if not raw_word: continue
        text = raw_word.replace('.', '').replace(',', '').replace('?', '').replace('!', '')
        
        # Ajusta tempo começando do ZERO (porque carregamos como um subclip)
        t_start = word_data['start'] - start_time
        
        # Para evitar que palavras fiquem "uma em cima da outra", force a duração a terminar no início da próxima palavra
        if i < len(clip_words) - 1:
            t_end = clip_words[i+1]['start'] - start_time
        else:
            t_end = word_data['end'] - start_time
            
        duration = t_end - t_start
        
        # Prevenção: Palavras faladas muito rapidamente ou com erro
        if duration <= 0:
            duration = 0.2
            
        txt_clip = make_text_clip(text, duration, video.w)
        # 1. Posiciona visualmente livre do centro (mais para baixo: ex. 65% da altura)
        txt_clip = txt_clip.set_position(('center', video.h * 0.65)).set_start(t_start)
        subtitle_clips.append(txt_clip)

    print(f"✍️ {len(subtitle_clips)} frames de legenda animada gerados com sucesso...")

    # 3.5 Adicionar a Marca D'água / Call to Action (CTA) do AutoCash 2026 FIXA na tela
    cta_text = "🔗 Link na Bio: AutoCash 2026"
    cta_clip = make_text_clip(cta_text, duration=video.duration, max_width=video.w, fontsize=40, color="#00F0FF")
    # Colocar no finalzinho da tela (embaixo das legendas)
    cta_clip = cta_clip.set_position(('center', video.h * 0.85)).set_start(0)

    # 4. Queimando tudo junto no filme
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
