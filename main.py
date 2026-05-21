from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
from playwright.sync_api import sync_playwright

app = FastAPI()


class TicketRequest(BaseModel):
    from_city: str
    to_city: str
    date: str
    wagon: str | None = "any"
    passengers: Any = 1


@app.get("/")
def home():
    return {"status": "ok", "message": "Train ticket checker is running with Playwright"}


@app.post("/check")
def check_tickets(request: TicketRequest):
    try:
        passengers = int(request.passengers)
    except Exception:
        passengers = 1

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = browser.new_page()
            page.goto(
                "https://booking.uz.gov.ua/",
                wait_until="domcontentloaded",
                timeout=30000
            )

            title = page.title()
            text = page.locator("body").inner_text(timeout=15000)

            browser.close()

        return {
            "found": False,
            "from": request.from_city,
            "to": request.to_city,
            "date": request.date,
            "wagon": request.wagon,
            "passengers": passengers,
            "page_title": title,
            "preview": text[:500],
            "message": "Playwright відкрив сайт УЗ. Наступним кроком додамо введення маршруту."
        }

    except Exception as e:
        return {
            "found": False,
            "from": request.from_city,
            "to": request.to_city,
            "date": request.date,
            "wagon": request.wagon,
            "passengers": passengers,
            "error": str(e),
            "message": "Сервіс запустився, але не зміг відкрити сайт УЗ. Помилку повернув у поле error."
        }
