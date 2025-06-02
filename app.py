from flask import Flask, render_template, request, redirect, session
import sqlite3
import random
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # change if you want

# Your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "8109824078:AAGAraEYqlRLdGmHNqX2yjB-LTKbnCksJvg"
TELEGRAM_CHAT_ID = "5116463638"  # Your Telegram user chat ID

# Sweet messages to comfort her 💌
messages = [
    "Alok shall weave your words into actions, my moon 🌙",
    "Your wish is my command, my Queen 👑",
    "This knight of yours rides now to fix it! 🐎",
    "Hold on, my angel — your warrior is on it 💘",
    "Even your sighs echo in my heart, and this one shall be healed 💭",
    "Storms you send, I calm with love ⛅",
    "One grievance closer to our forever harmony 💑",
    "You grieve, I move mountains — metaphorically and lovingly ⛰️",
    "Alok's on it like Romeo chasing Juliet 🏹",
    "Oh love, thy concern shall perish like the night at sunrise 🌅"
]

# Initialize DB
def init_db():
    with sqlite3.connect("grievance.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS grievances (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            message TEXT NOT NULL,
                            created_at TEXT NOT NULL
                        );''')

init_db()

def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        }
        response = requests.post(url, json=payload)
        print("Telegram Response:", response.text)
        return response.status_code == 200
    except Exception as e:
        print("Telegram Error:", e)
        return False

@app.route("/")
def index():
    with sqlite3.connect("grievance.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM grievances ORDER BY created_at DESC")
        grievances = cur.fetchall()
    love_note = session.pop('love_note', None)
    return render_template("index.html", grievances=grievances, love_note=love_note)

@app.route("/submit", methods=["POST"])
def submit():
    message = request.form.get("message")
    if message:
        with sqlite3.connect("grievance.db") as conn:
            conn.execute("INSERT INTO grievances (message, created_at) VALUES (?, ?)",
                         (message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        session['love_note'] = random.choice(messages)

        # Send Telegram alert with grievance message
        send_telegram_message(f"New grievance from my love 💌:\n\n{message}")

    return redirect("/")

@app.route("/admin")
def admin():
    with sqlite3.connect("grievance.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM grievances ORDER BY created_at DESC")
        grievances = cur.fetchall()
    return render_template("admin.html", grievances=grievances)

if __name__ == '__main__':
    app.run(debug=True)
