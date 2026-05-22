from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import requests

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

    try:
        url = "https://booking.uz.gov.ua/api/station/search/"
        params = {"term": request.from_city}

        response = requests.get(
            url,
            params=params,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://booking.uz.gov.ua/"
            }
        )

        return {
            "found": False,
            "from": request.from_city,
            "to": request.to_city,
            "date": request.date,
            "wagon": request.wagon,
            "passengers": passengers,
            "status_code": response.status_code,
            "response_preview": response.text[:1000],
            "message": "Тестую внутрішній API станцій УЗ."
        }

    except Exception as e:
        return {
            "found": False,
            "from": request.from_city,
            "to": request.to_city,
            "date": request.date,
            "wagon": request.wagon,
            "passengers": passengers,
            "message": "Помилка при зверненні до API станцій УЗ.",
            "error": str(e)
        }
