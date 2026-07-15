import time
import requests
from telegram import Bot
from config import BOT_TOKEN, CHAT_ID, FUNDING_LIMIT, PRICE_CHANGE_LIMIT, CHECK_INTERVAL

bot = Bot(token=BOT_TOKEN)

# Son gönderilen uyarıları sakla
last_alert = {}

BINANCE_PREMIUM = "https://fapi.binance.com/fapi/v1/premiumIndex"
BINANCE_TICKER = "https://fapi.binance.com/fapi/v1/ticker/24hr"


def send_message(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text)
        print("Telegram mesajı gönderildi.")
    except Exception as e:
        print("Telegram Hatası:", e)


def get_funding():
    try:
        data = requests.get(BINANCE_PREMIUM, timeout=15).json()

        funding = {}

        for coin in data:

            symbol = coin["symbol"]

            rate = float(coin["lastFundingRate"])

            funding[symbol] = rate

        return funding

    except Exception as e:
        print(e)
        return {} 
def get_price_changes():
    try:
        data = requests.get(BINANCE_TICKER, timeout=15).json()

        changes = {}

        for coin in data:

            symbol = coin["symbol"]

            try:
                change = float(coin["priceChangePercent"])
            except:
                change = 0

            changes[symbol] = change

        return changes

    except Exception as e:
        print(e)
        return {}


def check_market():

    funding = get_funding()

    changes = get_price_changes()

    for symbol in funding:

        if symbol not in changes:
            continue

        rate = funding[symbol]

        price_change = changes[symbol]

        # Funding filtresi
        if rate > FUNDING_LIMIT:
            continue

        # 24 saat fiyat filtresi
        if price_change < PRICE_CHANGE_LIMIT:
            continue

        # Aynı coin için tekrar bildirim gönderme
        now = time.time()

        if symbol in last_alert:

            if now - last_alert[symbol] < 3600:
                continue

        text = (
            "🚨 Funding Alarmı\n\n"
            f"Coin: {symbol}\n"
            f"Funding: {rate*100:.3f}%\n"
            f"24s Değişim: %{price_change:.2f}"
        )

        send_message(text)

        last_alert[symbol] = now
      def main():

    send_message("✅ Funding Bot başlatıldı.")

    while True:

        try:

            check_market()

        except Exception as e:

            print("Hata:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":

    main()
