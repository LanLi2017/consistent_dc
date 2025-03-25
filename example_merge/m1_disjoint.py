from pprint import pprint
import pandas as pd

from ev import *
from example.ev import m1_process
from example.ops import rm_char, value_repl
from ops import *


# Merge Disjoint mode:
# Changes(row, column) by operations are disjoint, so that copy-paste the changes from each side.
def exe_process(process,df):
    log_changes = []
    for f in process:
        df_cur = df.copy()
        log_change = []
        func = f['func']  # Get the function
        log_change.append(func.__name__)
        params = f['params']  # Get the parameters
        df = func(df, **params)  # Call the function with the DataFrame and parameters
        diff = exe_changes(df_cur, df)
        log_change.append(diff)
        log_changes.append(log_change)
    return log_changes


if __name__ == '__main__':
    data_in = {
        "event": ["BREAKFAST", "LUNCHEON", "DINNER(?)", "dinner", "lunch", "Breakfast"],
        "venue": ["COMMERCIAL", "SOC;", "COMM.", "[SOC?];", "COM", "COMMERCIAL"],
        "place": ["RMS CAMPANIA", "BOULEVARD, 66TH AND 67TH STREETS", "(60 PINE ST., NEW YORK, NY)", "NEW YORK", "PHILADELPHIA, PA.", "TAMPA, FL"],
        "currency": ["Shilings", "Dollars", "Dollars", "Canadian Dollars", "Deutsche Marks", "Dollas"],
        "currency_symbol": ["s", "$", "", "", "$", "$"]
    }
    df = pd.DataFrame(data_in)
    print(f"The original data input:")
    print(df)
    df.to_csv("m1_origin.csv")
    chars_to_remove = r"[()?:;,.]"

    df1 = df.copy()
    # List of functions with their respective parameters, including the DataFrame
    print(">>>>>>>Start Process P1>>>>>>>")
    
    process1 = [
        {'func': upper_op, 'params': {'col': 'event'}},
        {'func': rm_char, 'params': {'col': 'event', 'chars_to_remove': r"[()?:;,.]"}}
    ]
    print(f"{process1}")
    # Loop through the functions and pass the DataFrame through each function
    log_changes_p1 = exe_process(process1, df1)
    print("The executed changes by process P1")
    pprint(log_changes_p1)
    print(">>>>>END P1>>>>>")
    
    print(">>>>>>>>Start Process P2>>>>>>>>")
    df2 = df.copy()
    process2 = [
        {'func': rm_char, 'params': {'col': 'venue', 'chars_to_remove': r"[()?:;,.]"}},
        {'func': value_repl, 'params': {'col': 'venue', 'dicts': {
                                                                'COMM': 'COMMERCIAL',
                                                                'COM': 'COMMERCIAL'
                                                                }}}
    ]
    print(f"{process1}")
    log_changes_p2 = exe_process(process2, df2)
    print("The executed changes by process P2")
    pprint(log_changes_p2)
    print(">>>>>END P2>>>>>") 
    
    print("Merging Process:")
    m1_process(log_changes_p1, log_changes_p2)
    
