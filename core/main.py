# core/main.py
import os
import json
import time
from google import genai
from google.genai import types
import chromadb
from dotenv import load_dotenv
from .tools.executor import executar_comando_kali
from .tools.nuclei_scanner import rodar_nuclei
from .database import db

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
collection = chroma_client.get_or_create_collection(name="nexus_memory")

NEXUS_INSTRUCTION = """
Você é o NEXUS, o motor de pentest autônomo 'Olho de Deus'.
Sua inteligência é baseada no OWASP Top 10 e PTES.

OBJETIVOS ESPECÍFICOS:
1. Identificar Vulnerabilidades de Inclusão (LFI, RFI, LCI) e Injeção.
2. Analisar Endpoints expostos (DevTools, arquivos JS, env files).
3. Coletar OSINT (Emails, subdomínios, chaves de API, credenciais) e salvar como LOOT.
4. Manter o anonimato absoluto através do proxychains4.

CONTRATO JSON:
{
  "fase": "RECON | ENUM | VULN_DEV | EXPLOIT | POST",
  "estrategia": "Análise técnica",
  "comando": "Comando real para o Kali",
  "ferramenta": "Nome",
  "alerta": "Informação crítica",
  "discovery": { 
     "type": "vulnerability | loot", 
     "title": "Ex: Email encontrado / LFI detectado", 
     "severity": "CRITICAL-INFO", 
     "details": "Conteúdo extraído ou descrição da falha" 
  }
}
"""

def discover_models():
    try:
        available = [m.name for m in client.models.list()]
        preferred = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-pro"]
        return [p for p in preferred if any(p in name for name in available)] or ["gemini-1.5-flash"]
    except: return ["gemini-2.0-flash"]

class Nexus:
    def __init__(self):
        self.models = discover_models()
        self.model_id = self.models[0] if self.models else None

    def pensar_e_agir(self, user_input, dominio_alvo="desconhecido"):
        if not self.model_id: return {"error": "Engine Offline"}
        
        vulns = db.get_vulnerabilities(dominio_alvo)
        loots = db.get_loot(dominio_alvo)
        db_context = f"\n🔍 HISTÓRICO: {len(vulns)} vulns, {len(loots)} loots registrados."
        
        prompt = f"{NEXUS_INSTRUCTION}\n{db_context}\nTARGET: {dominio_alvo}\nINPUT: {user_input}"

        for model_name in self.models:
            try:
                response = client.models.generate_content(model=model_name, contents=prompt)
                raw = response.text.strip().replace('```json', '').replace('```', '').strip()
                result = json.loads(raw)
                
                if result.get("discovery") and result["discovery"]["type"] != "None":
                    disc = result["discovery"]
                    if disc["type"] == "vulnerability":
                        db.save_vulnerability(dominio_alvo, disc["title"], disc["severity"], disc["details"])
                    else:
                        db.save_loot(dominio_alvo, "OSINT", disc["details"], origin="Nexus Neural Search")
                
                return result
            except: continue
        return {"error": "IA falhou"}

    def executar(self, comando, dominio_alvo, usar_proxy=True):
        if "nuclei" in comando.lower():
            count = rodar_nuclei(dominio_alvo)
            return {"stdout": f"Scan Nuclei: {count} findings.", "exit_code": 0, "status": "success"}
        
        result = executar_comando_kali(comando, dominio_alvo, usar_proxy)
        db.log_execution(dominio_alvo, comando, result.get("stdout", ""), result.get("exit_code", -1))
        
        # Inteligência Pós-Execução: Tenta identificar SO/Tech se houver output
        if result.get("stdout"):
            self.identificar_infraestrutura(dominio_alvo, result["stdout"])
            
        return result

    def identificar_infraestrutura(self, target, context):
        """Extrai SO e Tech Stack do contexto de execução via IA."""
        if len(context) < 50: return
        prompt = f"Analise este output de ferramenta de segurança e identifique o Sistema Operacional (Windows/Linux) e a Stack Tecnológica (PHP/ASP/Java/Python/Node) do alvo {target}. Responda APENAS um JSON: {{\"os_family\": \"...\", \"tech_stack\": \"...\"}}. Output: {context[:2000]}"
        try:
            res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt).text
            data = json.loads(res.strip().replace('```json', '').replace('```', '').strip())
            db.update_target_intel(target, os_family=data.get("os_family"), tech_stack=data.get("tech_stack"))
        except: pass

nexus = Nexus()
