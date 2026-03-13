import json
import uuid
import os
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import redis

# --- Inisialisasi ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

app = FastAPI(
    title="Coffee Order API (Redis-Powered)",
    description="Sistem pemesanan kopi modern menggunakan FastAPI dan Redis.",
    version="1.0.0"
)

# Koneksi Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# --- Models ---
class OrderItem(BaseModel):
    item_name: str = Field(..., example="Caramel Macchiato")
    quantity: int = Field(..., gt=0, example=1)
    notes: Optional[str] = Field(None, example="Less sugar")

class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, example="Annisa")
    items: List[OrderItem]

# --- Endpoints ---
@app.post("/orders", status_code=201, tags=["Orders"])
async def create_order(order: OrderCreate):
    order_id = str(uuid.uuid4())
    order_data = {
        "order_id": order_id,
        "customer_name": order.customer_name,
        "status": "Pending",
        "timestamp": datetime.now().isoformat(),
        "items": json.dumps([item.dict() for item in order.items])
    }
    r.hset(f"order:{order_id}", mapping=order_data)
    r.lpush("kitchen_queue", order_id) # Masuk antrean dapur
    return {"order_id": order_id, "message": "Order created and queued!"}

@app.get("/orders/{order_id}", tags=["Orders"])
async def get_status(order_id: str):
    order = r.hgetall(f"order:{order_id}")
    if not order: raise HTTPException(404, "Order not found")
    return order

@app.get("/kitchen/queue", tags=["Kitchen"])
async def view_queue():
    return {"queue": r.lrange("kitchen_queue", 0, -1)}

@app.post("/kitchen/process", tags=["Kitchen"])
async def process_order():
    order_id = r.rpop("kitchen_queue") # Ambil pesanan tertua (FIFO)
    if not order_id: return {"message": "No orders in queue"}
    r.hset(f"order:{order_id}", "status", "Preparing")
    return {"message": f"Processing order {order_id}"}
