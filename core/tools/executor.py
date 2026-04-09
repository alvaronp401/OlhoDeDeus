import subprocess
import os
from datetime import datetime

def preparar_ambiente_alvo(dominio):
    """Cria a estrutura de pastas para organização dos resultados."""
    base_path = f"./targets/{dominio}"
    subpastas = ["scans", "vulnerabilities", "loot", "logs"]
    for pasta in subpastas:
        os.makedirs(f"{base_path}/{pasta}", exist_ok=True)
    return base_path

def executar_comando_kali(comando, dominio, usar_proxy=True, timeout=120):
    """Executa um comando no Kali via proxychains4 com timeout de segurança."""
    path_alvo = preparar_ambiente_alvo(dominio)
    prefixo = "proxychains4 -q " if usar_proxy else ""
    comando_final = f"{prefixo}{comando}"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[NEXUS_EXEC] [{timestamp}] Alvo: {dominio}")
    print(f"[NEXUS_EXEC] Comando: {comando_final}")
    print(f"[NEXUS_EXEC] Timeout: {timeout}s | Proxy: {'ON' if usar_proxy else 'OFF'}")
    
    try:
        processo = subprocess.run(
            comando_final, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=timeout
        )
        
        output = processo.stdout.strip()
        errors = processo.stderr.strip()
        
        # Salva o log histórico da execução
        log_file = f"{path_alvo}/logs/history.log"
        with open(log_file, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{timestamp}] CMD: {comando_final}\n")
            f.write(f"EXIT_CODE: {processo.returncode}\n")
            f.write(f"STDOUT:\n{output}\n")
            if errors:
                f.write(f"STDERR:\n{errors}\n")
            f.write(f"{'='*60}\n")
        
        # Salva output do scan em arquivo separado
        if output:
            scan_file = f"{path_alvo}/scans/{datetime.now().strftime('%H%M%S')}_{comando.split()[0]}.txt"
            with open(scan_file, "w") as f:
                f.write(output)
        
        print(f"[NEXUS_EXEC] ✓ Concluído (exit: {processo.returncode}) | {len(output)} bytes")
            
        return {
            "stdout": output[:5000],  # Limita output para não estourar o JSON
            "stderr": errors[:1000] if errors else "",
            "exit_code": processo.returncode,
            "status": "success",
            "log_path": log_file
        }
        
    except subprocess.TimeoutExpired:
        print(f"[NEXUS_EXEC] ✗ TIMEOUT após {timeout}s")
        return {
            "stdout": "",
            "stderr": f"Comando excedeu o timeout de {timeout}s",
            "exit_code": -1,
            "status": "timeout"
        }
    except Exception as e:
        print(f"[NEXUS_EXEC] ✗ ERRO: {str(e)}")
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "status": "error"
        }
