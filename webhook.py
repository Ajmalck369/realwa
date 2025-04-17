# webhook.py
from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "myverifytoken")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")  # Your WhatsApp API token from Meta
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

@app.route('/')
def home():
    return 'WhatsApp Webhook is Running ✅', 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge'), 200
        return "Verification failed", 403

    elif request.method == 'POST':
        data = request.json
        print("📩 Incoming WhatsApp Webhook:\n", data)

        try:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]
            contact = data['entry'][0]['changes'][0]['value']['contacts'][0]

            user_number = message['from']
            user_name = contact['profile']['name']
            text = message['text']['body'].strip().lower()

            # --- MENU LOGIC ---
            if text in ['hi', 'hello', 'start', 'menu']:
                reply(user_number, WELCOME_MENU)
            elif text == "1":
                reply(user_number, "🔍 About Sharjah Digital:\nSharjah Digital is a unified platform offering seamless access to essential public services and digital initiatives.")
            elif text == "2":
                reply(user_number, "🏠 Services:\nYou can access visa info, healthcare services, license renewals, utility payments, and more.")
            elif text == "3":
                reply(user_number, "🎟️ SEDD:\nSharjah Economic Development Department supports business licensing and trade services.")
            elif text == "4":
                reply(user_number, "📄 Municipality:\nExplore property services, waste management, and urban planning information.")
            elif text == "5":
                reply(user_number, "💰 Finance:\nIncludes fee payments, financial assistance programs, and public funding insights.")
            elif text == "6":
                reply(user_number, "🏛️ Archeology:\nDiscover museums, ancient sites, and Sharjah's historical treasures.")
            elif text == "7":
                reply(user_number, "📍 Places to Visit:\nTop sites: Al Noor Island, Sharjah Aquarium, Desert Park, and more.")
            elif text == "8":
                reply(user_number, "🎫 Events:\nGet updates on Sharjah's cultural, sporting, and entertainment events.")
            elif text == "9":
                reply(user_number, "🎮 Entertainment:\nMovies, exhibitions, theme parks, and family zones.")
            elif text == "10":
                reply(user_number, "🆘 Help:\nFor support, type 'help' or call 800-SHARJAH.")
            elif text == "11":
                reply(user_number, "👵 Senior Services:\nAccess healthcare, transport, and home services tailored to senior citizens.")
            elif text == "12":
                reply(user_number, "➕ Additional:\nYou can request new services, share feedback, or apply for initiatives.")
            else:
                reply(user_number, "❓ Sorry, I didn’t understand that. Please reply with a number from the menu or type 'menu' to see options again.")

        except Exception as e:
            print("❌ Error parsing webhook:", e)

        return "Webhook received", 200

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
    response = requests.post(url, json=payload, headers=headers)
    print("📤 Sent reply:", response.text)
