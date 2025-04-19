from resolve import resolve_conflict


def mapping(tb1, tb2):
    pass


def orma():
    pass


def get_operations():
    pass


def conflict_aware_merge(tb1, tb2, p1, p2):
    """
    Merge two cleaning processes with conflict resolution.
    
    Args:
        tb1, tb2: Input prepared tables.
        p1, p2: Lists of cleaning operations (each op has read_scope, write_scope).
    
    Returns:
        L: Final merged process (list of operations).
    """
    col_map = mapping(tb1, tb2)           # Step 1: Map columns between tables
    annotated_p1 = orma(p1)               # Step 2: Annotate operations with read/write/full scopes
    annotated_p2 = orma(p2)

    L = []  # Final merged process

    for op1 in annotated_p1:
        full_scope_op1 = op1.read_scope | op1.write_scope

        # Step 3: Find potentially conflicting operations from p2
        potential_conflict_p2 = get_operations(col_map, full_scope_op1)

        if not potential_conflict_p2:
            # Conflict Type I: Modification vs. No-change
            comb_op = resolve_conflict(op1, None, type=1)
            L.append(comb_op)
            continue

        while potential_conflict_p2:
            op2 = potential_conflict_p2.pop()
            
            if 'Null' in op1.write_scope or 'Null' in op2.write_scope:
                # Conflict Type II: Modification vs. Removal
                comb_op = resolve_conflict(op1, op2, type=2)
            elif full_scope_op1 & op2.write_scope:
                # Conflict Type III: Modification vs. Modification
                comb_op = resolve_conflict(op1, op2, type=3)
            else:
                # No conflict — skip
                continue

            L.append(comb_op)

    return L
