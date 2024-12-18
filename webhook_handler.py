from fastapi import FastAPI, Request, Header, HTTPException
import os
from main import AnnouncementBot

app = FastAPI()
bot = AnnouncementBot()

@app.post("/new-announcement")
async def handle_new_announcement(
    request: Request,
    x_webhook_secret: str = Header(None)
):
    if x_webhook_secret != os.getenv("WEBHOOK_SECRET"):
        raise HTTPException(status_code=403, detail="Invalid webhook secret")
        
    try:
        payload = await request.json()
        stock_name = payload.get('stock_name')
        
        if stock_name:
            print(f"Processing new announcement for {stock_name}")
            announcement = bot.get_latest_announcement(stock_name)
            return {"status": "success", "processed": bool(announcement)}
        
        return {"status": "error", "message": "No stock name provided"}
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}