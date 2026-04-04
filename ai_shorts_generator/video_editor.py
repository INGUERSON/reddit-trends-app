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

    if text_w > max_width - 80:
              new_fontsize = int(fontsize * ((max_width - 80) / max(text_w, 1)))
              try:
                            font = ImageFont.truetype("arialbd.ttf", new_fontsize)
                        except:
            pass
        text_bbox = d.textbbox((0, 0), text, font=font, stroke_width=5)
        text_w = text_bbox[2] - text_bbox[0]

    text_h = text_bbox[3] - text_bbox[1]
    x = (width - text_w) / 2
    y = (height - text_h) / 2 - text_bbox[1]

    d.text((x, y), text, font=font, fill=color, stroke_width=8, stroke_fill="black")
    img_array = np.array(img)
    return ImageClip(img_array).set_duration(duration)

def edit_and_render_clip(video_path, audio_path, start_time, end_time, words_data, output_filename):
      print(f"Iniciando edicao do trecho: {start_time}s ate {end_time}s...")

    try:
              video = VideoFileClip(video_path).subclip(start_time, end_time)
              audio = AudioFileClip(audio_path).subclip(start_time, end_time)
              from moviepy.audio.fx.all import audio_normalize
              audio = audio_normalize(audio)
              video = video.set_audio(audio)
except Exception as e:
          print(f"Falha ao carregar o video ou audio: {e}")
          return False

    w, h = video.size
    target_ratio = 9/16

    if w/h > target_ratio:
              new_w = int(h * target_ratio)
              video = crop(video, width=new_w, height=h, x_center=w/2, y_center=h/2)

    duration = video.duration
    segments = []
    zoom_interval = 4.0
    for i in range(int(duration / zoom_interval) + 1):
              t_start = i * zoom_interval
              t_end = min((i + 1) * zoom_interval, duration)

        if t_start >= duration:
                      break
                  seg = video.subclip(t_start, t_end)
        if i % 2 == 1:
                      seg = seg.resize(1.15)
                      seg = crop(seg, width=video.w, height=video.h, x_center=seg.w/2, y_center=seg.h/2)
                  segments.append(seg)

    from moviepy.editor import concatenate_videoclips
    video = concatenate_videoclips(segments)
    print(f"Resolucao final: {video.size} com efeitos de Zoom Dinamico aplicados.")

    clip_words = [w for w in words_data if w['start'] >= start_time and w['end'] <= end_time]
    subtitle_clips = []
    vibrant_colors = ["#FFFF00", "#32CD32", "#FFFFFF"]

    for i, word_data in enumerate(clip_words):
              raw_word = word_data['word'].strip().upper()
              if not raw_word:
                            continue
                        text = raw_word.replace('.', '').replace(',', '').replace('?', '').replace('!', '')
        t_start = word_data['start'] - start_time
        if i < len(clip_words) - 1:
                      t_end = clip_words[i+1]['start'] - start_time
else:
            t_end = word_data['end'] - start_time
        dur = max(t_end - t_start, 0.1)
        color = "#FFFFFF"
        if i % 3 == 0 or len(text) > 7:
                      color = vibrant_colors[i % 2]
                  txt_clip = make_text_clip(text, dur, video.w, color=color)
        txt_clip = txt_clip.set_position(('center', video.h * 0.70)).set_start(t_start)
        subtitle_clips.append(txt_clip)

    print(f"{len(subtitle_clips)} frames de legenda de alto impacto gerados.")

    cta_text = "AUTO CASH 2026"
    cta_clip = make_text_clip(cta_text, duration=video.duration, max_width=video.w, fontsize=35, color="#00F0FF")
    cta_clip = cta_clip.set_position(('center', video.h * 0.90)).set_opacity(0.8).set_start(0)

    final_video = CompositeVideoClip([video] + subtitle_clips + [cta_clip])
    print(f"Renderizando (ISSO PODE DEMORAR ALGUNS MINUTOS)...")

    try:
              final_video.write_videofile(
                  output_filename,
                  codec="libx264",
                  audio_codec="aac",
                  temp_audiofile=f"{output_filename}_temp.m4a",
                  remove_temp=True,
                  logger=None,
                  threads=os.cpu_count() or 4,
                  preset="ultrafast",
                  bitrate="4000k"
    )
        print(f"SUCESSO! CLIPE SALVO COMO: {output_filename}")
except Exception as e:
        print(f"Erro fatal durante a conversao do FFmpeg: {e}")

    video.close()
    final_video.close()
    return True
