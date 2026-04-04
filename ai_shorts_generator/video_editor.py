import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip
from moviepy.video.fx.all import crop

def make_text_clip(text, duration, max_width, fontsize=85, color="white"):
    width, height = max_width, int(fontsize * 4.0)
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

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
    text_h = text_bbox[3] - text_bbox[1]
    
    x_pos = (width - text_w) // 2
    y_pos = (height - text_h) // 2
    
    d.text((x_pos, y_pos), text, font=font, fill=color, stroke_width=3, stroke_fill="black")
    
    img_np = np.array(img)
    clip = ImageClip(img_np).set_duration(duration)
    return clip

def edit_and_render_clip(video_path, audio_path, start_time, end_time, words_data, output_filename):
    print(f"Renderizando trecho: {start_time}s ate {end_time}s")
    try:
        main_video = VideoFileClip(video_path)
        w, h = main_video.size
        
        target_ratio = 9/16
        current_ratio = w/h
        
        if current_ratio > target_ratio:
            new_w = h * target_ratio
            video_cropped = crop(main_video, x_center=w/2, width=new_w, height=h)
        else:
            new_h = w / target_ratio
            video_cropped = crop(main_video, y_center=h/2, width=w, height=new_h)
            
        video_cropped = video_cropped.resize(height=1920).subclip(start_time, end_time)
        final_w, final_h = video_cropped.size
        
        clip_words = [w for w in words_data if w['start'] >= start_time and w['end'] <= end_time]
        
        subtitle_clips = []
        for i, word in enumerate(clip_words):
            t_start = word['start'] - start_time
            if i < len(clip_words) - 1:
                t_end = clip_words[i+1]['start'] - start_time
            else:
                t_end = word['end'] - start_time
                
            word_text = word['word'].upper()
            txt_clip = make_text_clip(word_text, t_end - t_start, final_w - 100)
            txt_clip = txt_clip.set_start(t_start).set_position(('center', 1400))
            subtitle_clips.append(txt_clip)
            
        final_video = CompositeVideoClip([video_cropped] + subtitle_clips)
        
        final_video.write_videofile(
            output_filename,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            preset="ultrafast",
            threads=4,
            logger=None
        )
        main_video.close()
        return True
    except Exception as e:
        print(f"Erro na renderizacao: {e}")
        return False
