from tg_bot import run_bot
from threading import Thread

if __name__ == '__main__':
    thread = Thread(target=run_bot)
    thread.daemon = True
    thread.start()

    print("Бот запущен!")
    thread.join()
