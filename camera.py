import os
from datetime import datetime
from picamera2 import Picamera2
from conf import PHOTOS_DIR, PHOTO_SIZE
from logger import logger

def setup_camera():
    try:
        if not os.path.exists(PHOTOS_DIR):
            os.makedirs(PHOTOS_DIR)
        cam = Picamera2()
        config = cam.create_still_configuration(main={"size": (1920, 1080)})
        cam.configure(config)
        cam.start()
        return cam
    except Exception as e:
        logger.error(f"Fail when setup camera {e}")


def take_photo(cam):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(PHOTOS_DIR, f"{timestamp}.jpg")
    try:
        cam.capture_file(filename)
        logger.info(f"Фотография сохранена в {filename}")
        if os.path.exists(filename):
            logger.debug(f"Файл {filename} существует")
        else:
            logger.error(f"Ошибка: файл {filename} не найден")
        return filename
    except Exception as e:
        logger.error(f"Fail when capture image {e}")

#cam = setup_camera()
#take_photo(cam)
