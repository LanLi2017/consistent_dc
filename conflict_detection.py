
def cal_op_similarity(op1, op2) -> bool:
    # Calculate the similarity between the operations enhanced with explanations
    # Return True if the similarity is less than a threshold, which means the operations are opposite
    # Otherwise, return False.
    pass


def rigor_conflict(op1, op2) -> bool:
    # If op1.read_scope, op1.write_scope overlaps with op2.write_scope
    # This means op2 is trying to write the same column as op1(full scope), so that they are conflicting 
    # Return True, otherwise return False
    if set(op2['write_scope']).intersection(op1['read_scope']) or set(op2['write_scope']).intersection(op1['write_scope']):
        return True
    else:
        return False

def refine_conflict(op1, op2) -> bool:
    # For True rigor conflict
    # Using the cal_op_similarity function to refine the conflict
    # Only if the operations are opposite, return True
    pass