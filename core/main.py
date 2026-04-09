# core/main.py
import os
import json
import time
from google import genai
from google.genai import types
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Cliente sem forçar versão de API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
collection = chroma_client.get_or_create_collection(name="nexus_memory")

NEXUS_INSTRUCTION = """
Você é o NEXUS, o motor do 'Olho de Deus'.
Sua metodologia é baseada no PTES (Penetration Testing Execution Standard).

Responda APENAS com um JSON válido neste formato exato, sem markdown, sem explicações extras:
{"fase": "RECON", "estrategia": "sua análise", "comando": "comando para kali", "ferramenta": "nome da ferramenta", "alerta": "alertas importantes"}

Os valores possíveis para fase são: RECON, ENUM, VULN_DEV, EXPLOIT, POST
"""


def discover_models():
    """Retorna lista ordenada de modelos funcionais para esta API key."""
    print("\n" + "="*60)
    print("[NEXUS_BOOT] Descobrindo modelos disponíveis...")
    print("="*60)

    available = []
    try:
        for m in client.models.list():
            available.append(m.name)
    except Exception as e:
        print(f"  [ERRO] Falha ao listar modelos: {e}")
        return []

    # Ordem de preferência: estáveis primeiro, depois experimentais
    preferred = [
        "gemini-2.0-flash",          # Estável, rápido, menos congestionado
        "gemini-2.0-flash-lite",     # Ultra leve
        "gemini-2.5-flash",          # Mais recente, pode estar congestionado
        "gemini-2.5-pro",            # Pro mais recente
        "gemini-2.0-flash-001",      # Versão específica
        "gemini-flash-latest",       # Alias
        "gemini-pro-latest",         # Alias
    ]

    # Filtra só os que existem na conta
    valid = []
    for candidate in preferred:
        if any(candidate in name for name in available):
            valid.append(candidate)
            print(f"  [OK] {candidate}")
        
    if not valid:
        # Fallback: pega qualquer modelo gemini que suporte geração
        for name in available:
            clean = name.replace("models/", "")
            if "gemini" in clean and "embedding" not in clean and "image" not in clean:
                valid.append(clean)

    print(f"\n[NEXUS_BOOT] {len(valid)} modelos candidatos encontrados")
    print("="*60 + "\n")
    return valid


class Nexus:
    def __init__(self):
        self.models = discover_models()
        self.model_id = self.models[0] if self.models else None
        if self.model_id:
            print(f"[NEXUS_CORE] Motor primário: {self.model_id}")
            print(f"[NEXUS_CORE] Backup models: {self.models[1:3]}")
        else:
            print("[NEXUS_CORE] OFFLINE - Nenhum modelo disponível")

    def _call_model(self, model_name, prompt, retries=2):
        """Tenta chamar um modelo com retry automático para 503."""
        for attempt in range(retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                error_str = str(e)
                if "503" in error_str or "UNAVAILABLE" in error_str:
                    if attempt < retries - 1:
                        wait = (attempt + 1) * 2
                        print(f"[NEXUS] {model_name} sobrecarregado, retry em {wait}s...")
                        time.sleep(wait)
                        continue
                raise e
        return None

    def pensar_e_agir(self, user_input, dominio_alvo="desconhecido"):
        if not self.models:
            return {
                "fase": "ERRO_SISTEMA",
                "estrategia": "Nenhum modelo de IA disponível.",
                "comando": "N/A",
                "ferramenta": "N/A",
                "alerta": "Motor Neural Offline",
                "error": True
            }

        # Consulta memória
        try:
            memoria = collection.query(query_texts=[user_input, dominio_alvo], n_results=3)
            contexto = f"CONTEXTO DE MEMÓRIA: {memoria['documents']}\nALVO ATUAL: {dominio_alvo}"
        except:
            contexto = f"ALVO ATUAL: {dominio_alvo}"

        full_prompt = f"{NEXUS_INSTRUCTION}\n{contexto}\nENTRADA DO OPERADOR: {user_input}"

        # Tenta cada modelo na lista até um funcionar
        for model_name in self.models:
            try:
                raw = self._call_model(model_name, full_prompt)
                if raw:
                    raw = raw.strip().replace('```json', '').replace('```', '').strip()
                    result = json.loads(raw)
                    # Se funcionou com um modelo diferente do primário, promove ele
                    if model_name != self.model_id:
                        print(f"[NEXUS] Promovendo {model_name} para motor primário")
                        self.model_id = model_name
                    return result
            except json.JSONDecodeError:
                # Modelo respondeu mas não em JSON válido - tenta extrair
                try:
                    start = raw.index('{')
                    end = raw.rindex('}') + 1
                    return json.loads(raw[start:end])
                except:
                    pass
            except Exception as e:
                print(f"[NEXUS] {model_name} falhou: {str(e)[:60]}, tentando próximo...")
                continue

        return {
            "fase": "ERRO_SISTEMA",
            "estrategia": "Todos os modelos falharam. Tente novamente em alguns segundos.",
            "comando": "N/A",
            "ferramenta": "N/A",
            "alerta": "Alta demanda nos servidores Google",
            "error": True
        }

nexus = Nexus()
