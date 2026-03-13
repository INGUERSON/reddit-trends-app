import os
from pytubefix import YouTube
from moviepy.editor import AudioFileClip

def download_youtube_video(url, output_path="downloads"):
    """
    Downloads a YouTube video in the MP4 quality (up to 720p/1080p) using pytubefix.
    Extracts the audio as a separate MP3 file for easy transcription.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        print(f"📥 Conectando ao YouTube via PytubeFix: {url}")
        yt = YouTube(url)
        video_id = yt.video_id
        
        # 1. Download do Video Original (Alta Qualidade)
        print("🔍 Buscando melhor resolução (1080p)...")
        video_stream = yt.streams.filter(adaptive=True, type='video', file_extension='mp4').order_by('resolution').desc().first()
        
        if not video_stream: # Fallback para 720p progressivo
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            
        if not video_stream:
            print("❌ Nenhum stream de vídeo encontrado.")
            return None, None

        print(f"📥 Baixando Vídeo Principal ({video_stream.resolution})...")
        video_filename = video_stream.download(output_path=output_path, filename=f"{video_id}_vid.mp4")

        # 2. Extraindo o Áudio para a IA (Whisper) e edição
        print(f"🎵 Baixando Áudio para a IA (Whisper) e edição...")
        audio_stream = yt.streams.get_audio_only()
        audio_filename = audio_stream.download(output_path=output_path, filename=f"{video_id}_aud.mp4")
        
        # Carrega o áudio e salva como mp3 para compatibilidade garantida com Whisper
        final_audio_filename = os.path.join(output_path, f"{video_id}_audio.mp3")
        clip = AudioFileClip(audio_filename)
        clip.write_audiofile(final_audio_filename, logger=None)
        clip.close()
        
        # Limpar o audio original
        try:
            os.remove(audio_filename)
        except:
            pass

        print("✅ Download em Alta Qualidade concluído!")
        return video_filename, final_audio_filename

    except Exception as e:
        print(f"❌ Erro ao baixar o vídeo: {e}")
        return None, None

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=M7FIvfx5J10" # Short sample video
    v_path, a_path = download_youtube_video(test_url)
    print(f"Vídeo salvo em: {v_path}")
    print(f"Áudio salvo em: {a_path}")
