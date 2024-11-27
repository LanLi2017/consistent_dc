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

def m1_process(p1, p2):
    print(p1)
    print(p2)
    conflicts = []
    for i,op_list in enumerate(p1):
        op = op_list[0]
        changes_ = op_list[1]
        for j, op_list1 in enumerate(p2):
            op1 = op_list1[0]
            changes1_ = op_list1[1]
            print(f'compare p1.op: {op} <> p2.op: {op1}')
            print(f'changes by p1: {changes_} with changes by p2: {changes1_}')
            res = check_overlaps(changes_, changes1_)
            print(res)
            conflicts.append(res)
    return conflicts