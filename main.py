from flask import Flask, request
import requests

# Настройки
BOT_TOKEN = "8070908086:AAGUjDIPyfJRz7mA_szq-fSrHAPB1jlNEgE"
ADMIN_ID = "7823612290"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

app = Flask(__name__)

# Главная страница для проверки
@app.route("/")
def home():
    return "Bot is running!"

# Обработка веб-хуков
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    # Проверяем входящее сообщение
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        username = data["message"]["chat"].get("username", "Неизвестный")
        ip_address = request.remote_addr
        
        # Отправляем сообщение администратору
        message = (
            f"Новый пользователь!\n"
            f"Telegram ID: {chat_id}\n"
            f"Username: @{username}\n"
            f"IP-адрес: {ip_address}"
        )
        requests.post(TELEGRAM_API_URL, data={"chat_id": ADMIN_ID, "text": message})
        
        # Ответ пользователю
        requests.post(TELEGRAM_API_URL, data={"chat_id": chat_id, "text": "Добро пожаловать!"})
    
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
