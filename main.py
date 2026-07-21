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
    print(error)


def on_close(ws, code, msg):
    print("KAPANDI")


ws = websocket.WebSocketApp(
    "wss://fstream.binance.com/ws/!miniTicker@arr",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)

ws.run_forever()
