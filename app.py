import os
import random
import time
import requests
from dotenv import load_dotenv
from datetime import datetime
import zoneinfo  # nécessite 'tzdata' dans requirements

# Charger les variables d'environnement
load_dotenv()

SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")  # ex: shpat_xxx
SHOP_URL = os.getenv("SHOP_URL")  # ex: tonstore.myshopify.com
# VARIANT_ID laissé optionnel si plus tard tu veux réactiver des trucs côté produit (non utilisé ici)
VARIANT_ID = os.getenv("VARIANT_ID")

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN or "",
    "Content-Type": "application/json"
}

# ---- OBJECTIF DE VENTES ----
DAILY_TARGET_MIN = 3000
DAILY_TARGET_MAX = 5500

# ---- NOM/EMAILS (gardés si tu veux les réutiliser ailleurs dans l'affichage)
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
    return first, last, email

# ---- FAKE SESSIONS (≈ 2k–6k / jour avec pause 5–20 min) ----
def _tick_fake_sessions():
    # ~115 cycles/jour si pause moyenne 12.5 min ; 20–60 / cycle ≈ ~4.6k/jour
    return random.randint(20, 60)

# ---- Shopify: check token/store (lecture seule) ----
def check_shopify():
    if not SHOP_URL or not SHOPIFY_ACCESS_TOKEN:
        print("🔐 Shopify check: variables manquantes (SHOP_URL/SHOPIFY_ACCESS_TOKEN)")
        return False
    try:
        url = f"https://{SHOP_URL}/admin/api/2024-01/shop.json"
        r = requests.get(url, headers=HEADERS, timeout=20)
        ok = (r.status_code == 200)
        print(f"🔐 Shopify check: {r.status_code} {'OK' if ok else r.text[:120]}")
        return ok
    except Exception as e:
        print("🔐 Shopify check exception:", e)
        return False

# ---- Shopify: lire les stats du jour (lecture seule) ----
def fetch_today_stats():
    """
    Retourne (orders_count, revenue_sum_float) pour AUJOURD'HUI (heure America/Toronto),
    uniquement commandes non annulées et 'paid'/'partially_paid'.
    """
    if not SHOP_URL or not SHOPIFY_ACCESS_TOKEN:
        return 0, 0.0

    tz = zoneinfo.ZoneInfo("America/Toronto")
    start = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    iso = start.isoformat()

    url = (
        f"https://{SHOP_URL}/admin/api/2024-01/orders.json"
        f"?status=any&created_at_min={iso}"
        f"&limit=250&fields=total_price,financial_status,cancelled_at"
    )

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print("❌ Orders read error:", r.status_code, r.text[:200])
            return 0, 0.0
        orders = r.json().get("orders", [])
        count = 0
        revenue = 0.0
        for o in orders:
            if o.get("cancelled_at"):
                continue
            if o.get("financial_status") in ("paid", "partially_paid"):
                count += 1
                try:
                    revenue += float(o.get("total_price", 0) or 0)
                except:
                    pass
        return count, round(revenue, 2)
    except Exception as e:
        print("⚠️ Exception lecture Shopify:", e)
        return 0, 0.0

def run_bot():
    # objectifs et compteurs
    daily_target = random.randint(DAILY_TARGET_MIN, DAILY_TARGET_MAX)
    fake_sessions = 0

    print(f"🎯 Objectif du jour (CA) : {daily_target} $ (plage {DAILY_TARGET_MIN}-{DAILY_TARGET_MAX})")

    # vérif Shopify (affiche juste le statut)
    check_shopify()

    # boucle continue (pas de restriction d'heure)
    while True:
        # sessions fictives
        fake_sessions += _tick_fake_sessions()

        # lecture réelle Shopify (lecture seule)
        orders_today, revenue_today = fetch_today_stats()

        # progression vers l'objectif (si 0 on affiche 0%)
        progress = (revenue_today / daily_target * 100) if daily_target > 0 else 0.0

        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"👥 Sessions(fake): {fake_sessions} | 🧾 Cmds réelles: {orders_today} | "
            f"CA réel: {revenue_today} $ | Progress: {progress:.1f}% de {daily_target} $"
        )

        # pause 5–20 min (modifie ici pour tester plus vite)
        pause = random.randint(300, 1200)
        print(f"⏱ Pause de {pause // 60} min...\n")
        time.sleep(pause)

if __name__ == "__main__":
    run_bot()
