import time
import json
import datetime
import sys
sys.path.insert(0, 'PathSolver Server/models/flowchart/rpi_sensors.py')

from rpi_sensors import RPiConfigs

# variabile che permette di decidere se si vuole utilizzare il programma
# come semplice simulazione, inserendo i valori a mano
# oppure utilizzando i sensori collegati al Raspberry (configurato in precedenza).
sensor_connected = False

# variabile che permette all'utente di decidere se salvare i dati registrati
# in un file esterno fruibile successivamente
log_data = True

# in ogni caso inizializzo una lista per loggare i dati
data = {}
log = []

# istanza della classe RaspberryConfigs
rpi = RPiConfigs()

# tolleranza
moisture_range = 2
temperature_range = 2
pressure_range = 2

# durata delay tra letture successive (in secondi)
casting_read_delay = 3
maturation_read_delay = 3

# valori attesi durante il getto
expected_moisture_casting = 70
expected_temperature_casting = 22
expected_pressure_casting = 10

# valori attesi a maturazione
expected_moisture_maturation = 50
expected_temperature_maturation = 22
expected_pressure_maturation = 20

# valori rilevati
current_moisture = 0.0
current_temperature = 0.0
current_pressure = 0.0


# controllo parametri durante la gettata
def check_moisture_casting():
    return current_moisture < abs(expected_moisture_casting - moisture_range)


def check_temperature_casting():
    return current_temperature < abs(expected_temperature_casting - temperature_range)


def check_pressure_casting():
    return current_pressure < abs(expected_pressure_casting - pressure_range)


# controllo parametri a gettata terminata
def check_moisture_maturation():
    return current_moisture < abs(expected_moisture_maturation - moisture_range)


def check_temperature_maturation():
    return current_temperature < abs(expected_temperature_maturation - temperature_range)


def check_pressure_maturation():
    return current_pressure < abs(expected_pressure_maturation - pressure_range)


# interroga i sensori del RaspberryPi per aggiornare i valori dei parametri da monitorare
def sensor_input_parameters():
    # TODO trovare soluzione per sensore di pressione
    detected_moisture = rpi.read_humidity()[1]
    detected_temperature = rpi.read_temperature()[1]
    detected_pressure = rpi.read_humidity()
    return detected_moisture, detected_temperature, detected_pressure


# chiede di inserire manualmente i parametri da monitorare
def user_input_parameters():
    input_moisture = input("Enter current moisture: ")
    input_temperature = input("Enter current temperature: ")
    input_pressure = input("Enter current pressure: ")
    return input_moisture, input_temperature, input_pressure


# aggiorna i parametri da monitorare secondo il canale prestabilito (manuale da utente o automatico da sensori)
def update_parameters():
    if sensor_connected:
        return sensor_input_parameters()
    else:
        return user_input_parameters()


# main function
if __name__ == '__main__':
    current_moisture, current_temperature, current_pressure = update_parameters()

    while check_moisture_casting() or check_temperature_casting() or check_pressure_casting():
        print("Parameters at casting are not as expected\nMoisture: {}\nTemperature: {}\nPressure: {}\n".format(
            current_moisture, current_temperature, current_pressure))
        # TODO comunicazione
        # invia dati a operatore -> ferma il getto
        # invia dati a DL
        # invia dati a centrale di betonaggio

        # aggiornamento parametri dai sensori
        current_moisture, current_temperature, current_pressure = update_parameters()

        # aggiorno il log
        log.append({'phase': 'casting', 'timestamp': datetime.datetime.now(), 'moisture': current_moisture,
                    'temperature': current_temperature, 'pressure': current_pressure})

        # delay lettura casting
        time.sleep(casting_read_delay)

    print("Parameters at casting are as expected. Moving to concrete maturation phase.")
    current_moisture, current_temperature, current_pressure = update_parameters()

    # monitoraggio post getto
    while not check_moisture_maturation() or not check_temperature_maturation() or not check_pressure_maturation():
        print("Level of maturation required unsatisfied\nMoisture: {}\nTemperature: {}\nPressure: {}\n".format(
            current_moisture, current_temperature, current_pressure))
        # TODO comunicazione
        # invia dati a operatore -> ferma il getto
        # invia dati a DL
        # invia dati a centrale di betonaggio

        # aggiornamento parametri dai sensori
        current_moisture, current_temperature, current_pressure = update_parameters()

        # aggiorno il log
        log.append({'phase': 'maturation', 'timestamp': datetime.datetime.now(), 'moisture': current_moisture,
                    'temperature': current_temperature, 'pressure': current_pressure})

        # delay lettura casting
        time.sleep(maturation_read_delay)

    # livello di maturazione raggiunto
    print("Level of maturation required is satisfied. You can now remove the formwork.")

    # rimozione casseri

    # salvataggio su file, se impostato
    if log_data:
        data['log'] = log

        with open('data.json', 'w') as outfile:
            json.dump(log, outfile)
            print("Data saved succesfully!")
    else:
        print("Nothing saved!")
