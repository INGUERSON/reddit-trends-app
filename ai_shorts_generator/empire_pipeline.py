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
          print("AUTO-CASH EMPIRE: INICIANDO NOVO CICLO")
          print("="*54 + "\n")

    niches = [
                  {"name": "marketing digital", "lang": "pt"},
                  {"name": "renda extra e sucesso financeiro", "lang": "pt"},
                  {"name": "tecnologia e inteligencia artificial", "lang": "pt"},
                  {"name": "empreendedorismo e negocios", "lang": "pt"},
                  {"name": "podcast de cortes milionarios", "lang": "pt"},
    ]

    # Shuffle para diversificar
    random.shuffle(niches)

    found_any = False
    for niche in niches:
                  print(f"BUSCANDO VIRAL PARA NICHE: {niche['name'].upper()}")

        # 1. Cacar video viral
                  video_url = hunt_viral_videos(niche['name'], lang=niche['lang'])

        if video_url:
                          print(f"VIDEO VIRAL ENCONTRADO: {video_url}")

            # 2. Gerar o clipe usando a factory do main.py
                          output_videos = factory_main(video_url)

            if output_videos:
                                  found_any = True
                                  print(f"CLIPES GERADOS: {len(output_videos)}")

                # 3. Postar no Instagram
                                  for video_path in output_videos:
                                                            success = auto_publish(video_path, caption=f"Viralizando o nicho de {niche['name']}! #viral #shorts #ai")
                                                            if success:
                                                                                          print(f"POSTADO COM SUCESSO: {video_path}")
            else:
                        print(f"FALHA AO POSTAR: {video_path}")

                                  # Pausa entre postagens se houver mais de uma
                                  time.sleep(30)

            # Sair do loop de nichos apos encontrar um (um ciclo = um viral processado)
            break
else:
            print(f"Nada de novo em {niche['name']}. Mudando de nicho...")
            time.sleep(5)

    return found_any

def run_single_cycle():
          """Usado pelo GitHub Actions para rodar apenas uma vez"""
    load_dotenv()
    success = execute_full_cycle()
    if not success:
                  print("Ciclo finalizado: Nenhum video viral novo encontrado.")
        sys.exit(0)

if __name__ == "__main__":
          # Se rodar localmente sem argumentos, roda em loop eterno
          print("INICIANDO EMPIRE PIPELINE EM MODO LOOP...")
    while True:
                  execute_full_cycle()
        wait_time = random.randint(3600, 7200) # Espera entre 1 e 2 horas
        next_run = datetime.now() + timedelta(seconds=wait_time)
        print(f"Ciclo finalizado. Proxima execucao em: {next_run.strftime('%H:%M:%S')}")
        time.sleep(wait_time)
