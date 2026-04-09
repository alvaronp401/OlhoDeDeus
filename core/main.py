# core/main.py
import os
import json
import time
from google import genai
from google.genai import types
import chromadb
from dotenv import load_dotenv
from .tools.executor import executar_comando_kali
from .database import db

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ChromaDB para memória semântica
chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
collection = chroma_client.get_or_create_collection(name="nexus_memory")

NEXUS_INSTRUCTION = """
Você é o NEXUS, o motor de pentest autônomo 'Olho de Deus'.
Sua metodologia é baseada no PTES.

REGRAS DE CONTRATO (JSON APENAS):
{
  "fase": "RECON | ENUM | VULN_DEV | EXPLOIT | POST",
  "estrategia": "Análise técnica sênior",
  "comando": "Comando real para o Kali",
  "ferramenta": "Nome da ferramenta",
  "alerta": "Algo crítico?",
  "discovery": {
    "type": "vulnerability | loot | None",
    "title": "Título se houver descoberta",
    "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO",
    "details": "Detalhes da descoberta"
  }
}

INSTRUÇÕES:
1. Analise o HISTÓRICO e os RESULTADOS ANTERIORES para não se repetir.
2. Seja incisivo: se encontrar uma porta aberta, sugira a enumeração dela imediatamente.
3. Se o resultado de um comando mostrar uma flag, senha ou vulnerabilidade, preencha o campo 'discovery'.
"""

def discover_models():
    """Descobre e valida modelos Gemini na conta."""
    available = []
    try:
        for m in client.models.list():
            available.append(m.name)
    except:
        return []

    preferred = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-1.5-flash", "gemini-pro"]
    valid = [p for p in preferred if any(p in name for name in available)]
    return valid or [name.replace("models/", "") for name in available if "gemini" in name]

class Nexus:
    def __init__(self):
        self.models = discover_models()
        self.model_id = self.models[0] if self.models else None
        self.history = []

    def _get_persistent_context(self, domain):
        """Busca dados reais do SQLite para o prompt."""
        vulns = db.get_vulnerabilities(domain)
        loot = db.get_loot(domain)
        
        context = f"\n🔍 ESTADO ATUAL DO ALVO ({domain}):\n"
        if vulns:
            context += "- Vulnerabilidades já mapeadas: " + ", ".join([v['title'] for v in vulns]) + "\n"
        if loot:
            context += f"- Loot capturado: {len(loot)} itens no cofre.\n"
        
        return context

    def pensar_e_agir(self, user_input, dominio_alvo="desconhecido"):
        if not self.model_id:
            return {"fase": "ERRO", "estrategia": "IA Offline", "error": True}

        # Contexto: SQLite (Dados Estruturados) + ChromaDB (Memória Semântica)
        db_context = self._get_persistent_context(dominio_alvo)
        try:
            memoria = collection.query(query_texts=[user_input, dominio_alvo], n_results=3)
            sem_context = f"\n🧠 MEMÓRIA SEMÂNTICA: {memoria['documents']}"
        except:
            sem_context = ""

        prompt = f"{NEXUS_INSTRUCTION}\n{db_context}{sem_context}\nALVO: {dominio_alvo}\nOPERADOR: {user_input}"

        for model_name in self.models:
            try:
                response = client.models.generate_content(model=model_name, contents=prompt)
                raw = response.text.strip().replace('```json', '').replace('```', '').strip()
                result = json.loads(raw)
                
                # Se a IA detectou algo no pensamento, salva no DB
                disc = result.get("discovery")
                if disc and disc.get("type") != "None":
                    if disc["type"] == "vulnerability":
                        db.save_vulnerability(dominio_alvo, disc["title"], disc["severity"], disc["details"])
                    elif disc["type"] == "loot":
                        db.save_loot(dominio_alvo, "GENERAL", disc["details"], origin="Nexus Thought")

                return result
            except Exception as e:
                print(f"[NEXUS] Erro com {model_name}: {str(e)}")
                continue

        return {"fase": "ERRO", "estrategia": "Falha geral dos modelos", "error": True}

    def executar(self, comando, dominio_alvo, usar_proxy=True):
        """Executa e persiste o log no SQLite."""
        result = executar_comando_kali(comando, dominio_alvo, usar_proxy)
        
        # Loga no DB para persistência de longo prazo
        db.log_execution(dominio_alvo, comando, result.get("stdout", ""), result.get("exit_code", -1))
        
        # Opcional: Analisar o output do scan para encontrar vulns automaticamente
        # (Futura implementação: passar o output pro Gemini analisar se tem algo 'interessante')
        
        return result

nexus = Nexus()
