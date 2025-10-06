from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("✅ Cliente conectado")
    await ws.send_text("Conexión WebSocket exitosa 🎉")
    await ws.close()

if __name__ == "__main__":
    uvicorn.run("ws_test:app", host="0.0.0.0", port=8001, reload=True)
