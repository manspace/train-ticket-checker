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

            page = browser.new_page()
            page.goto("https://example.com", wait_until="domcontentloaded", timeout=30000)

            title = page.title()
            text = page.locator("body").inner_text(timeout=10000)

            browser.close()

        return {
            "found": False,
            "message": "Playwright відкрив example.com. Title: " + title + ". Text: " + text[:200]
        }

    except Exception as e:
        return {
            "found": False,
            "message": "Playwright failed on example.com.",
            "error": str(e)
        }
