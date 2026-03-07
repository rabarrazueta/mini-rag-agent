# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import RAGEngine

app = FastAPI()
rag = RAGEngine()

class IngestRequest(BaseModel):
    texto: str
    doc_id: str

class QueryRequest(BaseModel):
    pregunta: str

@app.post("/ingest")
def ingest(req: IngestRequest):
    rag.ingest(req.texto, req.doc_id)
    return {"status": "ok", "mensaje": f"Documento {req.doc_id} procesado"}

@app.post("/query")
def query(req: QueryRequest):
    respuesta = rag.query(req.pregunta)
    return {"pregunta": req.pregunta, "respuesta": respuesta}

@app.get("/health")
def health():
    return {"status": "ok"}
