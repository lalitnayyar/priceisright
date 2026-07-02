"""
Direct test: send 2 great deal Pushover notifications using real keys.
Run from: /home/ubuntu/priceisright/priceisrightcapstone/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import requests
from datetime import datetime

PUSHOVER_USER  = "uqokrzf6ufdu6qjmbst9dcyz4191qh"
PUSHOVER_TOKEN = "a2k3z2e88z9fhyutq1pweqcdkus4cc"

# Two great deal examples from the current memory.json
deals = [
    {
        "title": "Sony WH-1000XM5 Wireless Headphones",
        "listed_price": 199.99,
        "estimated_price": 399.99,
        "discount_pct": 50.0,
        "url": "https://www.dealnews.com/sony-wh1000xm5",
    },
    {
        "title": "Samsung 65\" QLED 4K Smart TV",
        "listed_price": 799.99,
        "estimated_price": 1299.99,
        "discount_pct": 38.5,
        "url": "https://www.dealnews.com/samsung-qled-65",
    },
]

def send_pushover(deal: dict, priority: int = 0) -> bool:
    title = "🏷️ The Price Is Right — Deal Alert"
    msg = (
        f"🔥 {deal['title']}\n"
        f"Listed: ${deal['listed_price']:.2f}  |  Est. Value: ${deal['estimated_price']:.2f}\n"
        f"💰 {deal['discount_pct']:.1f}% OFF — Great Opportunity!\n"
        f"👉 Tap to view deal"
    )
    resp = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token":     PUSHOVER_TOKEN,
            "user":      PUSHOVER_USER,
            "title":     title,
            "message":   msg,
            "url":       deal["url"],
            "url_title": "View Deal →",
            "priority":  priority,
            "sound":     "pushover",
        },
        timeout=10,
    )
    result = resp.json()
    if result.get("status") == 1:
        print(f"  ✅ Sent: {deal['title']} ({deal['discount_pct']:.1f}% off)")
        return True
    else:
        print(f"  ❌ Failed: {result}")
        return False

print(f"\n{'='*60}")
print(f"  Price Is Right — Pushover Deal Notification Test")
print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*60}\n")

for i, deal in enumerate(deals, 1):
    print(f"[{i}/2] Sending notification for: {deal['title']}")
    priority = 1 if deal["discount_pct"] >= 50 else 0
    send_pushover(deal, priority=priority)

print(f"\n✅ Done — check your Pushover app!\n")
