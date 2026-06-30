import os
import threading
from mcrcon import MCRcon
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

# ---------------- НАСТРОЙКИ ----------------

TOKEN = os.environ.get("BOT_TOKEN")

RCON_HOST = os.environ.get("RCON_HOST")
RCON_PORT = int(os.environ.get("RCON_PORT"))
RCON_PASSWORD = os.environ.get("RCON_PASSWORD")

# ---------------- КОМАНДЫ БОТА ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я AI-помощник сервера Minecraft.\n"
        "Пока я умею базовые команды."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Сервер работает ✅\n"
        "ИИ-помощник онлайн 🤖"
    )

async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            result = mcr.command("list")

        await update.message.reply_text(
            f"📋 Ответ сервера:\n{result}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка подключения:\n{e}"
        )

# ---------------- ЗАПУСК БОТА ----------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("list", list_players))

print("Бот запущен!")

app.run_polling()
