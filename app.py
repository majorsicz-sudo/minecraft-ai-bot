import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------------- WEB SERVER ДЛЯ RENDER ----------------

web = Flask(__name__)

@web.route("/")
def home():
    return "Minecraft AI Bot работает!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ---------------- TELEGRAM BOT ----------------

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я AI-помощник сервера Minecraft.\n"
        "Пока умею базовые команды."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Сервер работает ✅\n"
        "ИИ-помощник онлайн 🤖"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("status", status))

print("Бот запущен!")

app.run_polling()
