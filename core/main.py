# core/main.py
import os
import json
from google import genai
from google.genai import types
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Inicializamos o cliente da nova SDK
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
collection = chroma_client.get_or_create_collection(name="nexus_memory")

class Nexus:
    def __init__(self):
        # Instruções de sistema agora são passadas na config da requisição ou do chat
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
        self.model_id = "gemini-1.5-flash"

    def pensar_e_agir(self, user_input, dominio_alvo="desconhecido"):
        # Consulta memória sobre o alvo ou tecnologias parecidas
        try:
            memoria = collection.query(query_texts=[user_input, dominio_alvo], n_results=3)
            contexto = f"CONTEXTO DE MEMÓRIA: {memoria['documents']}\nALVO ATUAL: {dominio_alvo}"
        except:
            contexto = f"ALVO ATUAL: {dominio_alvo}"
        
        full_prompt = f"{contexto}\nENTRADA: {user_input}"
        
        try:
            # Na nova SDK, o suporte a JSON é nativo e garantido por ResponseMimeType
            response = client.models.generate_content(
                model=self.model_id,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.instruction,
                    response_mime_type="application/json",
                )
            )
            
            # O retorno já vem sanitizado e pronto para ser parseado
            return json.loads(response.text)
            
        except Exception as e:
            return {
                "fase": "ERRO_SISTEMA",
                "estrategia": f"Erro na nova SDK Nexus: {str(e)}",
                "comando": "N/A",
                "ferramenta": "N/A",
                "alerta": "Falha na Camada Neural",
                "error": True
            }

nexus = Nexus()
