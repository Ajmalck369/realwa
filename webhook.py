import os
import requests
from flask import Flask, request

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")  # Your WhatsApp API token
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")  # From Meta Console

WELCOME_MENU = """
Welcome to Digital Sharjah Services:
Please select your language:
1️⃣ Arabic
2️⃣ English

Once selected:

1. 🏥 About Sharjah Digital
2. 🏠 Services
3. 🎟️ SEDD
4. 📄 Municipality
5. 💰 Finance
6. 🏛️ Archeology
7. 📍 Places to Visit
8. 🎫 Events
9. 🎮 Entertainment
10. 🆘 Help
11. 👵 Senior Services
12. ➕ Additional

Reply with a number to continue.
"""

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get("VERIFY_TOKEN"):
            return request.args.get('hub.challenge'), 200
        return "Verification failed", 403

    elif request.method == 'POST':
        data = request.json
        try:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]
            contact = data['entry'][0]['changes'][0]['value']['contacts'][0]

            user_number = message['from']
            text = message['text']['body'].strip().lower()

            # ROUTING
            if text in ['hi', 'hello', 'start', 'menu']:
                reply(user_number, WELCOME_MENU)
            elif text == "1":
                reply(user_number, "🔍 About Sharjah Digital:\nSharjah Digital is a smart platform connecting all services under one roof...")
            elif text == "2":
                reply(user_number, "🏠 Available services include government, licensing, healthcare, utilities, etc.")
            elif text == "3":
                reply(user_number, "🎟️ SEDD (Sharjah Economic Development Department):\nYou can check license status, apply for new businesses, etc.")
            # ... and so on up to 12
            else:
                reply(user_number, "I didn't understand that. Please reply with a number from the menu.")

        except Exception as e:
            print("❌ Error:", e)

        return "OK", 200

def reply(user_number, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": user_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    requests.post(url, json=payload, headers=headers)
