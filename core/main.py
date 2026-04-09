# core/main.py
import os
import json
from google import genai
from google.genai import types
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Configuração de Versão de API: Forçamos a 'v1' estável
http_options = types.HttpOptions(api_version='v1')
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=http_options
)

chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
collection = chroma_client.get_or_create_collection(name="nexus_memory")

class Nexus:
    def __init__(self):
        self.instruction = """
        Você é o NEXUS, o motor do 'Olho de Deus'.
        Sua metodologia é baseada no PTES (Penetration Testing Execution Standard).
        
        Você deve SEMPRE retornar um JSON que siga este contrato:
        {
          "fase": "RECON | ENUM | VULN_DEV | EXPLOIT | POST",
          "estrategia": "Sua análise detalhada",
          "comando": "O comando exato para o Kali",
          "ferramenta": "nmap, ffuf, sqlmap, katana...",
          "alerta": "Algo crítico encontrado?"
        }
        """
        self.model_id = self.resolve_best_model()

    def resolve_best_model(self):
        """Testa modelos em ordem de preferência até encontrar um funcional na conta."""
        print("\n[NEXUS_BOOT] Iniciando Sequência de Resolução de Modelo...")
        candidates = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
        
        for model_name in candidates:
            try:
                print(f"[NEXUS_BOOT] Testando integridade: {model_name} (v1)...")
                client.models.generate_content(
                    model=model_name,
                    contents="health_check",
                    config=types.GenerateContentConfig(max_output_tokens=1)
                )
                print(f"[NEXUS_BOOT] SUCESSO: Engine vinculada a {model_name}\n")
                return model_name
            except Exception as e:
                print(f"[NEXUS_BOOT] FALHA em {model_name}: {str(e)[:100]}...")
        
        print("[NEXUS_BOOT] CRITICAL: Nenhum modelo resolvido. Verifique sua API Key e permissões.\n")
        return "gemini-1.5-flash" # Fallback otimista

    def pensar_e_agir(self, user_input, dominio_alvo="desconhecido"):
        # Consulta memória sobre o alvo
        try:
            memoria = collection.query(query_texts=[user_input, dominio_alvo], n_results=3)
            contexto = f"CONTEXTO DE MEMÓRIA: {memoria['documents']}\nALVO ATUAL: {dominio_alvo}"
        except:
            contexto = f"ALVO ATUAL: {dominio_alvo}"
        
        full_prompt = f"{contexto}\nENTRADA: {user_input}"
        
        try:
            response = client.models.generate_content(
                model=self.model_id,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.instruction,
                    response_mime_type="application/json",
                )
            )
            return json.loads(response.text)
        except Exception as e:
            return {
                "fase": "ERRO_SISTEMA",
                "estrategia": f"Erro na camada Nexus v1: {str(e)}",
                "comando": "N/A",
                "ferramenta": "N/A",
                "alerta": "Falha na Camada Neural Estável",
                "error": True
            }

nexus = Nexus()
