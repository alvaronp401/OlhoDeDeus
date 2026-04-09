# core/tools/executor.py
import subprocess
import os

def preparar_alvo(dominio):
    """Cria a estrutura de pastas para o alvo se não existir"""
    path = f"./targets/{dominio}"
    folders = ['logs', 'vulnerabilities', 'scans', 'loot']
    for folder in folders:
        os.makedirs(f"{path}/{folder}", exist_ok=True)
    return path

def executar_kali(comando, dominio, anonimato=True):
    path_alvo = preparar_alvo(dominio)
    
    # Prefixos para anonimato
    prefixo = "proxychains4 -q " if anonimato else ""
    
    # Se for um comando que gera arquivo (ex: nmap -oN), direcionamos para a pasta do alvo
    comando_final = f"{prefixo}{comando}"
    
    try:
        print(f"[NEXUS EXEC] Alvo: {dominio} | Comando: {comando_final}")
        result = subprocess.run(comando_final, shell=True, capture_output=True, text=True)
        
        # Salva o log da execução automaticamente
        log_path = f"{path_alvo}/logs/exec_history.log"
        with open(log_path, "a") as f:
            f.write(f"\nCMD: {comando_final}\nOUT: {result.stdout}\nERR: {result.stderr}\n{'-'*20}")
            
        return {"stdout": result.stdout, "stderr": result.stderr, "path": path_alvo}
    except Exception as e:
        return {"error": str(e)}
