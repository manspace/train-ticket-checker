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

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            page = browser.new_page()
            page.goto(
                "https://booking.uz.gov.ua/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(10000)

            title = page.title()
            html = page.content()
            text = html[:1000]

            browser.close()

        return {
            "found": False,
            "from": request.from_city,
            "to": request.to_city,
            "date": request.date,
            "wagon": request.wagon,
            "passengers": passengers,
            "message": "УЗ title: " + title + " HTML: " + text
        }

    except Exception as e:
        return {
            "found": False,
            "from": request.from_city,
            "to": request.to_city,
            "date": request.date,
            "wagon": request.wagon,
            "passengers": passengers,
            "message": "Playwright не зміг відкрити УЗ.",
            "error": str(e)
        }
