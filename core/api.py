from fastapi import FastAPI
from pydantic import BaseModel
from .main import nexus
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Libera o acesso para o seu Dashboard (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    command: str

@app.post("/ask")
async def ask(data: RequestData):
    # O Nexus processa a pergunta usando Gemini + ChromaDB
    res = nexus.pensar_e_agir(data.command)
    return {"strategy": res}

@app.get("/")
def status():
    return {"status": "Nexus Core Online", "engine": "Gemini 1.5 Pro"}
