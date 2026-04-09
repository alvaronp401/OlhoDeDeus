import subprocess
import os
from datetime import datetime

def preparar_ambiente_alvo(dominio):
    """Cria a estrutura de pastas para organização absurda"""
    base_path = f"./targets/{dominio}"
    subpastas = ["scans", "vulnerabilities", "loot", "logs"]
    for pasta in subpastas:
        os.makedirs(f"{base_path}/{pasta}", exist_ok=True)
    return base_path

def executar_comando_kali(comando, dominio, usar_proxy=True):
    path_alvo = preparar_ambiente_alvo(dominio)
    prefixo = "proxychains4 -q " if usar_proxy else ""
    comando_final = f"{prefixo}{comando}"
    
    print(f"[NEXUS_EXEC] Alvo: {dominio} | Comando: {comando_final}")
    
    try:
        processo = subprocess.run(comando_final, shell=True, capture_output=True, text=True)
        
        # Salva o log histórico da execução
        log_file = f"{path_alvo}/logs/history.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"\n[{timestamp}] CMD: {comando_final}\nOUT: {processo.stdout}\nERR: {processo.stderr}\n")
            
        return {
            "stdout": processo.stdout,
            "stderr": processo.stderr,
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
