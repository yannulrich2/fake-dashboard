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

# Sécurité: DRY_RUN=1 (par défaut) => NE PAS créer de vraies commandes
DRY_RUN = os.getenv("DRY_RUN", "1") == "1"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Fonction pour créer une commande Shopify (ou simuler si DRY_RUN)
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

    # En mode DRY_RUN: on n'envoie rien à Shopify, on log juste
    if DRY_RUN:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚫 DRY_RUN actif — (simulation) Commande pour {email}")
        return True

    # ATTENTION: n'active pas ceci sur une boutique réelle
    response = requests.post(
        f"https://{SHOP_URL}/admin/api/2024-01/orders.json",
        json=order,
        headers=HEADERS,
        timeout=30
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
    if DRY_RUN:
        print("⚠️ DRY_RUN=1 — aucune commande réelle ne sera créée (test/log uniquement).")

    while total_revenue < revenue_target:
        # ✅ plus AUCUNE restriction d’heure — ça tourne dès le lancement

        # 75% de chances de “créer” une commande à chaque passage
        if random.random() < 0.75:
            success = create_fake_order()
            if success:
                total_revenue += price
                print(f"📈 Revenu actuel : {round(total_revenue, 2)} $ / {revenue_target} $")

        # 🔎 petite pause pour que tu voies la notif rapidement (5–10 sec)
        pause = random.randint(5, 10)
        print(f"⏱ Pause de {pause} sec avant prochaine tentative...\n")
        time.sleep(pause)

if __name__ == "__main__":
    run_bot()
