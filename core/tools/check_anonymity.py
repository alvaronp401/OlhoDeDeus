# core/tools/check_anonymity.py
import subprocess
import requests

def verificar_anonimato_fast():
    """Versão otimizada para o Dashboard."""
    try:
        # Tenta pegar IP via Proxychains4
        # Usamos timeout baixo para não travar a UI
        try:
            res = subprocess.run(
                ["proxychains4", "-q", "curl", "-s", "--connect-timeout", "2", "https://ifconfig.me"], 
                capture_output=True, text=True
            )
            proxy_ip = res.stdout.strip()
        except:
            proxy_ip = "CONNECTION_ERROR"

        # Pega IP direto (sem proxy) para comparar
        try:
            direct_ip = requests.get("https://ifconfig.me", timeout=2).text.strip()
        except:
            direct_ip = "HIDDEN"

        is_safe = proxy_ip != direct_ip and proxy_ip != "CONNECTION_ERROR"
        
        return {
            "proxy_ip": proxy_ip,
            "direct_ip": direct_ip,
            "status": "PROTECTED" if is_safe else "UNSAFE",
            "provider": "Tor Network" if is_safe else "Clearweb"
        }
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    print(verificar_anonimato_fast())
