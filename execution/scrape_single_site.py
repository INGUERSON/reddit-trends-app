import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

# Load variables (FIRECRAWL_API_KEY)
load_dotenv()

def scrape_url(target_url: str):
    print(f"[+] Iniciando scrape para: {target_url}")
    
    # Init Firecrawl Application Instance
    # Uses FIRECRAWL_API_KEY environment variable. 
    # Must exist in .env file or environment mapping
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key or api_key == "SUA_CHAVE_AQUI":
        print("[-] ERRO: Chave FIRECRAWL_API_KEY não encontrada ou inválida no ambiente.")
        print("[-] Por favor, insira a chave da FireCrawl no arquivo .env")
        sys.exit(1)
        
    app = FirecrawlApp(api_key=api_key)

    try:
        # Configuration parameters for markdown scraping
        # Scrape a single URL using Firecrawl v2 interface
        result = app.scrape(target_url, formats=['markdown'])
        
        if hasattr(result, 'markdown') and result.markdown:
            markdown_content = result.markdown
            title = result.metadata.title if hasattr(result, 'metadata') and hasattr(result.metadata, 'title') and result.metadata.title else 'Sem_Titulo'
            
            # Ensure .tmp directory exists as per AGENTS.md conventions
            tmp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp")
            os.makedirs(tmp_dir, exist_ok=True)
            
            # Generate a clean filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            safe_title = safe_title.replace(" ", "_").lower()[:50]
            
            filename = f"{tmp_dir}/scraped_{safe_title}_{timestamp}.md"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n")
                f.write(f"**URL Original:** {target_url}\n")
                f.write("---\n\n")
                f.write(markdown_content)
                
            print(f"[+] Website salvo com sucesso em formato Markdown: {filename}")
            return filename
            
        else:
            print("[-] Formato markdown não retornado pela API.")
            print(result)
            return None
            
    except Exception as e:
        print(f"[-] Erro ao processar scraping: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python execution/scrape_single_site.py <URL>")
        test_url = "https://www.scrapethissite.com/pages/"
        print(f"Executando URL de teste: {test_url}")
        scrape_url(test_url)
    else:
        url = sys.argv[1]
        scrape_url(url)
