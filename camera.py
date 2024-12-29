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
        config = cam.create_still_configuration(lores={"size": PHOTO_SIZE})
        cam.configure(config)  # Применяем конфигурацию к камере
        cam.start()
        return cam

    except Exception as e:
        logger.error(f"Fail when setup camera {e}")


# TODO: не сохраняет файлы фоток в папку.
def capture_image(cam):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(PHOTOS_DIR, f"{timestamp}.jpg")
    try:
        cam.capture_file(filename)
        logger.debug(f"Фотография сохранена в {filename}")
        logger.info(f"Сфотографировано")

        if os.path.exists(filename):
            logger.debug(f"Файл {filename} существует")
        else:
            logger.error(f"Ошибка: файл {filename} не найден")

        return filename
    except Exception as e:
        logger.error(f"Fail when capture image {e}")


#capture_image(setup_camera())
