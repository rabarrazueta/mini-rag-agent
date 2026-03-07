import os
from rag_engine import RAGEngine

# Asegúrate de que tu API KEY esté en el entorno
# Si no la has exportado en la terminal, puedes hacerlo aquí (solo para pruebas):
# os.environ["GROQ_API_KEY"] = "tu_clave_aqui"

print("🧠 Iniciando Motor RAG...")
engine = RAGEngine()

# 1. Cargar el documento
print("📂 Ingestando documento de Processia Ops...")
with open("documents/processia.txt", "r", encoding="utf-8") as f:
    contenido = f.read()
    engine.ingest(contenido, "processia_info")

# 2. Prueba de "Éxito Semántico"
# Pregunta algo que esté en el texto pero con otras palabras
pregunta_real = "¿Qué beneficios ofrecen sus servicios de automatización?"
print(f"\n❓ Pregunta Relevante: {pregunta_real}")
print(f"🤖 Respuesta: {engine.query(pregunta_real)}")

# 3. Prueba de "Control de Alucinaciones"
# Pregunta algo totalmente ajeno
pregunta_ajena = "¿Cómo se cocina una paella valenciana?"
print(f"\n❓ Pregunta Ajena: {pregunta_ajena}")
print(f"🤖 Respuesta: {engine.query(pregunta_ajena)}")