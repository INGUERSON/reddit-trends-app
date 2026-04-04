import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from instagrapi import Client
from secure_vault import decrypt_value

load_dotenv()

def get_secure_env(key):
    val = os.getenv(key)
    if val and val.startswith("gAAAA"):
        return decrypt_value(val)
    return val

client = OpenAI(api_key=get_secure_env("OPENAI_API_KEY"))

def generate_social_copy(niche, lang="pt"):
    print(f"Gerando Copy via OpenAI (lang={lang.upper()})...")
    if lang == "en":
        target_lang = "English"
        cta = 'Access now the Link in My Profile!'
        caption_label = "CAPTION:"
    else:
        target_lang = "Portuguese (Brazil)"
        cta = 'Acesse agora o Link no Meu Perfil!'
        caption_label = "LEGENDA:"

    system_prompt = f"You are a viral social media manager. Create a high-converting caption in {target_lang}."
    user_prompt = f"Create a short, catchy caption with 5 niche-relevant hashtags for a video about: {niche}. End with this CTA: {cta}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8
        )
        copy = response.choices[0].message.content
        return f"{caption_label}
\n{copy}"
    except Exception as e:
        print(f"Erro ao gerar copy: {e}")
        return f"Check out this viral {niche} video! {cta}\n\n#viral #fyp #{niche.replace(' ', '')}"

def post_to_instagram(video_path, caption):
    print(f"Preparando Postagem no Instagram: {os.path.basename(video_path)}")
    
    cl = Client()
    user = get_secure_env("IG_USERNAME")
    password = get_secure_env("IG_PASSWORD")
    
    if not user or not password:
        print("Erro: Credenciais do Instagram nao configuradas.")
        return False

    try:
        print(f"Autenticando usuario: {user}...")
        cl.login(user, password)
        
        print("Enviando Reels...")
        media = cl.clip_upload(
            video_path,
            caption=caption,
            extra_data={
                "disable_comments": False,
                "like_and_view_counts_disabled": False,
                "audio_muted": False
            }
        )
        print(f"SUCESSO! Post realizado com ID: {media.pk}")
        return True
    except Exception as e:
        print(f"Falha na postagem: {e}")
        return False
