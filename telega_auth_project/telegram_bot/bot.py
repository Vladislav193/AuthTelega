import os
import django
import requests

from telegram import Update
from telegram.ext import CommandHandler, Updater, Application, ContextTypes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telega_auth_project.settings')
django.setup()

DJANGO_URL = 'http://127.0.0.1:8000/auth/telegram/'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = context.args[0] if context.args else None
    if token:
        response = requests.post(DJANGO_URL, json={
            'telegram_id': update.effective_user.id,
            'telegram_username': update.effective_user.username,
            'auth_token': token
        })
        if response.status_code == 200:
            await update.message.reply_text("Вы успешно авторизовались!")
        else:
            await update.message.reply_text("Ошибка авторизации.")
    else:
        await update.message.reply_text("Токен не найден.")

def main():
    application = Application.builder().token("7850783193:AAGXyY9fmFVVxgIKjLa4WxXhyi9VGe1ULcQ").build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()