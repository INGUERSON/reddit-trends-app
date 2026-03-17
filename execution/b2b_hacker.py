import os
import requests
import json
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from openai import OpenAI

load_dotenv()
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not FIRECRAWL_API_KEY or not OPENAI_API_KEY:
    print("Erro: Chaves de API da OpenAI ou Firecrawl não encontradas no .env!")
    exit(1)

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# ==========================================
# 🎯 CONFIGURAÇÃO DO ALVO B2B
# ==========================================
NICHE = "Clínicas de Estética"
CITY = "Paraíba"
MAX_RESULTS = 3

FUNNEL_LINK = "https://INGUERSON.github.io/reddit-trends-app/"

def send_to_telegram(message):
    """Envia o dossiê de empresas direto para o Telegram do mestre"""
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
    except Exception as e:
        print(f"(TG) Falha no Telegram: {e}")

def find_businesses(niche, city, limit):
    print(f"[*] Investigando negócios: {niche} em {city}...")
    # Excluímos instagram e facebook pois o Firecrawl bloqueia a extração destes domínios B2C
    query = f"{niche} {city} site profissional contato -site:instagram.com -site:facebook.com"
    
    try:
        search_data = app.search(query, limit=limit)
        web_results = getattr(search_data, 'web', [])
        
        leads = []
        for i, result in enumerate(web_results[:limit]):
            url = getattr(result, 'url', None)
            if not url:
                continue 
                
            print(f" > Extraindo dados do site: {url}")
            try:
                # Usa o poder profundo do Firecrawl para ler o site inteiro (Markdown)
                scrape_result = app.scrape(url, formats=['markdown'])
                if hasattr(scrape_result, 'markdown') and scrape_result.markdown:
                    leads.append({
                        "url": url,
                        "content": scrape_result.markdown[:6000], # Mandamos os primeiros 6000 chars pra IA 
                        "title": getattr(scrape_result.metadata, 'title', 'Untitled') if hasattr(scrape_result, 'metadata') else 'Untitled'
                    })
            except Exception as e:
                print(f"[!] Erro ao varrer a página {url}: {e}")
                
        return leads
    except Exception as e:
        print(f"[❌] Erro crítico na busca global: {e}")
        return []

def extract_contact_info(lead_content):
    print(" > 🧠 Iniciando IA para garimpar Nome, Email e Telefone...")
    prompt = f"""
    Analise o texto extraído do site dessa empresa e encontre os contatos.
    Responda EXATAMENTE e SOMENTE neste formato JSON, sem crases de formatação:
    {{
      "empresa": "Nome da Empresa",
      "email": "email@encontrado.com ou Não encontrado",
      "telefone": "telefone com DDD ou Não encontrado"
    }}

    TEXTO DO SITE:
    {lead_content}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Erro na extração de contatos (IA): {e}")
        return {"empresa": "Desconhecida", "email": "Não", "telefone": "Não"}

def generate_cold_pitch(empresa):
    print(f" > ✍️ Criando Script Persuasivo para {empresa}...")
    prompt = f"""
    Escreva uma mensagem Curta, Persuasiva e Sofisticada de WhatsApp (ou Cold Email) para o dono(a) da {empresa}.
    
    Você é o Diretor da "AutoCash AI Automations".
    O que você está vendendo: Vimos que vocês podem estar perdendo clientes fáceis pois as pessoas mandam mensagens na madrugada ou fds e não têm agendamento imediato. Criamos a 'Assistente Linda', um chatbot 100% autônomo e inteligente para WhatsApp que qualifica e fecha vendas 24h por dia para o segmento da {empresa}.
    
    A mensagem deve parecer B2B, escrita para lucrar mais. Não seja chato e não pareça telemarketing comum. 
    Seja impactante e termine mandando acessar o seu link secreto para a demo: {FUNNEL_LINK}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except:
        return ""

def main():
    print("="*60)
    print("💼 INICIANDO OPERAÇÃO B2B HACKER (CAPTAÇÃO DE ALTO VALOR)")
    print("="*60)
    
    leads_raw = find_businesses(NICHE, CITY, MAX_RESULTS + 3) # Busca um excesso para fugir de links sociais
    
    if not leads_raw:
        print("[-] Nenhuma empresa extraída com sucesso.")
        return
        
    message_batch = f"🎯 <b>ALVOS B2B DE ALTO VALOR: {NICHE} ({CITY})</b>\n\n"
    
    for lead in leads_raw[:MAX_RESULTS]: # Pegamos os 3 melhores
        contact_info = extract_contact_info(lead["content"])
        empresa = contact_info.get("empresa", lead["title"])
        
        email = contact_info.get("email", "Não encontrado")
        telefone = contact_info.get("telefone", "Não encontrado")
        
        print(f"\n[+] EMPRESA MAPEADA: {empresa} | {email} | {telefone}")
        
        copy_vendas = generate_cold_pitch(empresa)
        
        message_batch += f"🏢 <b>Empresa:</b> {empresa}\n"
        message_batch += f"🌐 <b>Website:</b> {lead['url']}\n"
        message_batch += f"📧 <b>E-mail:</b> {email}\n"
        message_batch += f"📱 <b>WhatsApp/Tel:</b> {telefone}\n"
        message_batch += f"💬 <b>Script de Fechamento B2B:</b>\n<code>{copy_vendas}</code>\n"
        message_batch += "----------\n\n"
        
    print("\n✅ Relatório concluído! Enviando diretamente para o centro de comando (Telegram)...")
    send_to_telegram(message_batch)

if __name__ == "__main__":
    main()
