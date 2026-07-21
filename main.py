import json
import websocket
import requests
import time

from config import *

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def telegram(text):
    try:
        requests.post(
            TELEGRAM_URL,
            data={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=10
        )
    except Exception as e:
        print(e)


sent = False


def on_open(ws):
    print("WebSocket Bağlandı")
    telegram("✅ Bot başladı\nWebSocket bağlandı.")


def on_message(ws, message):
    global sent

    data = json.loads(message)

    if not isinstance(data, list):
        return

    if len(data) == 0:
        return

    coin = data[0]

    symbol = coin.get("s")
    price = coin.get("c")

    print(symbol, price)

    if not sent:
        telegram(f"📡 İlk veri geldi\n\n{symbol}\nFiyat: {price}")
        sent = True


def on_error(ws, error):
    print("HATA:", error)
    telegram(f"❌ WebSocket Hatası\n{error}")


def on_close(ws, code, msg):
    print("Bağlantı kapandı")
    telegram("⚠️ WebSocket kapandı")

    time.sleep(5)

    start()


def start():
    ws = websocket.WebSocketApp(
        "wss://fstream.binance.com/ws/!miniTicker@arr",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()


print("BOT BAŞLIYOR...")

start()
