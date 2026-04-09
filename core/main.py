# core/main.py
import os
import json
import google.generativeai as genai
import chromadb
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

chroma_client = chromadb.PersistentClient(path="./memory/chroma_db")
collection = chroma_client.get_or_create_collection(name="nexus_memory")

class Nexus:
    def __init__(self):
        # Iniciamos com instruções de sistema rigorosas
        self.instruction = """
        Você é o NEXUS. Atue como um motor de Pentest Autônomo.
        Sempre retorne sua resposta em formato JSON estrito com as chaves:
        {
          "estrategia": "descrição do plano",
          "comando_sugerido": "comando real para o kali",
          "ferramenta_utilizada": "nome da ferramenta",
          "vulnerabilidade_suspeita": "nível e tipo",
          "anonimato_requerido": true/false
        }
        """
        self.chat = model.start_chat(history=[])

    def pensar_e_agir(self, user_input, dominio_alvo):
        # Consulta memória sobre o alvo ou tecnologias parecidas
        memoria = collection.query(query_texts=[user_input, dominio_alvo], n_results=3)
        
        contexto = f"CONTEXTO DE MEMÓRIA: {memoria['documents']}\nALVO ATUAL: {dominio_alvo}"
        
        full_prompt = f"{self.instruction}\n{contexto}\nENTRADA: {user_input}"
        
        response = self.chat.send_message(full_prompt)
        
        # Tenta parsear o JSON para garantir que o dashboard receba dados limpos
        try:
            return json.loads(response.text.replace('```json', '').replace('```', ''))
        except:
            return {"estrategia": response.text, "error": "Falha ao estruturar JSON"}

nexus = Nexus()
