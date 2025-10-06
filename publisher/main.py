from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine, Base
from models import PublicationDB, Publication

import paho.mqtt.client as mqtt
import json


# -----------------------------
# Configuración de la base de datos
# -----------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI()

# -----------------------------
# Configuración de CORS
# -----------------------------
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # ⚠️ evita usar "*" con credenciales
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Configuración MQTT
# -----------------------------
BROKER = "broker.hivemq.com"   # o test.mosquitto.org
PORT = 1883
TOPIC = "mi/topico/de/prueba"

mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()  # para que funcione en segundo plano


# -----------------------------
# Dependencia de la base de datos
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Endpoint: Crear publicación
# -----------------------------
@app.post("/publication")
def create_publication(publication: Publication, db: Session = Depends(get_db)):
    # Guardar en la base de datos
    db_publication = PublicationDB(title=publication.title, body=publication.body)
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)

    # Crear mensaje limpio para enviar por MQTT
    mensaje = {
        "id": db_publication.id,
        "title": db_publication.title,
        "body": db_publication.body
    }

    # Publicar mensaje en el broker MQTT
    mqtt_client.publish(TOPIC, json.dumps(mensaje))

    # Retornar respuesta JSON válida
    return {
        "message": "Publication created & sent via MQTT",
        "publication": mensaje
    }


# -----------------------------
# Endpoint: Obtener publicaciones
# -----------------------------
@app.get("/publications", response_model=List[Publication])
def get_publications(db: Session = Depends(get_db)):
    publications = db.query(PublicationDB).all()
    return publications
