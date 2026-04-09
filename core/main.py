# core/main.py
import os
import json
from google import genai
from google.genai import types
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Cliente sem forçar versão - deixa o SDK escolher
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

def discover_model():
    """Descobre qual modelo está disponível AGORA para esta API key."""
    print("\n" + "="*60)
    print("[NEXUS_BOOT] Descobrindo modelos disponíveis...")
    print("="*60)
    
    # Lista todos os modelos que a chave consegue ver
    available = []
    try:
        for m in client.models.list():
            available.append(m.name)
            print(f"  [FOUND] {m.name}")
    except Exception as e:
        print(f"  [ERRO] Falha ao listar modelos: {e}")
    
    # Ordem de preferência: modelos mais recentes primeiro
    preferred = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro",
    ]
    
    # Testa cada candidato com uma chamada real
    for candidate in preferred:
        # Verifica se está na lista (com ou sem prefixo 'models/')
        found_in_list = any(candidate in name for name in available)
        if not found_in_list:
            continue
        
        print(f"\n[NEXUS_BOOT] Testando {candidate} com chamada real...")
        try:
            response = client.models.generate_content(
                model=candidate,
                contents="Responda apenas: OK"
            )
            if response and response.text:
                print(f"[NEXUS_BOOT] ✓ SUCESSO: {candidate} respondeu!")
                print(f"[NEXUS_BOOT] Engine selecionada: {candidate}")
                print("="*60 + "\n")
                return candidate
        except Exception as e:
            print(f"[NEXUS_BOOT] ✗ {candidate} falhou: {str(e)[:80]}")
    
    # Se nenhum preferido funcionar, tenta qualquer um que suporte generateContent
    print("\n[NEXUS_BOOT] Tentando qualquer modelo disponível...")
    for name in available:
        clean_name = name.replace("models/", "")
        try:
            response = client.models.generate_content(
                model=clean_name,
                contents="Responda apenas: OK"
            )
            if response and response.text:
                print(f"[NEXUS_BOOT] ✓ Fallback encontrado: {clean_name}")
                print("="*60 + "\n")
                return clean_name
        except:
            continue
    
    print("[NEXUS_BOOT] CRITICAL: Nenhum modelo funcional encontrado!")
    print("="*60 + "\n")
    return None


class Nexus:
    def __init__(self):
        self.model_id = discover_model()
        if self.model_id:
            print(f"[NEXUS_CORE] Online com: {self.model_id}")
        else:
            print("[NEXUS_CORE] OFFLINE - Verifique sua GEMINI_API_KEY")

    def pensar_e_agir(self, user_input, dominio_alvo="desconhecido"):
        if not self.model_id:
            return {
                "fase": "ERRO_SISTEMA",
                "estrategia": "Nenhum modelo de IA disponível. Verifique a GEMINI_API_KEY.",
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

        try:
            response = client.models.generate_content(
                model=self.model_id,
                contents=full_prompt
            )
            raw = response.text.strip()
            raw = raw.replace('```json', '').replace('```', '').strip()
            return json.loads(raw)
        except Exception as e:
            return {
                "fase": "ERRO_SISTEMA",
                "estrategia": f"Erro Nexus ({self.model_id}): {str(e)}",
                "comando": "N/A",
                "ferramenta": "N/A",
                "alerta": "Falha na Camada Neural",
                "error": True
            }

nexus = Nexus()
