from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TicketRequest(BaseModel):
    from_city: str
    to_city: str
    date: str
    wagon: str | None = "any"
    passengers: int | None = 1


@app.get("/")
def home():
    return {"status": "ok", "message": "Train ticket checker is running"}


@app.post("/check")
def check_tickets(request: TicketRequest):
    return {
        "found": False,
        "from": request.from_city,
        "to": request.to_city,
        "date": request.date,
        "wagon": request.wagon,
        "passengers": request.passengers,
        "message": "Сервіс працює. Реальну перевірку УЗ підключимо наступним кроком."
    }
