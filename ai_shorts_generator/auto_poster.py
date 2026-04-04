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
        comment_label = "COMMENT:"
        comment_fallback = "Comment I WANT and I will send the tool to your DM!"
    else:
        target_lang = "Portuguese"
        cta = 'Acesse agora o Link no Meu Perfil!'
        caption_label = "LEGENDA:"
        comment_label = "COMENTARIO:"
        comment_fallback = "Comenta EU QUERO que te mando a ferramenta no direct!"

    prompt = f"""
    Gere uma legenda em {target_lang} para um video curto do nicho de: '{niche}'.
    A legenda deve ser altamente persuasiva e terminar com: "{cta}"
    Inclua de 5 a 8 hashtags virais.
    Gere o 1o Comentario (que vai ser pinado).
    Formato OBRIGATORIO EXATO:
    {caption_label} [sua legenda aqui]
    {comment_label} [seu comentario aqui]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )
        content = response.choices[0].message.content.replace("CAPTION:", "LEGENDA:").replace("COMMENT:", "COMENTARIO:")
        caption = content.split("COMENTARIO:")[0].replace("LEGENDA:", "").strip()
        comment = content.split("COMENTARIO:")[1].strip() if "COMENTARIO:" in content else comment_fallback
        return caption, comment
    except Exception as e:
        print(f"Erro ao gerar copy: {e}")
        return "Dica incrivel! Link na Bio.\n\n#sucesso #dica #marketing", "Comenta se gostou!"

def post_to_instagram(video_path, caption, comment):
    username = get_secure_env("IG_USERNAME")
    password = get_secure_env("IG_PASSWORD")

    if not username or not password:
        print("Skiping Instagram: Credenciais nao configuradas no .env")
        return False

    try:
        if username.startswith("@"):
            username = username[1:]

        print(f"Autenticando no Instagram como: {username}...")
        cl = Client()

        session_file = "instagram_session.json"
        if os.path.exists(session_file):
            print("Carregando sessao existente...")
            try:
                cl.load_settings(session_file)
                cl.get_timeline_feed()
                print("Sessao valida carregada.")
            except Exception:
                print("Sessao expirada. Realizando login completo...")
                cl.login(username, password)
                cl.dump_settings(session_file)
        else:
            cl.login(username, password)
            cl.dump_settings(session_file)
            print("Nova sessao salva.")

        print(f"Fazendo Upload do Reels ({os.path.basename(video_path)})...")
        media = cl.clip_upload(
            video_path,
            caption,
            extra_data={'custom_accessibility_caption': caption, 'like_and_view_counts_disabled': False}
        )

        print(f"Reels Postado com Sucesso! Media ID: {media.id}")

        if comment:
            print(f"Comentando no proprio video: {comment}")
            time.sleep(5)
            cl.media_comment(media.id, comment)
            print("Comentario postado!")

        return True
    except Exception as e:
        print(f"Erro ao postar no Instagram: {e}")
        if os.path.exists("instagram_session.json"):
            os.remove("instagram_session.json")
        return False

def auto_publish(video_paths, niche, lang="pt"):
    print("\n" + "="*50)
    print("AGENTE PUBLICADOR INICIADO")
    print("="*50)

    if not video_paths:
        print("Nenhum video recebido para publicar.")
        return

    for video_path in video_paths:
        print(f"Preparando video: {video_path}")
        if not os.path.exists(video_path):
            print(f"Arquivo nao encontrado: {video_path}")
            continue

        caption, comment = generate_social_copy(niche, lang=lang)
        print("LEGENDA GERADA:")
        print(caption)
        print("COMENTARIO GERADO:")
        print(comment)

        post_to_instagram(video_path, caption, comment)

    print("PROCESSO DE PUBLICACAO CONCLUIDO!")
