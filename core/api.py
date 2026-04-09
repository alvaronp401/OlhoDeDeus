from fastapi import FastAPI, Query, File, UploadFile, Form
from pydantic import BaseModel
from .main import nexus
from .database import db
from .vision_engine import analisar_evidencia_visual
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/ask")
async def ask_nexus(data: dict):
    # Aceita dict flexível para o dashboard legado
    return nexus.pensar_e_agir(data.get("command"), data.get("target"))

@app.post("/ask/vision")
async def ask_vision(
    target: str = Form(...),
    prompt: str = Form("Analise esta evidência."),
    image: UploadFile = File(...)
):
    """Módulo de Visão: Analisa print de tela e integra achados ao banco."""
    image_bytes = await image.read()
    raw_analysis = analisar_evidencia_visual(image_bytes, prompt)
    
    try:
        # Tenta extrair JSON da resposta do Gemini Vision
        clean_raw = raw_analysis.strip().replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_raw)
        
        # Se encontrou vulnerabilidade na imagem, salva no DB
        if data.get("vetor") and data.get("vetor") != "None":
            db.save_vulnerability(
                target, 
                f"[VISION] {data['vetor']}", 
                "MEDIUM", 
                data['analise'], 
                data.get("sugestao")
            )
        return data
    except:
        return {"analise": raw_analysis, "error": "A IA não retornou um JSON válido, mas a análise textual está disponível."}

@app.post("/execute")
async def execute_command(data: dict):
    return nexus.executar(data.get("comando") or data.get("command"), data.get("target"))

@app.get("/vulnerabilities")
def get_vulnerabilities(target: str = Query(None)):
    return db.get_vulnerabilities(target)

@app.get("/loot")
def get_loot(target: str = Query(None)):
    return db.get_loot(target)

@app.get("/status")
def get_status():
    return {"status": "Online", "engine": nexus.model_id, "vision": "Active"}
