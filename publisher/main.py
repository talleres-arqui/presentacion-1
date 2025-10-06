from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import PublicationDB, Publication

import paho.mqtt.client as mqtt

import json

# Configuración de la DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración MQTT
BROKER = "broker.hivemq.com"   # o test.mosquitto.org
PORT = 1883
TOPIC = "mi/topico/de/prueba"

mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()  # para que funcione en segundo plano


# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/publication")
def create_publication(publication: Publication, db: Session = Depends(get_db)):
    # Guardar en DB
    db_publication = PublicationDB(title=publication.title, body=publication.body)
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)

    # Enviar por MQTT
    mensaje = publication.__dict__
    mensaje['id'] = db_publication.id
    mqtt_client.publish(TOPIC, json.dumps(mensaje))

    return {"message": "Publication created & sent via MQTT", "publication": db_publication}


@app.get("/publications", response_model=List[Publication])
def get_publications(db: Session = Depends(get_db)):
    publications = db.query(PublicationDB).all()
    return publications
