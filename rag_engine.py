# rag_engine.py
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
import os

class RAGEngine:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("documentos")
        self.groq = Groq(api_key=os.environ.get("GROQ_API_KEY")) # usa tu GROQ_API_KEY

    def ingest(self, texto: str, doc_id: str):
        # Chunking simple: dividir por párrafos
        chunks = [c.strip() for c in texto.split('\n\n') if len(c.strip()) > 50]
        embeddings = self.embedder.encode(chunks).tolist()
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"{doc_id}_{i}" for i in range(len(chunks))]
        )

    def query(self, pregunta: str, n_resultados: int = 3) -> str:
        embedding_query = self.embedder.encode([pregunta]).tolist()
        resultados = self.collection.query(
            query_embeddings=embedding_query,
            n_results=n_resultados
        )
        contexto = "\n\n".join(resultados['documents'][0])
        
        respuesta = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": 
                 "Responde únicamente basándote en el contexto proporcionado. "
                 "Si la respuesta no está en el contexto, dilo explícitamente."},
                {"role": "user", "content": 
                 f"Contexto:\n{contexto}\n\nPregunta: {pregunta}"}
            ]
        )
        return respuesta.choices[0].message.content
