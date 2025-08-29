import os
import random
import time
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Charger les variables d'environnement
load_dotenv()

SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOP_URL = os.getenv("SHOP_URL")
VARIANT_ID = os.getenv("VARIANT_ID")

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# ============================
# Stats Shopify réelles
# ============================
_cache = {"timestamp": None, "orders": 0, "revenue": 0.0}

def fetch_today_stats(cache_seconds=120):  # <-- augmenté de 60 à 120
    """Récupère les commandes réelles du jour avec cache pour éviter l'erreur 429"""
    now = datetime.utcnow()
    if _cache["timestamp"] and (now - _cache["timestamp"]).seconds < cache_seconds:
        return _cache["orders"], _cache["revenue"]

    try:
        today = datetime.utcnow().strftime("%Y-%m-%dT00:00:00Z")
        url = f"https://{SHOP_URL}/admin/api/2023-10/orders.json"
        params = {"status": "any", "created_at_min": today}
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code == 200:
            data = response.json()
            orders = len(data.get("orders", []))
            revenue = sum(float(o["total_price"]) for o in data.get("orders", []))
            _cache.update({"timestamp": now, "orders": orders, "revenue": revenue})
            return orders, revenue
        else:
            print(f"❌ Orders read error: {response.status_code} {response.text}")
            return _cache["orders"], _cache["revenue"]
    except Exception as e:
        print(f"❌ Exception orders: {e}")
        return _cache["orders"], _cache["revenue"]

# ============================
# Fake Sessions + Objectifs
# ============================
def generate_fake_sessions():
    return random.randint(20, 80)

def generate_sales_goal():
    return random.randint(3000, 5500)

# ============================
# Main Loop
# ============================
if __name__ == "__main__":
    objectif = generate_sales_goal()
    print(f"🎯 Objectif du jour (CA) : {objectif} $ (plage 3000-5500)")

    # Test connexion Shopify
    test_url = f"https://{SHOP_URL}/admin/api/2023-10/shop.json"
    test_resp = requests.get(test_url, headers=HEADERS)
    if test_resp.status_code == 200:
        print("🔐 Shopify check: 200 OK")
    else:
        print(f"🔐 Shopify check FAILED: {test_resp.status_code}")

    while True:
        # Stats Shopify
        orders, revenue = fetch_today_stats()

        # Fake sessions
        fake_sessions = generate_fake_sessions()

        # Progression
        progress = round((revenue / objectif) * 100, 1) if objectif > 0 else 0

        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"👥 Sessions(fake): {fake_sessions} | 🧾 Cmds réelles: {orders} | "
              f"CA réel: {revenue:.2f} $ | Progress: {progress}% de {objectif} $")

        # 🔑 Pause fixée à 60 sec pour éviter l'erreur 429
        time.sleep(60)
