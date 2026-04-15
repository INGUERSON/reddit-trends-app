import os
import sys
import random
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


def execute_full_cycle():
    # Import inside function to avoid circular import issues
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
        {"name": "Joe Rogan powerful clips", "lang": "en"},
        {"name": "Business scale and automation", "lang": "en"},
    ]

    escolha = random.choice(niches)
    nicho = escolha["name"]
    idioma = escolha["lang"]
    print(f"Nicho do Ciclo: {nicho.upper()} ({idioma})")

    result = hunt_viral_videos(nicho, max_results=5)

    if not result:
        print("Nenhum video viral encontrado para este nicho.")
        return False

    if isinstance(result, dict):
        print(f"Video: {result.get('video_url', '')[:70]}")
        print(f"Audio: {result.get('audio_url', '')[:70]}")
    else:
        print(f"Alvo Localizado: {result}")

    try:
        generated_clips = factory_main(url=result)
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
        postados = auto_publish(generated_clips, nicho, lang=idioma)
    except Exception as e:
        print(f"Erro na Publicacao: {e}")
        postados = 0
        import traceback
        traceback.print_exc()

    print("\nLimpando arquivos gerados e baixados para liberar espaco...")
    # Limpa os videos cortados APENAS SE FORAM POSTADOS
    if postados > 0:
        for video_file in generated_clips:
            try:
                if os.path.exists(video_file):
                    os.remove(video_file)
                    print(f"Deletado arquivo de output: {video_file}")
            except Exception as e:
                print(f"Erro ao deletar {video_file}: {e}")
    else:
        print("Videos de output matidos na pasta 'output/' pois a postagem falhou ou gerou erro.")

    # Limpa a pasta de downloads
    downloads_dir = "downloads"
    if os.path.exists(downloads_dir):
        for f in os.listdir(downloads_dir):
            file_path = os.path.join(downloads_dir, f)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deletado download: {f}")
            except Exception as e:
                pass

    print("\n" + "="*54)
    print("CICLO COMPLETO FINALIZADO E HD LIMPO.")
    print("="*54 + "\n")
    return True


def run_single_cycle():
    """Entry point used by GitHub Actions - runs only once."""
    load_dotenv()
    success = execute_full_cycle()
    if not success:
        print("Ciclo finalizado sem sucesso. Nenhum video processado.")
        sys.exit(0)


def run_empire_pipeline():
    """Continuous loop - for local use only."""
    while True:
        success = execute_full_cycle()
        interval_hours = 10
        if not success:
            print("Tentando novamente em 1 hora...")
            time.sleep(3600)
            continue
        next_run = datetime.now() + timedelta(hours=interval_hours)
        print(f"Proximo ciclo agendado para: {next_run.strftime('%H:%M:%S')}")
        for h in range(interval_hours, 0, -1):
            print(f"Aguardando... {h}h restantes")
            time.sleep(3600)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("ALERTA: OPENAI_API_KEY nao encontrada!")
        sys.exit(1)
    run_empire_pipeline()
