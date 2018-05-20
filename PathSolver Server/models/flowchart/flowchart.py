import time
import json
import datetime
import data_converter
from typing import Tuple

# variabile che permette all'utente di decidere se salvare i dati registrati
# in un file esterno fruibile successivamente
log_data = True
file_suffix = ['short', 'full', 'test']
BIM_id = 'A'

# in ogni caso in inizializzo una lista per loggare i dati
log_full = []  # report completo, ad alta frequenza di campionamento
log_short = []  # report sintetico

# tolleranza
moisture_range = 2
temperature_range = 2
pressure_range = 2

# durata delay tra letture successive (in secondi)
casting_read_delay = 3
maturation_read_delay = 3

# delay tra due salvataggi successivi (in secondi)
full_report_delay = 60
short_report_delay = 300

# valori attesi durante il getto
expected_moisture_casting = 50
expected_temperature_casting = 28
expected_pressure_casting = 10

# valori attesi a maturazione
expected_moisture_maturation = 50
expected_temperature_maturation = 30
expected_pressure_maturation = 10

# valori rilevati
current_moisture = 0.0
current_temperature = 0.0
current_pressure = 0.0


# controllo parametri durante la gettata
def check_moisture_casting() -> bool:
    return float(current_moisture) < abs(expected_moisture_casting - moisture_range)


def check_temperature_casting() -> bool:
    return float(current_temperature) < abs(expected_temperature_casting - temperature_range)


def check_pressure_casting() -> bool:
    return float(current_pressure) < abs(expected_pressure_casting - pressure_range)


# controllo parametri a gettata terminata
def check_moisture_maturation() -> bool:
    return float(current_moisture) < abs(expected_moisture_maturation - moisture_range)


def check_temperature_maturation() -> bool:
    return float(current_temperature) < abs(expected_temperature_maturation - temperature_range)


def check_pressure_maturation() -> bool:
    return float(current_pressure) < abs(expected_pressure_maturation - pressure_range)


# interroga i sensori del RaspberryPi per aggiornare i valori dei parametri da monitorare
def sensor_input_parameters() -> Tuple[float, float, float]:
    # TODO trovare soluzione per sensore di pressione
    detected_moisture = rpi.read_humidity[1]
    detected_temperature = rpi.read_temperature[1]
    detected_pressure = rpi.read_humidity[1]
    return detected_moisture, detected_temperature, detected_pressure


# chiede di inserire manualmente i parametri da monitorare
def user_input_parameters() -> Tuple[float, float, float]:
    input_moisture = float(input("Enter current moisture: "))
    input_temperature = float(input("Enter current temperature: "))
    input_pressure = float(input("Enter current pressure: "))
    return input_moisture, input_temperature, input_pressure


# aggiorna i parametri da monitorare secondo il canale prestabilito (manuale da utente o automatico da sensori)
def update_parameters(use_sensors=True) -> Tuple[float, float, float]:
    if use_sensors:
        return sensor_input_parameters()
    else:
        return user_input_parameters()


