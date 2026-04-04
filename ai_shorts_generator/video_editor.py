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

def process_video_with_subs(video_path, clips_data, words_data, output_folder="outputs"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    generated_files = []
    
    print(f"Iniciando Renderizacao Heavy Metal: {video_path}")
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
        
    video_cropped = video_cropped.resize(height=1920)
    final_w, final_h = video_cropped.size
    
    for i, clip in enumerate(clips_data):
        start_t = clip['start_time']
        end_t = clip['end_time']
        
        print(f"Cortando Clipe {i+1}: {start_t}s ate {end_t}s")
        sub_video = video_cropped.subclip(start_t, end_t)
        
        clip_words = [w for w in words_data if w['start'] >= start_t and w['end'] <= end_t]
        
        subtitle_clips = []
        for j, word in enumerate(clip_words):
            t_start = word['start'] - start_t
            if j < len(clip_words) - 1:
                t_end = clip_words[j+1]['start'] - start_t
            else:
                t_end = word['end'] - start_t
                
            word_text = word['word'].upper()
            txt_clip = make_text_clip(word_text, t_end - t_start, final_w - 100)
            txt_clip = txt_clip.set_start(t_start).set_position(('center', 1400))
            subtitle_clips.append(txt_clip)
            
        final_clip = CompositeVideoClip([sub_video] + subtitle_clips)
        
        output_filename = os.path.join(output_folder, f"clip_{i}_{os.path.basename(video_path)}")
        print(f"Exportando: {output_filename}")
        
        final_clip.write_videofile(
            output_filename,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            preset="ultrafast",
            threads=4,
            logger=None
        )
        generated_files.append(output_filename)
        
    main_video.close()
    return generated_files
