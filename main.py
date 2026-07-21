import time
import requests

from config import *

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

price_history = {}
volume_history = {}
last_alert = {}

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
        print("Telegram Hatası:", e)


def market_data():

    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"

    data = requests.get(url, timeout=20).json()

    result = {}

    for coin in data:

        try:

            symbol = coin["symbol"]

            if not symbol.endswith("USDT"):
                continue

            price = float(coin["lastPrice"])

            volume = float(coin["quoteVolume"])

            result[symbol] = {
                "price": price,
                "volume": volume
            }

        except:
            pass

    return result


def check_market():

    global price_history
    global volume_history
    global last_alert

    market = market_data()

    now = time.time()

    for symbol in market:

        price = market[symbol]["price"]
        volume = market[symbol]["volume"]

        if symbol not in price_history:

            price_history[symbol] = []

            volume_history[symbol] = []

        price_history[symbol].append((now, price))

        volume_history[symbol].append((now, volume))

        while price_history[symbol] and now - price_history[symbol][0][0] > LOOKBACK_MINUTES * 60:

            price_history[symbol].pop(0)

        while volume_history[symbol] and now - volume_history[symbol][0][0] > LOOKBACK_MINUTES * 60:

            volume_history[symbol].pop(0)

        if len(price_history[symbol]) < 2:
            continue

        old_price = price_history[symbol][0][1]

        old_volume = volume_history[symbol][0][1]

        price_change = ((price - old_price) / old_price) * 100

        volume_change = volume / old_volume

        if price_change < PRICE_CHANGE_LIMIT:
            continue

        if volume_change < VOLUME_INCREASE:
            continue

        if symbol in last_alert:

            if now - last_alert[symbol] < 3600:
                continue

        last_alert[symbol] = now

        message = (
            f"🚀 GÜÇLÜ YÜKSELİŞ\n\n"
            f"🪙 {symbol}\n\n"
            f"📈 {LOOKBACK_MINUTES} dk: %{price_change:.2f}\n"
            f"📊 Hacim Artışı: x{volume_change:.2f}\n"
            f"💰 Fiyat: {price}\n"
        )

        telegram(message)

        print(message)


print("BOT BAŞLADI")

while True:

    try:

        check_market()

    except Exception as e:

        print("HATA:", e)

    time.sleep(CHECK_INTERVAL)
