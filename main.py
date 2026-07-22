import time
import requests

# =====================
# AYARLAR
# =====================

BOT_TOKEN = "8881582255:AAGDldtAsDtJ-2m7MWDeQW8RWG6KeDAs8_A"
CHAT_ID = "-1004346379498"

FUNDING_LIMIT = -0.001      # -0.10%
PRICE_LIMIT = 5.0           # %5
CHECK_INTERVAL = 30         # 30 saniye

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

old_funding = {}

# =====================
# TELEGRAM
# =====================

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

# =====================
# FUNDING
# =====================

def funding_data():

    url = "https://fapi.binance.com/fapi/v1/premiumIndex"

    r = requests.get(url, timeout=15)

    data = r.json()

    result = {}

    for coin in data:
        try:
            result[coin["symbol"]] = float(coin["lastFundingRate"])
        except:
            pass

    return result

# =====================
# FİYAT
# =====================

def ticker_data():

    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"

    r = requests.get(url, timeout=15)

    data = r.json()

    result = {}

    for coin in data:
        try:
            result[coin["symbol"]] = float(coin["priceChangePercent"])
        except:
            pass

    return result

# =====================
# KONTROL
# =====================

def check_market():

    global old_funding

    funding = funding_data()
    ticker = ticker_data()

    print("Kontrol edildi")

    for symbol in funding:

        if symbol not in ticker:
            continue

        current = funding[symbol]

        previous = old_funding.get(symbol, current)

        change = current - previous

        old_funding[symbol] = current

        if current > FUNDING_LIMIT:
            continue

        if change >= 0:
            continue

        if ticker[symbol] < PRICE_LIMIT:
            continue

        mesaj = (
            f"🚨 {symbol}\n\n"
            f"Funding : {current:.4%}\n"
            f"Değişim : {change:.4%}\n"
            f"24s Fiyat : %{ticker[symbol]:.2f}"
        )

        print(mesaj)

        telegram(mesaj)

# =====================
# ANA DÖNGÜ
# =====================

print("BOT BASLADI")

telegram("✅ Bot çalışmaya başladı.")

while True:

    try:

        check_market()

    except Exception as e:

        print("HATA:", e)

    time.sleep(CHECK_INTERVAL)
