raise Exception("YENI MAIN CALISTI")
import json
import websocket
import requests

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


count = 0


def on_message(ws, message):
    global count

    data = json.loads(message)

    if "data" not in data:
        return

    ticker = data["data"]

    symbol = ticker["s"]
    price = ticker["c"]

    count += 1

    print(symbol, price)

    if count == 1:
        telegram(f"✅ WebSocket Çalışıyor\n\n{symbol}\nFiyat: {price}")


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("Bağlantı kapandı")


def on_open(ws):
    print("WebSocket Bağlandı")


socket = "wss://fstream.binance.com/ws/!miniTicker@arr"

ws = websocket.WebSocketApp(
    socket,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)

ws.run_forever()
