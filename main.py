from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

app = FastAPI()

class TicketRequest(BaseModel):
    from_city: str
    to_city: str
    date: str
    wagon: str | None = "any"
    passengers: Any = 1

@app.get("/")
def home():
    return {"status": "ok", "message": "Railway app is alive"}

@app.post("/check")
def check_tickets(request: TicketRequest):
    try:
        passengers = int(request.passengers)
    except Exception:
        passengers = 1

    return {
        "found": False,
        "from": request.from_city,
        "to": request.to_city,
        "date": request.date,
        "wagon": request.wagon,
        "passengers": passengers,
        "message": "Railway API працює. Повернули стабільну версію."
    }
