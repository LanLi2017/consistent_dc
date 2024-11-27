| Working Space | Difference Expression |Description|Branch Name|Merging Methods|
| ----------- | ----------- | ----------- | ----------- | ----------- |
| Cell | f1(row1, col1) != f2(row1, col1)|Apply functions f1, f2 result in different cell values | c1 | require manual merge|
| |f1(row1, col1) != f2(row1, col1) f1(row1, col1) != (row1, col1) |Cell value at row1, col1 get changed in D1, no changes in D2 | c2| require manual merge|
| Row| D1.row1 != remove(D2.row1)|No changing in D1,Removing row1 in D2|r1|require manual merge |
||remove(D1.row1)!=D2.row1| Removing row1 in D1,No changing in D2|r3|require manual merge|
||add_row(D1)!=D2.row |Add row in D1,No changing in D2|r2|**Auto-Merging**|
||D1.row!=add_row(D2)|No changing in D1, Add row in D2|r4|require manual merge|
|Column|D1.cs1!=D2.cs2|Column Schema(CS) in D1 and D2 are not the same|c1|require manual merge|


