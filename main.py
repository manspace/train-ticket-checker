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
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            browser.close()

        return {
            "found": False,
            "message": "Playwright browser successfully launched in Railway."
        }

    except Exception as e:
        return {
            "found": False,
            "message": "Playwright failed.",
            "error": str(e)
        }
