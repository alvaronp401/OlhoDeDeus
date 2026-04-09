# core/tools/check_anonymity.py
import subprocess

def verificar_anonimato():
    """Verifica o IP real vs IP via proxychains4 para garantir anonimato."""
    print("\n" + "="*60)
    print("[NEXUS_SECURITY] Verificando integridade do anonimato...")
    print("="*60)
    
    try:
        # 1. Tenta pegar IP direto (se falhar, o sistema está blindado)
        direct_ip = "BLOCK"
        try:
            direct_ip = subprocess.run(
                ["curl", "-s", "--connect-timeout", "5", "https://ifconfig.me"], 
                capture_output=True, text=True
            ).stdout.strip()
        except:
            pass
        
        # 2. Tenta pegar IP via Proxychains4
        proxy_ip = "FAILED"
        try:
            proxy_ip = subprocess.run(
                ["proxychains4", "-q", "curl", "-s", "--connect-timeout", "10", "https://ifconfig.me"], 
                capture_output=True, text=True
            ).stdout.strip()
        except Exception as e:
            proxy_ip = f"ERROR: {str(e)}"

        print(f"  [DIRECT_IP] {direct_ip}")
        print(f"  [PROXY_IP]  {proxy_ip}")
        
        status = "PROTECTED ✓" if proxy_ip != direct_ip and proxy_ip != "FAILED" else "UNSAFE ✗"
        print(f"\n[STATUS] {status}")
        print("="*60 + "\n")
        
        return {
            "direct": direct_ip,
            "proxy": proxy_ip,
            "status": status
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    verificar_anonimato()
