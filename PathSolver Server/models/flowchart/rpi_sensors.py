import sys
import time
import datetime
import math

sys.path.append('PathSolver Server/models/flowchart/dht11.py')
import RPi.GPIO as GPIO
import dht11

# tempo di attesa tra una lettura e la successiva in caso di letture non valide
retry_delay = 1

#numero massimo di tentativi per leggere correttamente prima di lanciare un errore
max_retry = 10

class RPiConfigs(object):

    def __init__(self, moisture_temp_sensor_pin=17):
        self.moisture_temp_pin = moisture_temp_sensor_pin
        self.moisture_sensor_instance = dht11.DHT11(pin=moisture_temp_sensor_pin)

        # initialize GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

    # read temperature in Celsius degrees from the sensor
    def read_temperature(self):
        # TODO migliorare questo controllo -> se il sensore non è in grado di
        # TOOO realizzare una registrazione valida interrompere e restituire un codice di errore
        while True:
            result = self.moisture_sensor_instance.read()
            if result.is_valid():
                return str(datetime.datetime.now()), self.moisture_sensor_instance.read().temperature
            else:
                time.sleep(retry_delay)

    # read relative humidity from the sensor
    def read_humidity(self):
        while True:
            result = self.moisture_sensor_instance.read()
            if result.is_valid():
                return str(datetime.datetime.now()), self.moisture_sensor_instance.read().humidity
            else:
                time.sleep(retry_delay)
