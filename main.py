import time
import requests
print("MAIN DOSYASI ÇALIŞTI")
# Telegram
BOT_TOKEN = "8881582255:AAGDldtAsDtJ-2m7MWDeQW8RWG6KeDAs8_A"
CHAT_ID = "-1004346379498"

# Filtreler
FUNDING_LIMIT = -0.001      # -0.10%
PRICE_CHANGE_LIMIT = 5.0    # %5
CHECK_INTERVAL = 300

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

BINANCE_PREMIUM = "https://fapi.binance.com/fapi/v1/premiumIndex"
BINANCE_TICKER = "https://fapi.binance.com/fapi/v1/ticker/24hr"

last_alert = {}
old_funding = {}


def telegram(text):
    try:
        requests.post(
            TELEGRAM_URL,
            data={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=15
        )
    except Exception as e:
        print(e)


def funding_data():

    r = requests.get(BINANCE_PREMIUM, timeout=20)

    data = r.json()

    result = {}

    for coin in data:

        try:

            symbol = coin["symbol"]

            funding = float(coin["lastFundingRate"])

            result[symbol] = funding

        except:

            pass

    return result


def ticker_data():

    r = requests.get(BINANCE_TICKER, timeout=20)

    data = r.json()

    result = {}

    for coin in data:

        try:

            symbol = coin["symbol"]

            change = float(coin["priceChangePercent"])

            result[symbol] = change

        except:

            pass
          
    return result
def check_market():

    global old_funding

    funding = funding_data()
    ticker = ticker_data()

    for symbol in funding:

        if symbol not in ticker:
            continue

        current_funding = funding[symbol]
        price_change = ticker[symbol]

        previous_funding = old_funding.get(symbol, current_funding)
        funding_change = current_funding - previous_funding

        # Son funding değerini kaydet
        old_funding[symbol] = current_funding

        # Funding yeterince negatif değilse geç
        if current_funding > FUNDING_LIMIT:
            continue

        # Fiyat yeterince yükselmemişse geç
        if price_change < PRICE_CHANGE_LIMIT:
            continue

        # Funding daha negatife gitmemişse geç
        if funding_change >= 0:
            continue

        now = time.time()

        # Aynı coin için 1 saat içinde tekrar bildirim gönderme
        if symbol in last_alert:
            if now - last_alert[symbol] < 3600:
                continue

        message = (
            "🚨 FUNDING ALARMI 🚨\n\n"
            f"Coin: {symbol}\n"
            f"Funding: {current_funding*100:.4f}%\n"
            f"Önceki Funding: {previous_funding*100:.4f}%\n"
            f"Değişim: {funding_change*100:.4f}%\n"
            f"24 Saat: %{price_change:.2f}"
        )

        telegram(message)
        last_alert[symbol] = now


def main():
    print("MAIN ÇALIŞTI")
    telegram("🚀 Funding Bot başlatıldı.")

    while True:
        try:
            print("check_market çağrılıyor")
            check_market()
        except Exception as e:
            print("Hata:", repr(e))

        time.sleep(CHECK_INTERVAL)


print("BOT BAŞLIYOR")
if __name__ == "__main__":
    main()
