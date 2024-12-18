from flask import Flask, request, jsonify
import os
from main import AnnouncementBot

app = Flask(__name__)
bot = AnnouncementBot()

@app.route("/new-announcement", methods=['POST'])
def handle_new_announcement():
    # Check webhook secret from headers
    x_webhook_secret = request.headers.get('x-webhook-secret')
    if x_webhook_secret != os.getenv("WEBHOOK_SECRET"):
        return jsonify({"status": "error", "message": "Invalid webhook secret"}), 403
        
    try:
        payload = request.get_json()
        stock_name = payload.get('stock_name')
        
        if stock_name:
            print(f"Processing new announcement for {stock_name}")
            announcement = bot.get_latest_announcement(stock_name)
            return jsonify({"status": "success", "processed": bool(announcement)})
        
        return jsonify({"status": "error", "message": "No stock name provided"})
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    print("Starting application...")
    port = int(os.getenv("PORT", 4000))
    app.run(host="0.0.0.0", port=port)