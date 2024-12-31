import board
import time
import adafruit_bme280.advanced as adafruit_bme280
import csv
from datetime import datetime
from CONST import BME280_CSV_DATA, TIME_FOR_LOG_IN_DB
from logger import logger
import os

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# TODO: Сделать API запрос текущего давления на уровне моря
bme280.sea_level_pressure = 1013.25  # в гПа
bme280.mode = adafruit_bme280.MODE_NORMAL

# TODO: Надо сделать через MODE_SLEEP, чтобы датчик просыпался каждый раз при запросе
bme280.standby_period = adafruit_bme280.STANDBY_TC_1000

# Максимальная степепень сглаживания и максимальная передискретизация = максимальная точность
bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X16
bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X16


def initialize_csv():
    if not os.path.exists(BME280_CSV_DATA):
        with open(BME280_CSV_DATA, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Temperature (C)", "Humidity (%)", "Pressure (mmHg)"])
            logger.debug(f"СSV сконфигурирован")
    else: logger.debug(f"СSV существует")

def read_sensor_data():
    try:
        temperature = round(bme280.temperature, 1)
        humidity = round(bme280.relative_humidity, 1)
        pressure = round(3 * bme280.pressure / 4, 1)
        return temperature, humidity, pressure

    except Exception as e:
        logger.error(f"Fail to read sensor data: {e}")
        return None

def log_data_in_db():
    while True:
        temperature, humidity, pressure = read_sensor_data()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(BME280_CSV_DATA, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temperature, humidity, pressure])
        logger.debug(
            f"Записанно в БД: Temperature: {temperature}°C, Humidity: {humidity}%, Pressure: {pressure} mmHg"
        )
        time.sleep(TIME_FOR_LOG_IN_DB)

