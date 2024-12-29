import smbus2
from Adafruit_BME280 import BME280
from conf import BME280_I2C_ADDRESS, BME280_I2C_BUS

class BME280Sensor:
    def __init__(self):
        self.bus = smbus2.SMBus(BME280_I2C_BUS)
        self.bme280 = BME280(i2c_dev=self.bus, address=BME280_I2C_ADDRESS)

    def get_data(self):
        # Получаем данные с датчика
        temperature = self.bme280.get_temperature()
        humidity = self.bme280.get_humidity()
        pressure = self.bme280.get_pressure()
        return temperature, humidity, pressure
