from flask import Flask, request
import requests

app = Flask(__name__)

# Токен Telegram бота
TOKEN = "7504062714:AAG5hueraKvmcnK9_eQdpx_ydpssjUu8Wvg"

# ID групи (обов’язково з "-" перед ID)
CHAT_ID = "-4637345808"


# Функція для відправки повідомлення в Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.get(url, params=payload)
    return response.json()


# Основний маршрут для Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # Отримуємо JSON від TradingView
    if not data:
        return {"error": "Empty request"}, 400

    # Формуємо повідомлення
    message = f"""
📊 Торговий сигнал:
🔹 Символ: {data.get('symbol', 'N/A')}
📈 Дія: {data.get('side', 'N/A')}
📦 Кількість: {data.get('qty', 'N/A')}
💲 Ціна: {data.get('price', 'N/A')}
⏳ Час тригеру: {data.get('trigger_time', 'N/A')}
    """.strip()

    # Відправляємо у Telegram
    response = send_telegram_message(message)
    return response


# Запускаємо сервер
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)