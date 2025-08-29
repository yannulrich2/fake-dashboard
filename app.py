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

# Fonction pour créer une commande Shopify
def create_fake_order():
    prenoms = ["Alex", "Emma", "Lucas", "Léa", "Noah", "Inès"]
    noms = ["Martin", "Bernard", "Robert", "Richard", "Petit", "Durand"]
    email = f"{random.choice(prenoms).lower()}.{random.choice(noms).lower()}{random.randint(100, 999)}@gmail.com"

    order = {
        "order": {
            "email": email,
            "fulfillment_status": "fulfilled",
            "send_receipt": False,
            "send_fulfillment_receipt": False,
            "line_items": [
                {
                    "variant_id": VARIANT_ID,
                    "quantity": 1
                }
            ]
        }
    }

    response = requests.post(
        f"https://{SHOP_URL}/admin/api/2024-01/orders.json",
        json=order,
        headers=HEADERS
    )

    if response.status_code == 201:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Commande créée avec {email}")
        return True
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Erreur : {response.status_code} - {response.text}")
        return False

# Fonction principale du bot
def run_bot():
    total_revenue = 0
    revenue_target = random.randint(3000, 5000)
    price = 59.90

    print(f"🎯 Objectif du jour : {revenue_target} $")

    while total_revenue < revenue_target:
        # Toujours actif (pas de restriction d’heure)
        if random.random() < 0.75:  # 75% de chances de créer une commande
            success = create_fake_order()
            if success:
                total_revenue += price
                print(f"📈 Revenu actuel : {round(total_revenue, 2)} $ / {revenue_target} $")

        # Pause rapide pour test
        pause = random.randint(10, 20)
        print(f"⏱ Pause de {pause} sec...\n")
        time.sleep(pause)

if __name__ == "__main__":
    run_bot()
