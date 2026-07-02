import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ==========================
# НАСТРОЙКИ
# ==========================

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENWEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

# ==========================
# Команда /start
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Напишите название города на русском языке.\n\n"
        "Например:\n"
        "Москва\n"
        "Санкт-Петербург\n"
        "Казань"
    )

# ==========================
# Получение погоды
# ==========================

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={OPENWEATHER_API_KEY}"
        f"&units=metric"
        f"&lang=ru"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            await update.message.reply_text(
                "❌ Город не найден.\nПопробуйте написать название ещё раз."
            )
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind = data["wind"]["speed"]
        city_name = data["name"]

        text = (
            f"📍 Город: {city_name}\n\n"
            f"🌡 Температура: {temp}°C\n"
            f"☁️ Погода: {description.capitalize()}\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Ветер: {wind} м/с"
        )

        await update.message.reply_text(text)

    except Exception:
        await update.message.reply_text(
            "⚠️ Произошла ошибка при получении данных о погоде."
        )

# ==========================
# Запуск
# ==========================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
