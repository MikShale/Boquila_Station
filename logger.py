import logging
import colorlog


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
logger.addHandler(console)

#файловый обработчик
file_handler = logging.FileHandler("logs.log", mode="w")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
logger.addHandler(file_handler)
