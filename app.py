import os
import random
import time
import requests
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOP_URL = os.getenv("SHOP_URL")
VARIANT_ID = os.getenv("VARIANT_ID")

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def create_fake_order():
    prenoms = ["Alex", "Emma", "Lucas", "Léa", "Noah", "Inès"]
    noms = ["Martin", "Bernard", "Robert", "Richard", "Petit", "Durand"]
    email = f"{random.choice(prenoms).lower()}.{random.choice(noms).lower()}{random.randint(100, 999)}@gmail.com"

    order = {
        "order": {
            "email": email,
            "send_receipt": False,
            "send_fulfillment_receipt": False,
            "line_items": [
                {"variant_id": int(VARIANT_ID), "quantity": 1}
            ]
        }
    }

    url = f"https://{SHOP_URL}/admin/api/2024-01/orders.json"
    r = requests.post(url, json=order, headers=HEADERS, timeout=30)

    if r.status_code == 201:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Commande créée : {email}")
        return True
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {r.status_code} - {r.text}")
        return False

def run_bot():
    # checks de base pour éviter de tourner à vide
    missing = [k for k,v in {
        "SHOP_URL": SHOP_URL, "SHOPIFY_ACCESS_TOKEN": SHOPIFY_ACCESS_TOKEN, "VARIANT_ID": VARIANT_ID
    }.items() if not v]
    if missing:
        print("⛔ Variables manquantes :", ", ".join(missing))
        return

    total_revenue = 0.0
    revenue_target = random.randint(3000, 5500)
    price = 59.90

    print(f"🎯 Objectif du jour : {revenue_target} $ | Boutique: {SHOP_URL}")

    while total_revenue < revenue_target:
        now = datetime.now()
        if 9 <= now.hour <= 21:
            if random.random() < 0.75:
                if create_fake_order():
                    total_revenue += price
                    print(f"📈 Revenu actuel : {round(total_revenue, 2)} $ / {revenue_target} $")
        pause = random.randint(300, 1200)  # 5–20 min
        print(f"⏱ Pause de {pause//60} min...\n")
        time.sleep(pause)

if __name__ == "__main__":
    run_bot()
