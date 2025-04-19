def upper_op(df, col):
    """uppercase cell values to format data"""
    df[col]= df[col].str.upper()
    return df 


def rm_char(df, col, chars_to_remove):
    """remove unwanted/invalid characters from cell values"""
    df[col] = df[col].str.replace(chars_to_remove, '', regex=True).str.strip()
    return df


def value_repl(df, col, dicts):
    """replace cell values with standardized dictionary"""
    df[col] = df[col].replace(dicts)
    return df 