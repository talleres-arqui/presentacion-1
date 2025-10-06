from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import asyncio
import paho.mqtt.client as mqtt

from database import SessionLocal, engine, Base
from models import PublicationDB, Publication

import json

# ---------------------------
# 1. Inicializar Base de Datos
# ---------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ---------------------------
# 2. Dependencia DB
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# 3. Gestor de WebSockets
# ---------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

# ---------------------------
# 4. Configuración MQTT
# ---------------------------
BROKER = "broker.hivemq.com"   # o test.mosquitto.org
PORT = 1883
TOPIC = "mi/topico/de/prueba"

mqtt_queue = asyncio.Queue()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado al broker MQTT")
        client.subscribe(TOPIC)
    else:
        print(f"❌ Error de conexión MQTT: {rc}")

def on_message(client, userdata, msg):
    mensaje = msg.payload.decode()
    print(f"📡 Recibido en MQTT: {mensaje}")
    # Usamos el loop principal guardado
    main_loop.call_soon_threadsafe(mqtt_queue.put_nowait, mensaje)



mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# ---------------------------
# 5. Consumidor de mensajes MQTT
# ---------------------------
async def mqtt_consumer():
    while True:
        mensaje = await mqtt_queue.get()
        print(f"🔄 Procesando mensaje MQTT: {mensaje}")

        db = SessionLocal()
        try:
            data = json.loads(mensaje)
            publication = Publication(**data)   # CORRECCIÓN AQUÍ
            pub = PublicationDB(title=publication.title, body=publication.body)
            print(publication.body)
            
            db.add(pub)
            db.commit()
            db.refresh(pub)

            await manager.broadcast(f"{pub.id}: {pub.title} - {pub.body}")
        finally:
            db.close()

# ---------------------------
# 6. Eventos de ciclo de vida
# ---------------------------
@app.on_event("startup")
async def startup_event():
    global main_loop
    main_loop = asyncio.get_running_loop()  # Guardamos el loop principal
    print("🚀 Iniciando MQTT y consumidor")
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_start()
    asyncio.create_task(mqtt_consumer())

@app.on_event("shutdown")
def shutdown_event():
    mqtt_client.loop_stop()

# ---------------------------
# 7. Endpoint WebSocket
# ---------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # el cliente puede mandar mensajes, pero se ignoran
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ---------------------------
# 8. Endpoint REST para ver publicaciones
# ---------------------------
@app.get("/", response_model=List[Publication])
def get_publications(db: Session = Depends(get_db)):
    return db.query(PublicationDB).all()
