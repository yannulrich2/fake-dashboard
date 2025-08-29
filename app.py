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

# ---- OBJECTIF DE VENTES ----
DAILY_TARGET_MIN = 3000
DAILY_TARGET_MAX = 5500

# ---- NOMS / EMAILS FAKE ----
first_names = [
    "Camille", "Léa", "Manon", "Sophie", "Inès", "Clara", "Nina", "Élise", "Sarah", "Emma",
    "Isabelle", "Aurélie", "Chloé", "Océane", "Anaïs", "Laura", "Valérie", "Mélanie",
    "Aisha", "Fatima", "Priya", "Ananya", "Kiran",  # Indien / Afrique
    "Maria", "Carmen", "Isabella", "Sofia", "Lucia",  # Espagnol
    "Aminata", "Awa", "Nadia", "Yasmina", "Mariam"   # Afrique
]

last_names = [
    "Dubois", "Lefevre", "Morel", "Fournier", "Lambert", "Rousseau", "Blanc", "Garnier",
    "Lopez", "Martinez", "Rodriguez", "Fernandez",   # Espagnol
    "Singh", "Patel", "Kumar", "Sharma",             # Indien
    "Diop", "Traoré", "Konaté", "Sylla", "Diallo"    # Afrique
]

email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com"]

# ---- FAKE SESSIONS (2k–6k / jour avec pause 5–20 min) ----
def _tick_fake_sessions():
    # Avec ~115 cycles/jour (pause moyenne ~12.5 min),
    # +40 sessions/cycle ≈ 4.6k sessions/jour
    return random.randint(20, 60)

# ---- VARIABLES GLOBALES ----
current_revenue = 0
current_sessions = 0
daily_target = random.randint(DAILY_TARGET_MIN, DAILY_TARGET_MAX)

# ---- FONCTION POUR FAIRE UNE FAUSSE COMMANDE ----
def create_fake_order():
    first = random.choice(first_names)
    last = random.choice(last_names)
    email = f"{first.lower()}.{last.lower()}@{random.choice(email_domains)}"

    order = {
        "order": {
            "line_items": [
                {
                    "variant_id": VARIANT_ID,
                    "quantity": random.randint(1, 3)
                }
            ],
            "customer": {
                "first_name": first,
                "last_name": last,
                "email": email
            }
        }
    }

    try:
        response = requests.post(
            f"https://{SHOP_URL}/admin/api/2024-01/orders.json",
            json=order,
            headers=HEADERS
        )
        if response.status_code == 201:
            return True
        else:
            print(f"❌ Erreur Shopify: {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ Exception: {e}")
        return False

# ---- FONCTION PRINCIPALE ----
def run_bot():
    global current_revenue, current_sessions

    print(f"🎯 Objectif du jour : {daily_target} $ (revenu entre {DAILY_TARGET_MIN}-{DAILY_TARGET_MAX})")

    while True:
        # --- Sessions fake ---
        added_sessions = _tick_fake_sessions()
        current_sessions += added_sessions

        # --- Revenus fake ---
        added_revenue = random.randint(50, 200)
        current_revenue += added_revenue

        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"📈 Revenu actuel : {current_revenue} $ — {current_sessions} sessions")

        # Optionnel : simuler aussi des commandes Shopify
        # success = create_fake_order()

        # Pause aléatoire entre 5 et 20 minutes
        time.sleep(random.randint(300, 1200))

if __name__ == "__main__":
    run_bot()
