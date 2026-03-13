import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "script:trend_analyzer:v1.0")

if not OPENAI_API_KEY:
    print("Erro: OPENAI_API_KEY não encontrada no .env")
    exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

# Nossos alvos de infiltração
SUBREDDITS = ['investimentos', 'Empreendedorismo', 'farialimabets']
# Termos que indicam dor/necessidade
PAIN_KEYWORDS = ['desempregado', 'renda extra', 'dívida', 'cansado', 'oportunidade', 'ideia', 'dinheiro rápido', 'estou perdido', 'aguento mais']

# Link do nosso Funil
FUNNEL_LINK = "https://INGUERSON.github.io/reddit-trends-app/"

def send_to_telegram(message):
    """Envia os leads quentes e textos gerados direto pro Telegram do mestre"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message[:4000],
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, json=payload)
    except:
        pass

def fetch_recent_posts(subreddit, limit=50):
    """Pega os posts recentes via JSON (sem precisar de login/API Key do Reddit)"""
    print(f"[*] Patrulhando r/{subreddit}...")
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    headers = {'User-Agent': REDDIT_USER_AGENT}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for child in data.get('data', {}).get('children', []):
            post = child.get('data', {})
            posts.append({
                'id': post.get('id'),
                'title': post.get('title', ''),
                'selftext': post.get('selftext', ''),
                'url': "https://www.reddit.com" + post.get('permalink', ''),
                'created_utc': post.get('created_utc', 0)
            })
        return posts
    except Exception as e:
        print(f"[!] Erro ao varrer r/{subreddit}: {e}")
        return []

def filter_hot_leads(posts):
    """Filtra apenas os posts que demonstram dor/necessidade de renda"""
    hot_leads = []
    for post in posts:
        content = (post['title'] + " " + post['selftext']).lower()
        # Se qualquer uma das palavras-chave estiver no texto
        if any(keyword in content for keyword in PAIN_KEYWORDS):
            hot_leads.append(post)
    return hot_leads

def generate_stealth_comment(post_title, post_text):
    """Usa IA para criar um comentário que pareça orgânico, natural e que converta"""
    prompt = f"""
    Você é um usuário casual do Reddit do Brasil. Você viu este post de alguém precisando de dinheiro/renda extra:
    
    TÍTULO: {post_title}
    TEXTO: {post_text[:500]}
    
    Escreva um comentário (curto, de 2 a 4 frases) respondendo a essa pessoa de forma amigável e empática. 
    NADA DE PARECER UM VENDEDOR. Fale meio informal (pode usar gírias leves como "cara", "mano", "sei como é", etc).
    No final do comentário, sugira sutilmente que você descobriu um sistema de automação para renda extra que funciona sem comprar curso de guru, e indique este link: {FUNNEL_LINK}
    
    Seja extremamente sutil e natural. O objetivo é que pareça uma ajuda de amigo, não um anúncio (Stealth Mode).
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um usuário de internet comum tentando ajudar outra pessoa de forma disfarçada."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro na IA: {e}"

def main():
    print("="*50)
    print("🕵️ INICIANDO OPERAÇÃO STEALTH (REDDIT INFILTRATION)")
    print("="*50)
    
    total_leads = 0
    message_batch = "🎯 <b>RELATÓRIO DE INFILTRAÇÃO (STEALTH)</b>\n\nA IA encontrou as seguintes oportunidades de vendas (Leads Quentes) chorando por renda extra no Reddit. Copie e cole os comentários sugeridos para atraí-los para o seu funil!\n\n"
    
    for sub in SUBREDDITS:
        posts = fetch_recent_posts(sub)
        leads = filter_hot_leads(posts)
        
        if leads:
            print(f" > Encontrados {len(leads)} leads no r/{sub}")
            for lead in leads[:3]:  # Limita a 3 por sub para não estourar a API/Telegram
                total_leads += 1
                print(f"   - Analisando dor do lead: {lead['title'][:40]}...")
                
                comment = generate_stealth_comment(lead['title'], lead['selftext'])
                
                message_batch += f"📌 <b>Subreddit:</b> r/{sub}\n"
                message_batch += f"👤 <b>Post Original:</b> <a href='{lead['url']}'>Link aqui</a>\n"
                message_batch += f"💬 <b>Sua Resposta (Copiar/Colar):</b>\n<code>{comment}</code>\n\n"
                message_batch += "----------\n\n"
        else:
            print(f" > Nenhum lead quente encontrado no r/{sub} agora.")
            
    if total_leads > 0:
        print(f"\n✅ {total_leads} Comentários de Infiltração Gerados! Enviando para o Telegram...")
        send_to_telegram(message_batch)
    else:
        print("\n⏳ Sem vítimas no radar no momento. A máquina tentará novamente depois.")

if __name__ == "__main__":
    main()
