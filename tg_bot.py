# telegram_bot.py
import telebot
from conf import USER_CHAT_IDs, MEASUREMENT_INTERVAL, PHOTO_PATH
from TOKEN import TOKEN
from time import sleep
from threading import Thread
from camera import Camera
from bme_280 import BME280Sensor
from logger import logger

bot = telebot.TeleBot(TOKEN)
camera = Camera()
sensor = BME280Sensor()

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Бот запущен! Будет отправляться информация о влажности и снимок Бокелы каждые 30 минут.")
    start_sending_data(message.chat.id)
    logger.info()

def start_sending_data(chat_id):
    while True:
        try:
            temperature, humidity, pressure = sensor.get_data()
            camera.take_photo(PHOTO_PATH)

            message = (
                f"🌡️ Температура: {temperature:.2f}°C\n"
                f"💧 Влажность: {humidity:.2f}%\n"
                f"📊 Давление: {pressure:.2f} гПа\n"
            )

            with open(PHOTO_PATH, 'rb') as photo:
                bot.send_photo(chat_id=chat_id, photo=photo, caption=message)

            sleep(MEASUREMENT_INTERVAL)
        except Exception as e:
            print(f"Ошибка: {e}")
            sleep(60)

def run_bot():
    bot.infinity_polling()
