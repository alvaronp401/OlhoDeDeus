import subprocess
import json
import os
from ..database import db

def rodar_nuclei(target, templates=None):
    """
    Executa o Nuclei Scanner no alvo informado e salva resultados no SQLite.
    Usa proxychains4 para manter o anonimato.
    """
    print(f"\n[NEXUS_NUCLEI] Iniciando scan avançado em: {target}")
    
    # Se não houver templates, usa os 'tags' de tecnologia comuns
    cmd = [
        "proxychains4", "-q", "nuclei", 
        "-u", target, 
        "-json", 
        "-silent"
    ]
    
    if templates:
        cmd.extend(["-t", templates])
    
    try:
        processo = subprocess.run(cmd, capture_output=True, text=True)
        results = processo.stdout.strip().split('\n')
        
        findings_count = 0
        for line in results:
            if not line: continue
            try:
                data = json.loads(line)
                # Extrai informações relevantes
                title = data.get("info", {}).get("name", "Vulnerabilidade Detectada")
                severity = data.get("info", {}).get("severity", "INFO")
                desc = data.get("info", {}).get("description", "Sem descrição disponível.")
                matcher = data.get("matched-at", "")
                
                # Salva no banco de dados SQLite
                db.save_vulnerability(
                    target, 
                    f"[NUCLEI] {title}", 
                    severity.upper(), 
                    f"{desc}\nLocal: {matcher}"
                )
                findings_count += 1
            except:
                continue
                
        print(f"[NEXUS_NUCLEI] Scan concluído. {findings_count} vulnerabilidades encontradas.")
        return findings_count
        
    except FileNotFoundError:
        print("[NEXUS_NUCLEI] Erro: Nuclei não encontrado no sistema.")
        return -1
    except Exception as e:
        print(f"[NEXUS_NUCLEI] Erro na execução: {str(e)}")
        return -1

if __name__ == "__main__":
    # Teste rápido se chamado diretamente
    import sys
    if len(sys.argv) > 1:
        rodar_nuclei(sys.argv[1])
