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

# --- Listes: majorité FR + mix international ---
FIRST_NAMES = [
    # Français(es) (majorité, surtout féminin)
    "Emma","Camille","Chloé","Juliette","Sarah","Manon","Léa","Anaïs","Claire","Sophie",
    "Élise","Océane","Inès","Lucie","Nina","Aurélie","Amélie","Élodie","Maëlys","Alicia",
    "Hugo","Lucas","Louis","Mathis","Théo","Clément","Jules","Antoine","Maxime","Alexandre",
    # Espagnols/Latins
    "Maria","Isabella","Valentina","Sofia","Camila","Gabriela","Alejandro","Diego","Carlos","Juan",
    # Africains
    "Awa","Aminata","Fatou","Mariam","Nadia","Zara","Khadija","Ibrahim","Ousmane","Moussa","Amadou","Yacine",
    # Indiens
    "Aarav","Arjun","Vihaan","Rohan","Ananya","Priya","Isha","Diya","Aditi","Saanvi"
]

LAST_NAMES = [
    # Français
    "Dubois","Lefevre","Moreau","Laurent","Girard","Roux","Noel","Fontaine","Chevalier","Barbier",
    "Perrin","Renard","Caron","Lemoine","Marchand","Bernard","Petit","Robert","Richard","Durand",
    # Espagnols/Latins
    "Garcia","Martinez","Lopez","Hernandez","Rodriguez","Sanchez","Fernandez","Diaz",
    # Africains
    "Traoré","Diop","Konaté","Coulibaly","N'Diaye","Ouattara","Bakayoko","Diallo","Sow","Keita",
    # Indiens
    "Sharma","Patel","Kumar","Gupta","Singh","Reddy","Chopra","Mehta"
]

EMAIL_PROVIDERS = [
    "gmail.com","outlook.com","yahoo.com","protonmail.com","icloud.com",
    "hotmail.com","aol.com","zoho.com","mail.com","gmx.com",
    "orange.fr","laposte.net","sfr.fr","free.fr"
]

def _generate_fake_identity():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    provider = random.choice(EMAIL_PROVIDERS)
    email = f"{first.lower()}.{last.lower()}{random.randint(1, 999)}@{provider}"
    return email

# Fonction pour créer une commande Shopify
def create_fake_order():
    email = _generate_fake_identity()

    order = {
        "order": {
            "email": email,
            "fulfillment_status": "fulfilled",
            "send_receipt": False,
            "send_fulfillment_receipt": False,
            "line_items": [
                {
                    "variant_id": int(VARIANT_ID),
                    "quantity": 1
                }
            ]
        }
    }

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
    missing = [k for k, v in {
        "SHOP_URL": SHOP_URL, "SHOPIFY_ACCESS_TOKEN": SHOPIFY_ACCESS_TOKEN, "VARIANT_ID": VARIANT_ID
    }.items() if not v]
    if missing:
        print("⛔ Variables manquantes :", ", ".join(missing))
        return

    total_revenue = 0.0
    revenue_target = random.randint(3000, 5000)  # objectif 3k–5k
    price = 49.99

    print(f"🎯 Objectif du jour : {revenue_target} $ | Boutique: {SHOP_URL}")

    # ⬇️ AUCUNE RESTRICTION D'HEURE : ça tourne direct et en continu
    while total_revenue < revenue_target:
        # 75% de chances de créer une commande à chaque passage
        if random.random() < 0.75:
            success = create_fake_order()
            if success:
                total_revenue += price
                print(f"📈 Revenu actuel : {round(total_revenue, 2)} $ / {revenue_target} $")

        # Pause entre 5 et 20 minutes
        pause = random.randint(300, 1200)
        print(f"⏱ Pause de {pause // 60} min avant prochaine tentative...\n")
        time.sleep(pause)

if __name__ == "__main__":
    run_bot()
