# core/main.py
import os
import json
import google.generativeai as genai
import chromadb
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def initialize_model(model_name="gemini-1.5-flash"):
    """Tenta inicializar o modelo, com fallback para o Flash se o Pro falhar."""
    try:
        print(f"[NEXUS_CORE] Tentando inicializar modelo: {model_name}")
        return genai.GenerativeModel(model_name)
    except Exception as e:
        print(f"[NEXUS_CORE] Erro ao carregar {model_name}: {e}")
        if model_name != "gemini-1.5-flash":
            print("[NEXUS_CORE] Fazendo fallback para gemini-1.5-flash...")
            return genai.GenerativeModel("gemini-1.5-flash")
        raise e

# Inicializamos o modelo (preferência agora é Flash pela velocidade e disponibilidade)
model = initialize_model("gemini-1.5-flash")

chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
collection = chroma_client.get_or_create_collection(name="nexus_memory")

class Nexus:
    def __init__(self):
        # Iniciamos com instruções de sistema rigorosas
        self.instruction = """
        Você é o NEXUS, o motor do 'Olho de Deus'.
        Sua metodologia é baseada no PTES (Penetration Testing Execution Standard).
        
        Sempre retorne um JSON estruturado:
        {
          "fase": "RECON | ENUM | VULN_DEV | EXPLOIT | POST",
          "estrategia": "Sua análise detalhada",
          "comando": "O comando exato para o Kali",
          "ferramenta": "nmap, ffuf, sqlmap, katana...",
          "alerta": "Algo crítico encontrado?"
        }
        """
        try:
            self.chat = model.start_chat(history=[])
        except Exception as e:
            print(f"[NEXUS_CORE] Erro ao iniciar chat: {e}")
            self.chat = None

    def pensar_e_agir(self, user_input, dominio_alvo="desconhecido"):
        if not self.chat:
            return {"error": "IA não inicializada corretamente. Verifique sua GEMINI_API_KEY."}

        # Consulta memória sobre o alvo ou tecnologias parecidas
        try:
            memoria = collection.query(query_texts=[user_input, dominio_alvo], n_results=3)
            contexto = f"CONTEXTO DE MEMÓRIA: {memoria['documents']}\nALVO ATUAL: {dominio_alvo}"
        except:
            contexto = f"ALVO ATUAL: {dominio_alvo}"
        
        full_prompt = f"{self.instruction}\n{contexto}\nENTRADA: {user_input}"
        
        try:
            response = self.chat.send_message(full_prompt)
            # Tenta parsear o JSON para garantir que o dashboard receba dados limpos
            return json.loads(response.text.replace('```json', '').replace('```', ''))
        except Exception as e:
            return {
                "fase": "ERRO_SISTEMA",
                "estrategia": f"Erro na comunicação com a IA: {str(e)}",
                "comando": "N/A",
                "ferramenta": "N/A",
                "alerta": "Falha Crítica no Nexus Core",
                "error": True
            }

nexus = Nexus()
