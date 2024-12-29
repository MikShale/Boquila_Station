import telebot
import threading
import time
from camera import setup_camera
from bme_280 import read_sensor_data, log_data_in_db
from conf import LOGS_DIR, TIME_FOR_SEND_DATA, TIME_FOR_SEND_LOGS
from logger import logger
from TOKEN import TOKEN
import os

bot = telebot.TeleBot(TOKEN)

# TODO: Может быть переписать как dict {user_id: [username, is_described, is_in_log]} ?
# Сейчас хранится как subscribers[user_id] = username
subscribers = {}
log_viewers = {}

camera = setup_camera()

def send_updates():
    """
    Отправляет данные по влажности давлению и температуре, а также фотографию бокелы для подписчиков /start
    """
    while True:
        if subscribers:
            temperature, humidity, pressure = read_sensor_data()
            photo_filename = camera.capture_image()

            # TODO: BUG! не сохраняет файлы фоток в папку, но пишет что сохраняет

            logger.debug(f"Фотография сохранена во время вызова функции send_updates")

            for user_id in list(subscribers):
                try:
                    bot.send_photo(
                        user_id, photo_filename,
                        f"🌡 Температура: {temperature}°C\n"
                        f"💧 Влажность: {humidity}%\n"
                        f"📈 Давление: {pressure} hPa\n",
                    )
                    logger.info(f"Информация отправлена подписчикам")
                except Exception as e:
                    logger.error(f"Ошибка при отправке данных пользователю {subscribers.get(user_id)}: {e}")
        time.sleep(TIME_FOR_SEND_DATA)

def send_logs():
    last_logs = ""
    while True:
        try:
            with open(os.path.join(LOGS_DIR, "logs.log"), "r") as log_file:
                current_logs = log_file.read()
                if current_logs != last_logs:
                    for user_id in log_viewers:
                        bot.send_message(user_id, f"📜 Новые логи:\n{current_logs[len(last_logs):]}")
                    last_logs = current_logs
                    logger.debug(f"Логи отправлены")
        except Exception as e:
            logger.error(f"Ошибка при отправке логов: {e}")
        time.sleep(TIME_FOR_SEND_LOGS)

@bot.message_handler(commands=["start"])
def handle_start(message):

    user_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name

    if user_id not in subscribers:
        subscribers[user_id] = username
        bot.send_message(user_id, "✅ Вы подписаны на обновления.")
        logger.info(f"Пользователь {username} подписался на обновления")
    else:
        bot.reply_to(message, "Вы уже подписаны на обновления.")

@bot.message_handler(commands=["stop"])
def handle_stop(message):
    user_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name
    subscribers.pop(user_id, None)
    log_viewers.pop(user_id, None)
    bot.send_message(user_id, "❌ Вы отписались от обновлений.")
    logger.info(f"Пользователь {username} отписался от обновлений")


@bot.message_handler(commands=["logs"])
def handle_logs(message):
    user_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name

    if user_id not in log_viewers:
        log_viewers[user_id] = username
        bot.send_message(user_id, "✅ Вы подписаны на логи.")
        logger.info(f"Пользователь {username} подписался на логи")
    else:
        bot.reply_to(message, "Вы уже подписаны на логи.")


def main():
    threading.Thread(target=log_data_in_db, daemon=True).start()  # Логирование в CSV
    threading.Thread(target=send_updates, daemon=True).start()    # Отправка обновлений
    threading.Thread(target=send_logs, daemon=True).start()       # Отправка логов
    logger.info("Потоки запущенны, бот запущен")
    bot.infinity_polling()  # Запуск бота
    logger.critical("Потоки остановлены, бот остановлен")


if __name__ == "__main__":
    main()
