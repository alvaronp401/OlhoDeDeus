from fastapi import FastAPI
from pydantic import BaseModel
from .main import nexus
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PentestRequest(BaseModel):
    command: str
    target: str

@app.post("/ask")
async def ask_nexus(data: PentestRequest):
    # O Nexus agora recebe o alvo para manter o contexto na memória
    resultado = nexus.pensar_e_agir(data.command, data.target)
    return resultado

@app.get("/status")
def get_status():
    return {
        "status": "Nexus Core Online" if nexus.model_id else "Nexus Core OFFLINE",
        "engine": nexus.model_id or "Nenhum modelo encontrado"
    }

@app.get("/debug/nexus")
def debug_nexus():
    return {
        "active_model": nexus.model_id,
        "mode": "auto-discovery",
        "health": "OK" if nexus.model_id else "FAILED"
    }
