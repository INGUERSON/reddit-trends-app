import os
import sys
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from openai import OpenAI

# 🟢 PROFESSOR'S NOTE: Intelligence starts with proper configuration. 
# We load our secret keys from the .env file to keep our agent secure.
load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize our specialized tools
app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def deep_search_niche(niche_query, max_results=3):
    """
    🟢 PROFESSOR'S NOTE: Phase 1 - Discovery.
    We don't just guess where to look. We ask Firecrawl to search the web for the 
    most relevant and authoritative sources in the niche.
    """
    print(f"(SERP) Iniciando pesquisa profunda no nicho: {niche_query}...")
    
    try:
        # Search for top resources in the niche
        search_data = app.search(f"{niche_query} product reviews pain points forums", limit=max_results)
        
        # 🟢 PROFESSOR'S NOTE: The v2 API returns a SearchData object. 
        # We access the 'web' list within it.
        web_results = getattr(search_data, 'web', [])
        
        extracted_data = []
        
        for i, result in enumerate(web_results[:max_results]):
            url = getattr(result, 'url', None)
            if not url: continue
            
            print(f"(PAGE) Analisando fonte {i+1}: {url}")
            
            # 🟢 PROFESSOR'S NOTE: Phase 2 - Deep Extraction.
            try:
                scrape_result = app.scrape(url, formats=['markdown'])
            except Exception as e:
                print(f"[!] Erro ao extrair dados de {url}: {str(e)}")
                continue
            
            if hasattr(scrape_result, 'markdown') and scrape_result.markdown:
                extracted_data.append({
                    "url": url,
                    "content": scrape_result.markdown,
                    "title": getattr(scrape_result.metadata, 'title', 'Untitled') if hasattr(scrape_result, 'metadata') else 'Untitled'
                })
        
        return extracted_data
        
    except Exception as e:
        print(f"[❌] Erro durante a pesquisa: {str(e)}")
        return []

def analyze_findings_with_ai(niche, data_list):
    """
    🟢 PROFESSOR'S NOTE: Phase 3 - Synthesis.
    Raw data is useless without interpretation. We feed the extracted Markdown 
    to GPT-4o to find the 'Gold' (Pain Points and Sales Opportunities).
    """
    print("(AI) A Inteligência Artificial está processando as descobertas...")
    
    # Bundle the content for the LLM
    combined_content = ""
    for item in data_list:
        combined_content += f"\n--- FONTE: {item['url']} ---\n{item['content'][:3000]}\n"

    prompt = f"""
    Você é um Consultor de Estratégia de Vendas e Especialista em Market Research. 
    Analise o conteúdo abaixo sobre o nicho '{niche}' e forneça um dossiê estratégico.
    
    ESTRUTURA DO RELATÓRIO:
    1. **Resumo do Mercado**: Qual é o cenário atual desse nicho/tema?
    2. **Principais Dores/Desafios**: O que as pessoas estão buscando resolver ou reclamando?
    3. **Oportunidades Inexploradas**: Onde está o dinheiro/"ouro" que a maioria não vê?
    4. **Plano de Ação Sugerido**: Se fôssemos criar um modelo de negócio, produto ou serviço, por onde começar?
    5. **Palavras-Chave de Poder**: Termos e gírias usados pelo público que geram conexão.

    DADOS COLETADOS:
    {combined_content}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de mercado e copywriting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na análise da IA: {str(e)}"

def send_to_telegram(niche, analysis):
    """
    🟢 PROFESSOR'S NOTE: The final step of communication.
    We send the executive summary to the Telegram channel for instant visibility.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("[!] Telegram credentials not configured. Skipping notification.")
        return False
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # 🟢 PROFESSOR'S NOTE: Simplicity is robustness.
    # To avoid 400 Bad Request errors with Telegram's strict HTML/Markdown parsing,
    # we'll send the analysis as plain text but with a clear header.
    header = f"🚀 INSIGHT DE MERCADO: {niche.upper()}\n\n"
    message = (header + analysis)[:4000]
    
    payload = {
        "chat_id": chat_id,
        "text": message
        # No parse_mode to ensure it always delivers
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("(TG) Insights enviados com sucesso para o Telegram!")
        return True
    except Exception as e:
        print(f"(TG) Falha ao enviar para Telegram: {e}")
        return False

def save_dossier(niche, analysis):
    """
    🟢 PROFESSOR'S NOTE: Phase 4 - Archiving.
    A professional agent always leaves a trace. We save the final dossier in the .tmp folder.
    """
    tmp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tmp_dir}/dossie_{niche.replace(' ', '_').lower()}_{timestamp}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Dossiê de Pesquisa Profunda: {niche}\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("---\n\n")
        f.write(analysis)
        
    return filename

def main():
    # Niche default for our test
    niche = "Produtos de beleza e estética feminina"
    
    if len(sys.argv) > 1:
        niche = " ".join(sys.argv[1:])
        
    start_time = time.time()
    
    # 🏃 Loop de Execução do Agente
    raw_data = deep_search_niche(niche)
    
    if raw_data:
        analysis = analyze_findings_with_ai(niche, raw_data)
        dossier_path = save_dossier(niche, analysis)
        
        # 🟢 PROFESSOR'S NOTE: Integration! 
        # After saving the local file, we push the insights to the Telegram channel.
        send_to_telegram(niche, analysis)
        
        end_time = time.time()
        duration = int(end_time - start_time)
        
        print("\n" + "="*50)
        print(f"DONE: PESQUISA CONCLUÍDA EM {duration} SEGUNDOS")
        print(f"FILE: Dossiê salvo em: {dossier_path}")
        print("="*50)
        print(f"\nRESUMO DA ANÁLISE:\n{analysis[:500]}...")
    else:
        print("[-] Não foi possível extrair dados suficientes para análise.")

if __name__ == "__main__":
    main()
