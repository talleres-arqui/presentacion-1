# -----------------------------
# 1. Imagen base
# -----------------------------
FROM python:3.11-slim

# -----------------------------
# 2. Variables de entorno
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------
# 3. Directorio de la app
# -----------------------------
WORKDIR /

# -----------------------------
# 4. Copiar requirements e instalar
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 5. Copiar el código de la app
# -----------------------------
COPY . .

# -----------------------------
# 6. Exponer puerto
# -----------------------------
EXPOSE 80

# -----------------------------
# 7. Comando para correr FastAPI
# -----------------------------
# main.py es tu archivo principal, app es el objeto FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
