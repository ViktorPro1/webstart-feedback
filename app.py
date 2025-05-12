from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Дані пошти (встановлюються як змінні середовища на Render)
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = "webstartstudio978@gmail.com"

@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    data = request.json
    name = data.get('name')
    viber = data.get('viber')
    email = data.get('email')
    telegram = data.get('telegram')
    message = data.get('message')

    subject = f"Зворотній зв'язок від {name}"
    body = f"""
    Ім'я: {name}
    Вайбер: {viber}
    Email: {email}
    Telegram: {telegram}
    Повідомлення: {message}
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return jsonify({"success": True, "message": "Повідомлення надіслано."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run()

