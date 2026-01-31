import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Initialize Flask
app = Flask(__name__)

# 2. Setup Telegram Bot (v20.x+)
TOKEN = os.getenv("TELEGRAM_TOKEN") # Ensure this matches your Render Env Var name
tg_app = Application.builder().token(TOKEN).build()

# Define the /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Ameena is officially live and responding.")

tg_app.add_handler(CommandHandler("start", start))

# 3. The Webhook Route
@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle incoming Telegram updates by putting them into the PTB queue."""
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), tg_app.bot)
        await tg_app.process_update(update)
        return "OK", 200

@app.route('/')
def index():
    return "Bot is running...", 200

# 4. Critical: Initialize the Bot logic before Gunicorn handles requests
async def setup_bot():
    await tg_app.initialize()
    await tg_app.start()

# This runs once when the app starts
asyncio.run(setup_bot())
