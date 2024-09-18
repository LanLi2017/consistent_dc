import pandas as pd 
# This python script is to deal with first category of merging process
# Changes(row, column) by operations are disjoint, so that copy-paste the changes from each side.
def exe_changes():
    '''
    This func is to cal changes executed by each operation;
    Return a list of position information: [(0,'city'), (1, 'city'), (5, 'city'), ...]'''
    
    pass


def check_overlaps():
    '''This func is to check if overlaps exist between the changes'''
    pass


def process1():
    pass


def process2():
    pass


if __name__ == '__main__':
    data_in = {
        "event": ["BREAKFAST", "LUNCHEON", "DINNER(?)", "dinner", "lunch", "Breakfast"],
        "venue": ["COMMERCIAL", "SOC;", "COMM.", "[SOC?];", "COM", "COMMERCIAL"],
        "place": ["RMS CAMPANIA", "BOULEVARD, 66TH AND 67TH STREETS", "(60 PINE ST., NEW YORK, NY)", "NEW YORK", "PHILADELPHIA, PA.", "TAMPA, FL"],
        "currency": ["Shilings", "Dollars", "Dollars", "Canadian Dollars", "Deutsche Marks", "Dollas"],
        "currency_symbol": ["s", "$", "", "", "$", "$"]
    }
    df1 = pd.DataFrame(data_in)
    print(f'the first dataframe is : {df1}')
    df2 = pd.DataFrame(data_in)
    print(f'the second dataframe is {df2}')
    
