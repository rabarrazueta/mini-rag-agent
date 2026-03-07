# rag_engine.py
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
import os

class RAGEngine:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.Client() # Se mantiene en memoria
        self.collection = self.client.create_collection("documentos")
        self.groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def ingest(self, texto: str, doc_id: str, fuente: str = "manual"):
        chunks = [c.strip() for c in texto.split('\n\n') if len(c.strip()) > 50]
        embeddings = self.embedder.encode(chunks).tolist()
        
        metadatos = [{"source": fuente, "id": doc_id} for _ in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatos,
            ids=[f"{doc_id}_{i}" for i in range(len(chunks))]
        )

    def ingest_folder(self, folder_path: str):
        """Escanea la carpeta e ingesta archivos .txt si existen."""
        if not os.path.exists(folder_path):
            return
            
        for file in os.listdir(folder_path):
            if file.endswith(".txt"):
                with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                    self.ingest(f.read(), file, fuente=f"archivo: {file}")

    def query(self, pregunta: str, n_resultados: int = 3) -> dict:
        embedding_query = self.embedder.encode([pregunta]).tolist()
        resultados = self.collection.query(
            query_embeddings=embedding_query,
            n_results=n_resultados
        )
        
        contexto = "\n\n".join(resultados['documents'][0])
        fuentes = list(set([m.get("source", "desconocida") for m in resultados['metadatas'][0]]))
        
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
        
        return {
            "respuesta": respuesta.choices[0].message.content,
            "fuentes_utilizadas": fuentes
        }
