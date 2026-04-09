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
    return {"status": "Nexus Core Online", "engine": "Google GenAI SDK v1 (Flash)"}
