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
    print(f"Iniciando cacada GLOBAL no sub-nicho: '{nicho_escolhido}' ({idioma})")

    url_viral = hunt_viral_videos(nicho_escolhido, is_profile=False, max_results=10)
    if not url_viral:
              print("Nenhum video encontrado.")
              return False

    print(f"ALIMENTANDO FABRICA DE IA COM: {url_viral}")

    try:
              generated_clips = factory_main(url=url_viral)
except Exception as e:
          print(f"Erro Critico na Fabrica de Edicao: {e}")
          return False

    if not generated_clips:
              print("A fabrica de edicao falhou.")
              return False

    print(f"Fabrica concluiu a renderizacao de {len(generated_clips)} clipes verticais!")

    try:
              auto_publish(generated_clips, nicho_escolhido, lang=idioma)
except Exception as e:
          print(f"Erro Critico durante a Publicacao: {e}")

    print("\n" + "="*54)
    print("CICLO COMPLETO FINALIZADO. IMPERIO EM EXPANSAO.")
    print("="*54 + "\n")
    return True

def run_single_cycle():
      """Usado pelo GitHub Actions para rodar apenas uma vez"""
      load_dotenv()
      success = execute_full_cycle()
      if not success:
                print("Ciclo finalizado: Nenhum video viral novo encontrado.")
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
                  print(f"Proximo post agendado para: {next_post_time.strftime('%H:%M:%S')}")
                  for hour in range(interval_hours, 0, -1):
                                print(f"Horas restantes: {hour}h")
                                time.sleep(3600)

          if __name__ == "__main__":
                if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sua_chave_aqui":
                          print("ALERTA: OPENAI_API_KEY nao encontrada no .env!")
                          sys.exit(1)
                      print("Modulo Escalonador Iniciado: Postagens a cada 10 horas.")
    run_empire_pipeline()
