import websocket

def on_open(ws):
    print("WEBSOCKET BAGLANDI")

ws = websocket.WebSocketApp(
    "wss://fstream.binance.com/ws/!miniTicker@arr",
    on_open=on_open
)

ws.run_forever()
