from fastapi import FastAPI, HTTPException
from typing import Dict
from model import Item

app = FastAPI()

# Modelo de datos (validación automática con Pydantic)


# Base de datos simulada (diccionario)
fake_db: Dict[int, Item] = {}

# Rutas CRUD ------------------------------

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API con FastAPI!"}

@app.get("/items/")
def get_items():
    return fake_db

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return fake_db[item_id]

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in fake_db:
        raise HTTPException(status_code=400, detail="El item ya existe")
    fake_db[item_id] = item
    return {"message": "Item creado correctamente", "item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    fake_db[item_id] = item
    return {"message": "Item actualizado", "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    del fake_db[item_id]
    return {"message": "Item eliminado"}
