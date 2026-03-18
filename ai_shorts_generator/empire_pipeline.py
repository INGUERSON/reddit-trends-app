import os
import sys
import random
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

from viral_hunter import hunt_viral_videos
from main import main as factory_main
from auto_poster import auto_publish

load_dotenv()

def execute_full_cycle():
    print("\n" + "="*54)
    print("🌐🌍 AUTO-CASH EMPIRE: INICIANDO NOVO CICLO 🌍🌐")
    print("======================================================\n")
    
    # 1. Escolher nicho tático (Nacional + Internacional)
    niches = [
        {"name": "marketing digital", "lang": "pt"},
        {"name": "renda extra e sucesso financeiro", "lang": "pt"},
        {"name": "tecnologia e inteligência artificial", "lang": "pt"},
        {"name": "empreendedorismo e negócios", "lang": "pt"},
        {"name": "podcast de cortes milionários", "lang": "pt"},
        # Global / International Niches
        {"name": "AI and future technology", "lang": "en"},
        {"name": "Success mindset and money", "lang": "en"},
        {"name": "Joe Rogan powerful clips", "lang": "en"},
        {"name": "Andrew Huberman health tips", "lang": "en"},
        {"name": "Business scale and automation", "lang": "en"},
        {"name": "Luxury lifestyle and jets", "lang": "en"}
    ]
    
    selected = random.choice(niches)
    nicho_escolhido = selected["name"]
    idioma = selected["lang"]
    print(f"🎯 Iniciando caçada GLOBAL no sub-nicho: '{nicho_escolhido}' ({idioma})")
    
    # 2. Caçar Vídeo Viral (Step 1)
    url_viral = hunt_viral_videos(nicho_escolhido, is_profile=False, max_results=10)
    
    if not url_viral:
        print("❌ Nenhum vídeo encontrado.")
        return False
        
    print(f"\n⚙️ ALIMENTANDO FÁBRICA DE IA COM: {url_viral}")
    
    # 3. Gerar os Cortes com a IA (Step 2)
    try:
        generated_clips = factory_main(url=url_viral)
    except Exception as e:
        print(f"❌ Erro Crítico na Fábrica de Edição: {e}")
        return False
        
    if not generated_clips:
        print("❌ A fábrica de edição falhou.")
        return False
        
    print(f"\n✅ Fábrica concluiu a renderização de {len(generated_clips)} clipes verticais!")
    
    # 4. Postar na Nuvem (Step 3)
    try:
        auto_publish(generated_clips, nicho_escolhido, lang=idioma)
    except Exception as e:
        print(f"❌ Erro Crítico durante a Publicação: {e}")
        
    print("\n======================================================")
    print("✔️ CICLO COMPLETO FINALIZADO. IMPÉRIO EM EXPANSÃO. ✔️")
    print("======================================================\n")
    return True

def run_single_cycle():
    """Usado pelo GitHub Actions para rodar apenas uma vez"""
    load_dotenv()
    success = execute_full_cycle()
    if not success:
        print("💡 Ciclo finalizado: Nenhum vídeo viral novo encontrado para este nicho no momento.")
        sys.exit(0)

def run_empire_pipeline():
    while True:
        success = execute_full_cycle()
        
        if not success:
            print("Tentando novamente em 1 hora...")
            time.sleep(3600)
            continue
        
        interval_hours = 10
        next_post_time = datetime.now() + timedelta(hours=interval_hours)
        print(f"💤 Entrando em modo de espera. Próximo post agendado para: {next_post_time.strftime('%H:%M:%S')}")
        
        # Dormir 10 horas em pedaços de 1 hora para logs
        for hour in range(interval_hours, 0, -1):
            print(f"⏳ Horas restantes para a próxima caçada: {hour}h")
            time.sleep(3600)

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sua_chave_aqui":
        print("⚠️ ALERTA: OPENAI_API_KEY não encontrada no .env!")
        sys.exit(1)
        
    print("🚀 Módulo Escalonador Iniciado: Postagens a cada 10 horas.")
    run_empire_pipeline()
