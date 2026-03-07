# FastAPI RAG Engine (Groq + ChromaDB)

Este es un sistema de **Generación Aumentada por Recuperación (RAG)** diseñado para ser ligero, modular y fácil de probar. Utiliza **FastAPI** para la interfaz de comunicación, **ChromaDB** como base de datos vectorial en memoria y **Groq (Llama 3.3)** para la generación de respuestas inteligentes.

El motor es híbrido: puede consumir información de archivos de texto locales y de datos enviados dinámicamente a través de una API.

## 🚀 Características

-   **Ingesta Híbrida**: Carga automáticamente archivos `.txt` desde la carpeta `/documents` al iniciar.
    
-   **API de Ingesta**: Endpoint para agregar nuevo contexto "al vuelo" sin reiniciar el sistema.
    
-   **Rastreo de Fuentes**: Cada respuesta incluye metadatos que indican exactamente de qué archivo o fuente se extrajo la información.
    
-   **Base de Datos Volátil**: Diseñado para pruebas; utiliza almacenamiento en memoria que se limpia al detener el contenedor o servicio.
    
-   **Docker Ready**: Configuración completa con Docker y Docker Compose para un despliegue inmediato.
    

## 🛠️ Requisitos Previos

-   Python 3.12+ (si se corre localmente).
    
-   API KEY de **Groq**.
    
-   Docker y Docker Compose (opcional para despliegue en contenedores).
    

## 🔧 Configuración e Instalación

### Opción 1: Local (con venv)

1.  **Clonar el repositorio y entrar:**
    
    Bash
    
    ```
    git clone https://github.com/rabarrazueta/mini-rag-agent
    cd mini-rag-agent
    
    ```
    
2.  **Crear y activar el entorno virtual:**
    
    Bash
    
    ```
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Linux/Mac:
    source venv/bin/activate
    
    ```
    
3.  **Instalar dependencias:**
    
    Bash
    
    ```
    pip install -r requirements.txt
    
    ```
    
4.  **Configurar la variable de entorno:**
    
    Bash
    
    ```
    # En Linux/Mac:
    export GROQ_API_KEY="tu_api_key_aquí"
    # En Windows (PowerShell):
    $env:GROQ_API_KEY="tu_api_key_aquí"
    
    ```
    
5.  **Ejecutar la aplicación:**
    
    Bash
    
    ```
    uvicorn main:app --reload
    
    ```
    

### Opción 2: Docker Compose

1.  **Crear un archivo `.env`** en la raíz del proyecto y añadir tu llave:
    
    Fragmento de código
    
    ```
    GROQ_API_KEY=tu_api_key_aquí
    
    ```
    
2.  **Levantar el contenedor:**
    
    Bash
    
    ```
    docker-compose up --build
    
    ```
    
    El servicio estará disponible en `http://localhost:8000`.
    

## 📖 Uso de la API

### 1. Ingesta Automática

Cualquier archivo `.txt` colocado en la carpeta `./documents` será procesado e indexado automáticamente cuando el servidor se inicie.

### 2. Ingesta Manual (POST `/ingest`)

Agrega texto adicional al motor de búsqueda.

-   **URL:** `http://localhost:8000/ingest`
    
-   **Cuerpo (JSON):**
    
    JSON
    
    ```
    {
      "texto": "Contenido de ejemplo para el RAG",
      "doc_id": "documento_01"
    }
    
    ```
    

### 3. Consulta (POST `/query`)

Realiza preguntas basadas en el contexto cargado.

-   **URL:** `http://localhost:8000/query`
    
-   **Cuerpo (JSON):**
    
    JSON
    
    ```
    {
      "pregunta": "¿Qué servicios ofrece la empresa?"
    }
    
    ```
    
-   **Respuesta:** El sistema devolverá la `respuesta` generada por el LLM y una lista de `fuentes_utilizadas`.
    

## 📂 Estructura del Proyecto

-   `main.py`: Definición de la API y eventos de ciclo de vida.
    
-   `rag_engine.py`: Lógica de embeddings, base de datos vectorial y conexión con Groq.
    
-   `documents/`: Carpeta para almacenamiento de archivos de texto locales.
    
-   `requirements.txt`: Lista de dependencias del proyecto.
    
-   `Dockerfile` & `docker-compose.yml`: Configuración para contenedores.