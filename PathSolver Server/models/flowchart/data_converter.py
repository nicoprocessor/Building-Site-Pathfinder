import datetime
import numpy as np
import pandas as pd
import pathlib
import os
from pprint import pprint
from collections import OrderedDict
from typing import Dict, Any, List, NewType

# typing aliases
# Timestamp = NewType('Timestamp', datetime.datetime)
# Report_full_schema = Dict[str, str, float, float, float, str, Timestamp]
# Report_short_schema = Dict[str, float, float, float, Timestamp]

# Utility constants
file_suffix = ['short', 'full', 'test']
float_precision = 3

# dictionaries to convert dict names to xl naming conventions
schemas = [
    {  # short
        'BIM_id': 'B3F ID',
        'temperature': 'Temperatura getto',
        'moisture': 'Umidità getto',
        'pressure': 'Pressione getto',
        'timestamp': 'Timestamp'
    }, {  # full
        'BIM_id': 'BIM Object ID',
        'temperature': 'Temperatura getto',
        'moisture': 'Umidità getto',
        'pressure': 'Pressione getto',
        'phase': 'Fase',
        'status': 'Stato',
        'begin_timestamp': 'Begin_TS',
        'end_timestamp': 'End_TS'
    }, {  # test
        'BIM_id': 'BIM Object ID',
        'temperature': 'Temperatura getto',
        'moisture': 'Umidità getto',
        'pressure': 'Pressione getto',
        'timestamp': 'Timestamp'
    }]


def extract_data(log, file_detail):
    """Extracts summarized info from a batch of data"""
    summarized_log = OrderedDict()

    BIM_id = log[-1]['BIM_id']

    avg_temperature = np.average([l['temperature'] for l in log])
    avg_moisture = np.average([l['moisture'] for l in log])
    avg_pressure = np.average([l['pressure'] for l in log])

    summarized_log['BIM_id'] = BIM_id
    summarized_log['temperature'] = round(avg_temperature, float_precision)
    summarized_log['moisture'] = round(avg_moisture, float_precision)
    summarized_log['pressure'] = round(avg_pressure, float_precision)

    if file_detail == file_suffix[0]:  # short
        status = log[-1]['status']
        phase = log[-1]['phase']
        timestamp = log[-1]['timestamp']

        summarized_log['status'] = status
        summarized_log['phase'] = phase
        summarized_log['timestamp'] = timestamp
    elif file_detail == file_suffix[1]:  # full
        begin_ts = log[-1]['begin_timestamp']
        end_ts = log[-1]['end_timestamp']

        summarized_log['begin_timestamp'] = begin_ts
        summarized_log['end_timestamp'] = end_ts
    return dict(summarized_log)


def convert_dict_keys(old_dict, conversion_table):
    """Converts a dictionary to an equal dictionary,
    changing the keys according to the given conversion table"""
    converted_dict = OrderedDict()

    for key, value in old_dict.items():
        try:
            converted_key = conversion_table[key]
            converted_dict[converted_key] = value
        except KeyError:
            # if the key is not contained in the conversion table, drop that element
            continue
    return dict(converted_dict)


def append_summary(log, file_detail: str):
    """Generates and writes the summarized line on the full log file"""
    # Setting the right path to the spreadsheet
    sheet_path = pathlib.Path.cwd().parent.parent.joinpath('res', 'report-' + file_detail + '.xlsx')
    print("Updating file at: " + os.fspath(sheet_path))

    # Loading previous Excel data into dataframe
    xl_df = pd.read_excel(open(os.fspath(sheet_path), 'rb'), sheet_name='Sheet1')

    # data pre processing, summarize the list of dicts in a single dict
    summarized_log = extract_data(log, file_detail)
    log_list = []

    # Key conversion of the dictionary in order to match with the schema on the destination file
    schema_index = file_suffix.index(file_detail)
    converted_log = convert_dict_keys(summarized_log, conversion_table=schemas[schema_index])
    log_list.append(converted_log)

    # Update previous dataframe with the new row
    new_row = pd.DataFrame.from_dict(log_list)
    xl_df = pd.concat([xl_df, new_row])
    pprint(xl_df)

    # Write update dataframe to Excel spreadsheet
    writer = pd.ExcelWriter(os.fspath(sheet_path))
    xl_df.to_excel(writer, 'Sheet1', index=False)
    writer.save()

    # # leave for debug purpose
    df_check = pd.read_excel(open(os.fspath(sheet_path), 'rb'), sheet_name='Sheet1')
    pprint(df_check)


# main
if __name__ == '__main__':
    time_series = np.sort(list(map(lambda x:round(x,3), np.random.random(18))))

    d1 = [{'BIM_id': 'A', 'temperature': 10, 'moisture': 20, 'pressure': 10, 'begin_timestamp': 0, 'end_timestamp': 0},
          {'BIM_id': 'A', 'temperature': 12, 'moisture': 22, 'pressure': 20, 'begin_timestamp': 0, 'end_timestamp': 0},
          {'BIM_id': 'A', 'temperature': 12, 'moisture': 22, 'pressure': 20, 'begin_timestamp': 0, 'end_timestamp': 0}]
    d2 = [{'BIM_id': 'A', 'temperature': 20, 'moisture': 50, 'pressure': 20, 'begin_timestamp': 0, 'end_timestamp': 0},
          {'BIM_id': 'A', 'temperature': 22, 'moisture': 52, 'pressure': 20, 'begin_timestamp': 0, 'end_timestamp': 0},
          {'BIM_id': 'A', 'temperature': 22, 'moisture': 54, 'pressure': 20, 'begin_timestamp': 0, 'end_timestamp': 0}]
    d3 = [{'BIM_id': 'A', 'temperature': 20, 'moisture': 60, 'pressure': 20, 'begin_timestamp': 0, 'end_timestamp': 0},
          {'BIM_id': 'A', 'temperature': 22, 'moisture': 67, 'pressure': 22, 'begin_timestamp': 0, 'end_timestamp': 0},
          {'BIM_id': 'A', 'temperature': 22, 'moisture': 68, 'pressure': 24, 'begin_timestamp': 0, 'end_timestamp': 0}]

    data = [d1, d2, d3]
    counter = 0

    for i in range(len(data)):
        l = data[i]
        for d_index in range(len(l)):
            l[d_index]['begin_timestamp'] = time_series[counter]
            counter += 1
            l[d_index]['end_timestamp'] = time_series[counter]
            counter += 1

    append_summary(d1, file_detail='full')
    append_summary(d2, file_detail='full')
    append_summary(d3, file_detail='full')
