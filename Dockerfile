FROM python:3.12-slim 
# Python ligero

WORKDIR /app 
# Directorio de trabajo

COPY requirements.txt . 
# Librerías a usar

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Código copiado

EXPOSE 8000
# Puerto a usar

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Comando de arranque