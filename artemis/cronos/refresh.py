import schedule
import time
import subprocess
import logging

logging.basicConfig(
    filename='atualizacao_ia.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def atualizar_base():
    logging.info("Iniciando atualização da base IA...")
    try:
        result = subprocess.run(
            ['python', 'carregar_do_banco.py'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logging.info("Base atualizada com sucesso")
        else:
            logging.error(f"Erro na atualização: {result.stderr}")
    except Exception as e:
        logging.error(f"Exceção: {e}")

# Agendar para rodar todo dia às 02:00
schedule.every().day.at("02:00").do(atualizar_base)

if __name__ == "__main__":
    logging.info("Serviço de atualização iniciado")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar a cada minuto