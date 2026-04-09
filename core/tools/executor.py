import subprocess
import os
import threading
from datetime import datetime

LIVE_LOG_FILE = "/tmp/nexus_live.log"

def preparar_ambiente_alvo(dominio):
    """Cria a estrutura de pastas para organização dos resultados."""
    base_path = f"./targets/{dominio}"
    subpastas = ["scans", "vulnerabilities", "loot", "logs"]
    for pasta in subpastas:
        os.makedirs(f"{base_path}/{pasta}", exist_ok=True)
    return base_path

def stream_to_file(process, log_path):
    """Lê o stdout do processo e escreve no arquivo de log em tempo real."""
    with open(log_path, "a") as f:
        # Pega as primeiras linhas de erro se houver
        for line in process.stdout:
            f.write(line)
            f.flush()
        for line in process.stderr:
            f.write(f"[STDERR] {line}")
            f.flush()

def executar_comando_kali(comando, dominio, usar_proxy=True, timeout=120):
    """Executa um comando no Kali e captura o output de forma assíncrona para live logs."""
    path_alvo = preparar_ambiente_alvo(dominio)
    prefixo = "proxychains4 -q " if usar_proxy else ""
    comando_final = f"{prefixo}{comando}"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Limpa ou inicializa o log de live streaming
    with open(LIVE_LOG_FILE, "w") as f:
        f.write(f"--- [START] {timestamp} Alvo: {dominio} ---\n")
        f.write(f"CMD> {comando_final}\n\n")
        f.flush() # Força a escrita imediata para a UI captar

    try:
        # Popen permite que leiamos o output enquanto o processo roda
        processo = subprocess.Popen(
            comando_final,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1 # Line buffering
        )

        # Thread para ler o output sem travar a execução
        thread = threading.Thread(target=stream_to_file, args=(processo, LIVE_LOG_FILE))
        thread.start()

        # Esperamos o processo terminar (com timeout)
        try:
            # Capturamos o output final para o banco de dados
            stdout, stderr = processo.communicate(timeout=timeout)
            exit_code = processo.returncode
        except subprocess.TimeoutExpired:
            processo.kill()
            stdout, stderr = processo.communicate()
            stdout += f"\n\n[ERROR] Comando excedeu o timeout de {timeout}s"
            exit_code = -1

        # Salva o log histórico completo
        log_file = f"{path_alvo}/logs/history.log"
        with open(log_file, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{timestamp}] CMD: {comando_final}\n")
            f.write(f"STDOUT:\n{stdout}\n")
            f.write(f"{'='*60}\n")
        
        return {
            "stdout": stdout[:5000],
            "stderr": stderr[:1000] if stderr else "",
            "exit_code": exit_code,
            "status": "completed"
        }
        
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "status": "error"
        }

def get_live_logs():
    """Retorna as últimas linhas do log em tempo real."""
    if not os.path.exists(LIVE_LOG_FILE):
        return ""
    try:
        with open(LIVE_LOG_FILE, "r") as f:
            lines = f.readlines()
            return "".join(lines[-50:]) # Retorna as últimas 50 linhas
    except:
        return ""
