# webhook.py
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "myverifytoken")


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

        # Optional: forward to Bardeen


        return "Webhook received", 200
