print("TEST 123456")
import json
import websocket

def on_open(ws):
    print("WEBSOCKET BAGLANDI")


def on_message(ws, message):
    data = json.loads(message)

    print("VERI GELDI")

    if isinstance(data, list) and len(data) > 0:
        coin = data[0]
        print(coin)


def on_error(ws, error):
    print("HATA:", repr(error))


def on_close(ws, code, msg):
    print(f"KAPANDI code={code} msg={msg}")


ws = websocket.WebSocketApp(
    "wss://fstream.binance.com/ws/!miniTicker@arr",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)

ws.run_forever(
    ping_interval=20,
    ping_timeout=10
)
