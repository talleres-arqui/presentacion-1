from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import asyncio
import paho.mqtt.client as mqtt
import json

from database import SessionLocal, engine, Base
from models import PublicationDB, Publication

# ---------------------------
# 1. Inicializar Base de Datos
# ---------------------------
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Suscriptor de Noticias")

# ---------------------------
# 2. Configuración CORS
# ---------------------------
origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# 3. Dependencia DB
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# 4. Cola compartida para SSE
# ---------------------------
mqtt_queue = asyncio.Queue()       # cola original (mensajes MQTT)
sse_queue = asyncio.Queue()        # cola adicional para el stream SSE

# ---------------------------
# 5. MQTT Configuración
# ---------------------------
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "mi/topico/de/prueba"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado al broker MQTT")
        client.subscribe(TOPIC)
    else:
        print(f"❌ Error de conexión MQTT: {rc}")

def on_message(client, userdata, msg):
    mensaje = msg.payload.decode()
    print(f"📡 Recibido en MQTT: {mensaje}")
    main_loop.call_soon_threadsafe(mqtt_queue.put_nowait, mensaje)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# ---------------------------
# 6. Consumidor de mensajes MQTT
# ---------------------------
async def mqtt_consumer():
    while True:
        mensaje = await mqtt_queue.get()
        print(f"🔄 Procesando mensaje MQTT: {mensaje}")

        db = SessionLocal()
        try:
            data = json.loads(mensaje)
            publication = Publication(**data)
            pub = PublicationDB(title=publication.title, body=publication.body)
            db.add(pub)
            db.commit()
            db.refresh(pub)

            print(f"✅ Guardado en BD: {pub.title}")

            # 🔹 Enviar publicación a la cola SSE
            await sse_queue.put({
                "id": pub.id,
                "title": pub.title,
                "body": pub.body
            })

        except Exception as e:
            print(f"⚠️ Error procesando mensaje MQTT: {e}")
        finally:
            db.close()

# ---------------------------
# 7. Endpoint SSE (solo cuando llega una publicación)
# ---------------------------
async def sse_event_stream():
    while True:
        data = await sse_queue.get()  # espera hasta que llegue una publicación
        json_data = json.dumps(data)
        yield f"data: {json_data}\n\n"

@app.get("/stream")
async def stream():
    print("📡 Cliente SSE conectado")
    return StreamingResponse(sse_event_stream(), media_type="text/event-stream")

# ---------------------------
# 8. Endpoint REST para ver publicaciones
# ---------------------------
@app.get("/", response_model=List[Publication])
def get_publications(db: Session = Depends(get_db)):
    print("📃 Consultando publicaciones guardadas...")
    return db.query(PublicationDB).all()

# ---------------------------
# 9. Eventos de ciclo de vida
# ---------------------------
@app.on_event("startup")
async def startup_event():
    global main_loop
    main_loop = asyncio.get_running_loop()
    print("🚀 Iniciando conexión MQTT y consumidor")
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_start()
    asyncio.create_task(mqtt_consumer())

@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Deteniendo cliente MQTT...")
    mqtt_client.loop_stop()
