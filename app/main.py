from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/health")
def get_health():
    return {"msg": "ok"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

handler = Mangum(app)