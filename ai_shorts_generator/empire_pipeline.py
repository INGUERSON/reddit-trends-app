import os
import sys
import random
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


def execute_full_cycle():
    from viral_hunter import hunt_viral_videos
    from main import main as factory_main
    from auto_poster import auto_publish

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
        {"name": "Business scale and automation", "lang": "en"},
    ]

    escolha = random.choice(niches)
    nicho = escolha["name"]
    idioma = escolha["lang"]
    print(f"Nicho do Ciclo: {nicho.upper()} ({idioma})")

    video_url = hunt_viral_videos(nicho, max_results=5)

    if not video_url:
        print("Nenhum video viral encontrado para este nicho.")
        return False

    print(f"Alvo Localizado: {video_url}")

    try:
        generated_clips = factory_main(url=video_url)
    except Exception as e:
        print(f"Erro na Fabrica de Cortes: {e}")
        import traceback
        traceback.print_exc()
        return False

    if not generated_clips:
        print("A fabrica nao gerou clipes.")
        return False

    print(f"Fabrica concluiu: {len(generated_clips)} clipes gerados!")

    try:
        auto_publish(generated_clips, nicho, lang=idioma)
    except Exception as e:
        print(f"Erro na Publicacao: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*54)
    print("CICLO COMPLETO FINALIZADO.")
    print("="*54 + "\n")
    return True


def run_single_cycle():
    load_dotenv()
    success = execute_full_cycle()
    if not success:
        print("Ciclo finalizado sem sucesso.")
        sys.exit(0)


def run_empire_pipeline():
    while True:
        success = execute_full_cycle()
        if not success:
            print("Tentando novamente em 1 hora...")
            time.sleep(3600)
            continue
        interval_hours = 10
        next_run = datetime.now() + timedelta(hours=interval_hours)
        print(f"Proximo ciclo: {next_run.strftime('%H:%M:%S')}")
        for h in range(interval_hours, 0, -1):
            print(f"Aguardando... {h}h restantes")
            time.sleep(3600)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("ALERTA: OPENAI_API_KEY nao encontrada!")
        sys.exit(1)
    run_empire_pipeline()
