import sys
sys.path.insert(0, 'PathSolver Server/models/flowchart/dht11.py')
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import math


class RPiConfigs(object):

    def __init__(self, moisture_temp_sensor_pin = 17):
        self.moisture_temp_pin = moisture_temp_sensor_pin
        self.moisture_sensor_instance = dht11.DHT11(pin=moisture_temp_sensor_pin)

        # initialize GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

    # read temperature in Celsius degrees from the sensor
    def read_temperature(self):
        return str(datetime.datetime.now()), self.moisture_sensor_instance.read().temperature

    # read relative humidity from the sensor
    def read_humidity(self):
        return str(datetime.datetime.now()), self.moisture_sensor_instance.read().humidity

if __name__ == '__main__':
    rpi = RPiConfigs()
