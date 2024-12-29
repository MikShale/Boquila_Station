import logging
import os.path
from conf import LOGS_DIR
import colorlog

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

#TODO: добавить вывод основных логов в systemd

logger = logging.getLogger(__name__)

formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s  - %(levelname)s:%(message)s',
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

logger.setLevel(logging.DEBUG)

#консольный обработчик
console = logging.StreamHandler()
console.setFormatter(formatter)


#файловый обработчик
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "logs.log"), mode="a")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))

if not logger.hasHandlers():
    logger.addHandler(console)
    logger.addHandler(file_handler)