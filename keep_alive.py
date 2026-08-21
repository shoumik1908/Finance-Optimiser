"""
Keep-alive script for Render free tier.
Pings the app every 10 minutes to prevent spin-down.
Run in background: python keep_alive.py
"""
import time
import urllib.request

URL = "https://finance-optimiser.onrender.com/"
INTERVAL = 600  # 10 minutes

print(f"Keep-alive started. Pinging {URL} every {INTERVAL//60} minutes...")

while True:
    try:
        req = urllib.request.Request(URL, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=10)
        print(f"[{time.strftime('%H:%M:%S')}] Status: {resp.status}")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Error: {e}")
    time.sleep(INTERVAL)
