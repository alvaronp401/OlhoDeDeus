from fastapi import FastAPI, Query
from pydantic import BaseModel
from .main import nexus
from .database import db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class PentestRequest(BaseModel):
    command: str
    target: str

class ExecuteRequest(BaseModel):
    command: str
    target: str
    use_proxy: bool = True

@app.post("/ask")
async def ask_nexus(data: PentestRequest):
    return nexus.pensar_e_agir(data.command, data.target)

@app.post("/execute")
async def execute_command(data: ExecuteRequest):
    return nexus.executar(data.command, data.target, data.use_proxy)

@app.get("/vulnerabilities")
def get_vulnerabilities(target: str = Query(None)):
    """Retorna vulnerabilidades reais do banco de dados."""
    return db.get_vulnerabilities(target)

@app.get("/loot")
def get_loot(target: str = Query(None)):
    """Retorna itens de loot reais do banco de dados."""
    return db.get_loot(target)

@app.get("/status")
def get_status():
    return {
        "status": "Online",
        "engine": nexus.model_id,
        "database": "Connected"
    }
