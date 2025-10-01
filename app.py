import os
import random
import time
import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Charger les variables d'environnement
load_dotenv()

SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOP_URL = os.getenv("SHOP_URL")
VARIANT_ID = int(os.getenv("VARIANT_ID") or 0)

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

API_VERSION = "2025-01"
TZ = pytz.timezone("America/Toronto")  # fuseau horaire Canada

def create_paid_order():
    prenoms = ["Emma", "Lucas", "Alex", "Chloé", "Marc", "Sophie"]
    noms = ["Petit", "Martin", "Bernard", "Robert", "Lefebvre", "Gagnon"]
    first_name = random.choice(prenoms)
    last_name = random.choice(noms)

    # Génération email unique réaliste
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100,999)}@gmail.com"

    now = datetime.now(TZ).isoformat()

    order = {
        "order": {
            "email": email,
            "created_at": now,
            "line_items": [
                {"variant_id": VARIANT_ID, "quantity": 1}
            ],
            "financial_status": "paid",
            "transactions": [{
                "kind": "sale",
                "status": "success",
                "amount": "59.90",
                "gateway": "manual"
            }],
            "billing_address": {
                "first_name": first_name,
                "last_name": last_name,
                "address1": "123 Rue Saint-Paul",
                "city": "Montréal",
                "province": "QC",
                "country": "Canada",
                "zip": "H2X 1X1"
            },
            "send_receipt": False,
            "send_fulfillment_receipt": False
        }
    }

    url = f"https://{SHOP_URL}/admin/api/{API_VERSION}/orders.json"
    r = requests.post(url, json=order, headers=HEADERS, timeout=30)

    if r.status_code in (200, 201):
        print(f"[{datetime.now(TZ).strftime('%H:%M:%S')}] ✅ Commande créée : {email} ({first_name} {last_name})")
        return 59.90
    else:
        print(f"[{datetime.now(TZ).strftime('%H:%M:%S')}] ❌ {r.status_code} - {r.text}")
        return 0.0

def run_bot():
    missing = [k for k, v in {
        "SHOP_URL": SHOP_URL, "SHOPIFY_ACCESS_TOKEN": SHOPIFY_ACCESS_TOKEN, "VARIANT_ID": VARIANT_ID
    }.items() if not v]
    if missing:
        print("⛔ Variables manquantes :", ", ".join(missing))
        return

    total_revenue = 0.0
    revenue_target = 4000.0  # Objectif fixe : 4k CA/jour
    print(f"🎯 Objectif du jour : {revenue_target}$ | Boutique: {SHOP_URL}")

    while total_revenue < revenue_target:
        now = datetime.now(TZ)
        if 9 <= now.hour <= 21:
            if random.random() < 0.75:
                total_revenue += create_paid_order()
                print(f"📈 Revenu actuel : {round(total_revenue, 2)}$ / {revenue_target}$")

        pause = random.randint(300, 1200)  # entre 5 et 20 min
        print(f"⏱ Pause de {pause//60} min...\n")
        time.sleep(pause)

if __name__ == "__main__":
    run_bot()
