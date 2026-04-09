# core/vision_engine.py
import os
import io
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

VISION_PROMPT = """
Você é o 'Olho de Deus - Módulo Visão'. 
Sua tarefa é analisar capturas de tela de ferramentas de pentest (Burp Suite, Wireshark, Terminal, Navigators) e identificar vetores de ataque.

INSTRUÇÕES:
1. Identifique a ferramenta na imagem.
2. Extraia parâmetros, URLs ou headers suspeitos.
3. Sugira um payload de exploração ou o próximo comando para o Kali.
4. Responda APENAS com um JSON válido:
{"analise": "o que você viu", "vetor": "XSS/SQLi/etc", "sugestao": "payload ou comando", "ferramenta_detectada": "nome"}
"""

def analisar_evidencia_visual(image_bytes, prompt_extra=""):
    """Envia uma imagem para o Gemini 2.0 Vision e retorna análise técnica."""
    try:
        # Converte bytes para objeto de imagem PIL para validação (opcional)
        img = Image.open(io.BytesIO(image_bytes))
        
        full_prompt = f"{VISION_PROMPT}\nContexto adicional do operador: {prompt_extra}"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                full_prompt,
                types.Part.from_bytes(data=image_bytes, mime_type="image/png")
            ]
        )
        
        return response.text
    except Exception as e:
        return f"Erro na análise de visão: {str(e)}"
