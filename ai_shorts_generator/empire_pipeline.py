import os
import sys
import random
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

from viral_hunter import hunt_viral_videos
from main import main as factory_main

load_dotenv()

def execute_full_cycle():
    print("\n" + "="*54)
    print("AUTO-CASH EMPIRE: INICIANDO NOVO CICLO")
    print("="*54 + "\n")

    niches = [
        {"name": "marketing digital", "lang": "pt"},
        {"name": "renda extra e sucesso financeiro", "lang": "pt"},
        {"name": "tecnologia e inteligencia artificial", "lang": "pt"},
        {"name": "empreendedorismo e negocios", "lang": "pt"},
        {"name": "podcast de cortes milionarios", "lang": "pt"},
    ]

    escolha = random.choice(niches)
    print(f"Nicho do Ciclo: {escolha['name'].upper()} ({escolha['lang']})")

    video_url = hunt_viral_videos(escolha['name'], max_results=5)
    
    if video_url:
        print(f"Alvo Localizado: {video_url}")
        try:
            factory_main(video_url)
            print("Ciclo de Producao de Video Finalizado.")
        except Exception as e:
            print(f"Erro na Fabrica de Cortes: {e}")
    else:
        print("Nenhum video viral encontrado para este nicho no momento.")

if __name__ == "__main__":
    execute_full_cycle()
