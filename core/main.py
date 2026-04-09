# core/main.py
import os
import json
from google import genai
from google.genai import types
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Cliente com v1 estável (que encontrou o modelo com sucesso)
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(api_version='v1')
)

chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
collection = chroma_client.get_or_create_collection(name="nexus_memory")

# Instrução do sistema - será injetada diretamente no prompt
NEXUS_INSTRUCTION = """
Você é o NEXUS, o motor do 'Olho de Deus'.
Sua metodologia é baseada no PTES (Penetration Testing Execution Standard).

Responda APENAS com um JSON válido neste formato exato, sem markdown, sem explicações extras:
{"fase": "RECON", "estrategia": "sua análise", "comando": "comando para kali", "ferramenta": "nome da ferramenta", "alerta": "alertas importantes"}

Os valores possíveis para fase são: RECON, ENUM, VULN_DEV, EXPLOIT, POST
"""

class Nexus:
    def __init__(self):
        self.model_id = "gemini-1.5-flash"
        print(f"[NEXUS_CORE] Motor inicializado: {self.model_id} (API v1)")

    def pensar_e_agir(self, user_input, dominio_alvo="desconhecido"):
        # Consulta memória sobre o alvo
        try:
            memoria = collection.query(query_texts=[user_input, dominio_alvo], n_results=3)
            contexto = f"CONTEXTO DE MEMÓRIA: {memoria['documents']}\nALVO ATUAL: {dominio_alvo}"
        except:
            contexto = f"ALVO ATUAL: {dominio_alvo}"

        # Monta o prompt completo com a instrução embutida
        full_prompt = f"{NEXUS_INSTRUCTION}\n{contexto}\nENTRADA DO OPERADOR: {user_input}"

        try:
            # Chamada limpa - sem system_instruction, sem response_mime_type
            response = client.models.generate_content(
                model=self.model_id,
                contents=full_prompt
            )

            # Limpa possíveis marcadores de markdown do texto
            raw = response.text.strip()
            raw = raw.replace('```json', '').replace('```', '').strip()
            return json.loads(raw)

        except Exception as e:
            return {
                "fase": "ERRO_SISTEMA",
                "estrategia": f"Erro Nexus: {str(e)}",
                "comando": "N/A",
                "ferramenta": "N/A",
                "alerta": "Falha na Camada Neural",
                "error": True
            }

nexus = Nexus()
