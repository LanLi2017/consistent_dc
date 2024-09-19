# This python script is to evaluate whether overlaps/conflicts exist

def exe_changes(df, df_cur):
    '''
    This func is to cal changes executed by each operation;
    Return a list of position information: [(0,'city'), (1, 'city'), (5, 'city'), ...]'''
    differences = []
    # Ensure both DataFrames have the same structure
    for col in df.columns:
        if col in df_cur.columns:
            for i in df.index:
                if df.at[i, col] != df_cur.at[i, col]:
                    differences.append((i, col))
    return differences


def check_overlaps(c1, c2):
    '''
    #@params c1: changes by Process I.op{x}
    #@params c2: changes by Process II.op{y}
    '''
    # Find overlap where both row id and column name are the same
    overlap = set(c1).intersection(set(c2))

    # Convert the result back to a list
    overlap_list = list(overlap)
    return overlap_list