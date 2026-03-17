import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from instagrapi import Client

from secure_vault import decrypt_value

load_dotenv()

# Segurança AES-256: Descriptografando chaves
def get_secure_env(key):
    val = os.getenv(key)
    if val and val.startswith("gAAAA"):
        return decrypt_value(val)
    return val

client = OpenAI(api_key=get_secure_env("OPENAI_API_KEY"))

def generate_social_copy(niche, lang="pt"):
    print(f"🧠 Gerando Copywave ({lang.upper()}) (Legenda e Comentários) via OpenAI...")
    
    if lang == "en":
        target_lang = "English"
        cta = f'🔗 Access now the Link in My Profile or here: {os.getenv("STRIPE_PRODUCT_URL", "your-link-here")} to get your copy!'
        prompt_instruction = "You are a professional social media expert specializing in organic virality on TikTok and Instagram Reels."
        format_instruction = "MANDATORY EXACT output format (no additional markdowns):"
        caption_label = "CAPTION:"
        comment_label = "COMMENT:"
        comment_fallback = "Comment 'I WANT' and I will send the tool to your DM!"
    else:
        target_lang = "Portuguese"
        cta = f'🔗 Acesse agora o Link no Meu Perfil ou aqui: {os.getenv("STRIPE_PRODUCT_URL", "seu-link-aqui")} para garantir sua cópia!'
        prompt_instruction = "Você é um social media profissional especializado em viralização orgânica no TikTok e Instagram Reels."
        format_instruction = "Formato de saída OBRIGATÓRIO EXATO (sem markdowns adicionais):"
        caption_label = "LEGENDA:"
        comment_label = "COMENTÁRIO:"
        comment_fallback = "Comenta 'EU QUERO' que te mando a ferramenta no direct!"

    prompt = f"""
    {prompt_instruction}
    Gere uma legenda em {target_lang} para um vídeo curto do nicho de: '{niche}'.
    
    A legenda deve ser altamente persuasiva, chamar a atenção nos primeiros 3 segundos de leitura e terminar obrigatoriamente com o Call to Action: "{cta}"
    
    Também inclua de 5 a 8 hashtags super virais.
    E gere o 1º Comentário (que vai ser pinado) incitando as pessoas a comentarem "EU QUERO" (ou equivalente em {target_lang}).
    
    {format_instruction}
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
        processed_content = response.choices[0].message.content.replace("CAPTION:", "LEGENDA:").replace("COMMENT:", "COMENTÁRIO:")
        
        caption = processed_content.split("COMENTÁRIO:")[0].replace("LEGENDA:", "").strip()
        comment = processed_content.split("COMENTÁRIO:")[1].strip() if "COMENTÁRIO:" in processed_content else comment_fallback
        
        return caption, comment
    except Exception as e:
        print(f"❌ Erro ao gerar copy: {e}")
        return "🔥 Dica incrível para você multiplicar seus resultados! Link na Bio.\n\n#sucesso #dica #marketing", "Comenta 🔥 se gostou!"

def post_to_instagram(video_path, caption, comment):
    username = get_secure_env("IG_USERNAME")
    password = get_secure_env("IG_PASSWORD")
    
    if not username or not password:
        print("⏭️ Skiping Instagram: Credenciais (IG_USERNAME / IG_PASSWORD) não configuradas no .env")
        return False
        
    try:
        print(f"📱 Autenticando no Instagram como: {username}...")
        cl = Client()
        # Para evitar blocks ao logar repetidamente em IPs diferentes:
        # cl.delay_range = [1, 3] # define delays de humano
        cl.login(username, password)
        
        print(f"🚀 Fazendo Upload do Reels ({os.path.basename(video_path)})... Isso pode demorar.")
        media = cl.clip_upload(
            video_path, 
            caption,
            extra_data={'custom_accessibility_caption': caption, 'like_and_view_counts_disabled': False}
        )
        
        print(f"✅ Reels Postado com Sucesso! Media ID: {media.id}")
        
        if comment:
            print(f"💬 Comentando no próprio vídeo: {comment}")
            time.sleep(5) # Pede um tempo para interagir como humano
            cl.media_comment(media.id, comment)
            print("✅ Comentário postado!")
            
        return True
    except Exception as e:
        print(f"❌ Erro ao postar no Instagram: {e}")
        return False

def post_to_tiktok(video_path, caption):
    print("⏳ TikTok Automação: Atualmente requer setup manual de sessão de cookies via `playwright`.")
    print("Para postar no TikTok de forma 100% segura sem levar shadowban (punição por BOT), o sistema fará apenas o Upload Manual nesta versão, ou podemos usar APIs oficiais posteriormente.")
    return False

def auto_publish(video_paths, niche, lang="pt"):
    print("\n" + "="*50)
    print("📤 AGENTE PUBLICADOR INICIADO")
    print("="*50)
    
    if not video_paths:
        print("❌ Nenhum vídeo recebido para publicar.")
        return
        
    for video_path in video_paths:
        print(f"\n📦 Preparando vídeo: {video_path}")
        if not os.path.exists(video_path):
            print(f"❌ Arquivo não encontrado: {video_path}")
            continue
            
        caption, comment = generate_social_copy(niche, lang=lang)
        
        print("\n📝 LEGENDA GERADA:")
        print(caption)
        print("\n💬 COMENTÁRIO GERADO:")
        print(comment)
        print("-" * 30)
        
        post_to_instagram(video_path, caption, comment)
        # post_to_tiktok(video_path, caption) # Desativado por padrao pela segurança da conta
        
    print("\n✅ PROCESSO DE PUBLICAÇÃO CONCLUÍDO!")

if __name__ == "__main__":
    test_vid = "output/Clip_01.mp4"
    if os.path.exists(test_vid):
        auto_publish([test_vid], "Inteligência Artificial")
    else:
        print(f"Crie um vídeo em {test_vid} para testar diretamente.")
