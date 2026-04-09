from fastapi import FastAPI, Query, File, UploadFile, Form
from pydantic import BaseModel
from .main import nexus
from .database import db
from .vision_engine import analisar_evidencia_visual
from .tools.check_anonymity import verificar_anonimato_fast
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/ask")
async def ask_nexus(data: dict):
    # Suporte a múltiplas chaves (command/comando)
    command = data.get("command") or data.get("comando")
    target = data.get("target") or "target"
    return nexus.pensar_e_agir(command, target)

@app.post("/ask/vision")
async def ask_vision(
    target: str = Form(...),
    prompt: str = Form("Analise esta evidência."),
    image: UploadFile = File(...)
):
    image_bytes = await image.read()
    raw_analysis = analisar_evidencia_visual(image_bytes, prompt)
    try:
        clean_raw = raw_analysis.strip().replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_raw)
        if data.get("vetor") and data.get("vetor") != "None":
            db.save_vulnerability(target, f"[VISION] {data['vetor']}", "MEDIUM", data['analise'], data.get("sugestao"))
        return data
    except:
        return {"analise": raw_analysis, "error": "JSON_FAILED"}

@app.post("/execute")
async def execute_command(data: dict):
    command = data.get("command") or data.get("comando")
    target = data.get("target")
    usar_proxy = data.get("use_proxy", True)
    return nexus.executar(command, target, usar_proxy)

@app.get("/proxy-status")
def get_proxy_status():
    """Retorna o status de anonimato real para o Dashboard."""
    return verificar_anonimato_fast()

@app.get("/vulnerabilities")
def get_vulnerabilities(target: str = Query(None)):
    return db.get_vulnerabilities(target)

@app.get("/loot")
def get_loot(target: str = Query(None)):
    return db.get_loot(target)

@app.get("/status")
def get_status():
    return {"status": "Online", "engine": nexus.model_id, "vision": "Active", "anonimato": "Monitoring"}