# main function
def monitoring_session(use_sensors: bool = True, log_data: bool = True, BIM_id: str = 'test'):
    if use_sensors:
        from rpi_sensors import RPiConfigs
        rpi = RPiConfigs()

    # full_report_delay = 60
    # short_report_delay = 300

    print(
        "Phase: casting\n"
        "Expected moisture casting: {}\n"
        "Expected temperature casting: {}\n"
        "Expected pressure casting: {}\n".format(
            expected_moisture_casting, expected_temperature_casting, expected_pressure_casting))
    current_moisture, current_temperature, current_pressure = update_parameters(use_sensors)

    start_time = time.time()

    while check_moisture_casting() or check_temperature_casting() or check_pressure_casting():
        print("Parameters at casting are not as expected\n"
              "Moisture: {}\n"
              "Temperature: {}\n"
              "Pressure: {}\n".format(
            current_moisture, current_temperature, current_pressure))

        # TODO comunicazione
        # invia dati a operatore -> ferma il getto
        # invia dati a DL
        # invia dati a centrale di betonaggio

        # aggiornamento parametri dai sensori
        current_moisture, current_temperature, current_pressure = update_parameters(use_sensors)

        # update log-full
        log_full.append({'BIM_id': BIM_id,
                         'phase': 'casting',
                         'status': 'Bad',
                         'begin_timestamp': start_time,
                         'end_timestamp': datetime.datetime.now(),
                         'moisture': current_moisture,
                         'temperature': current_temperature,
                         'pressure': current_pressure})

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Salvataggio Excel
        if elapsed_time > full_report_delay:
            # Salvataggio su file Excel completo (full)
            data_converter.append_summary(log_full, file_detail=file_suffix[1])
            log_full = []

        if elapsed_time > short_report_delay:
            # salvataggio su file Excel riassuntivo (short)
            log_short.append({'BIM_id': BIM_id,
                              'phase': 'casting',
                              'status': 'Bad',
                              'timestamp': end_time,
                              'moisture': current_moisture,
                              'temperature': current_temperature,
                              'pressure': current_pressure})
            data_converter.append_summary(log_short, file_detail=file_suffix[0])
            log_short = []

        # delay lettura casting
        time.sleep(casting_read_delay)

    print("Parameters at casting are as expected. Moving to concrete maturation phase.")

    # update data with the change of status
    log_full.append({'BIM_id': BIM_id,
                     'phase': 'casting',
                     'status': 'OK',
                     'begin_timestamp': start_time,
                     'end_timestamp': datetime.datetime.now(),
                     'moisture': current_moisture,
                     'temperature': current_temperature,
                     'pressure': current_pressure})
    log_short.append({'BIM_id': BIM_id,
                      'phase': 'casting',
                      'status': 'OK',
                      'timestamp': end_time,
                      'moisture': current_moisture,
                      'temperature': current_temperature,
                      'pressure': current_pressure})

    data_converter.append_summary(log_short, file_detail=file_suffix[0])
    data_converter.append_summary(log_full, file_detail=file_suffix[1])
    log_short = []
    log_full = []

    print("Phase: maturation\n"
          "Expected moisture maturation: {}\n"
          "Expected temperature maturation: {}\n"
          "Expected pressure maturation: {}\n".format(
        expected_moisture_maturation, expected_temperature_maturation, expected_pressure_maturation))

    current_moisture, current_temperature, current_pressure = update_parameters(use_sensors)

    # monitoraggio post getto
    while check_moisture_maturation() or check_temperature_maturation() or check_pressure_maturation():
        print("Level of maturation required unsatisfied\n"
              "Moisture: {}\n"
              "Temperature: {}\n"
              "Pressure: {}\n".format(
            current_moisture, current_temperature, current_pressure))

        # TODO comunicazione
        # invia dati a operatore -> ferma il getto
        # invia dati a DL
        # invia dati a centrale di betonaggio

        # aggiornamento parametri dai sensori
        current_moisture, current_temperature, current_pressure = update_parameters(use_sensors)

        # update full-log
        log_full.append({'BIM_id': BIM_id,
                         'phase': 'maturation',
                         'status': 'Bad',
                         'begin_timestamp': start_time,
                         'end_timestamp': datetime.datetime.now(),
                         'moisture': current_moisture,
                         'temperature': current_temperature,
                         'pressure': current_pressure})

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Salvataggio Excel
        if elapsed_time > full_report_delay:
            # Salvataggio su file Excel completo (full)
            data_converter.append_summary(log_full, file_detail=file_suffix[1])
            log_full = []

        if elapsed_time > short_report_delay:
            # salvataggio su file Excel riassuntivo (short)
            log_short.append({'BIM_id': BIM_id,
                              'phase': 'maturation',
                              'status': 'Bad',
                              'timestamp': end_time,
                              'moisture': current_moisture,
                              'temperature': current_temperature,
                              'pressure': current_pressure})
            data_converter.append_summary(log_short, file_detail=file_suffix[0])
            log_short = []

        # read delay
        time.sleep(maturation_read_delay)

    # livello di maturazione raggiunto
    print("Level of maturation required is satisfied. You can now remove the formwork.")

    # update data with the change of status
    log_full.append({'BIM_id': BIM_id,
                     'phase': 'maturation',
                     'status': 'OK',
                     'begin_timestamp': start_time,
                     'end_timestamp': datetime.datetime.now(),
                     'moisture': current_moisture,
                     'temperature': current_temperature,
                     'pressure': current_pressure})
    log_short.append({'BIM_id': BIM_id,
                      'phase': 'maturation',
                      'status': 'OK',
                      'timestamp': end_time,
                      'moisture': current_moisture,
                      'temperature': current_temperature,
                      'pressure': current_pressure})

    data_converter.append_summary(log_short, file_detail=file_suffix[0])
    data_converter.append_summary(log_full, file_detail=file_suffix[1])
    log_short = []
    log_full = []


if __name__ == '__main__':
    monitoring_session()

