import logging
import os.path
from CONST import LOGS_DIR
import colorlog
from logging.handlers import SysLogHandler

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logger = logging.getLogger(__name__)

formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s  - %(levelname)s:%(message)s',
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'light_red',
    },
    secondary_log_colors={},
    style='%'
)

logger.setLevel(logging.DEBUG)

#консольный обработчик
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)

#файловый обработчик
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "logs.log"), mode="a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

#обработчик syslog (systemd)
syslog_handler = SysLogHandler(address='/dev/log')
syslog_handler.setLevel(logging.INFO)
syslog_handler.setFormatter(formatter)


# TODO: BUG: Debug все равно выводится в systemd
if not logger.hasHandlers():
    logger.addHandler(console)
    logger.addHandler(file_handler)
    logger.addHandler(syslog_handler)
