## Data cleaning conflicts – Model LL-1

### Data cleaning process and components
1. A **data cleaning process** is a sequence of **data cleaning steps** carried out on a particular data set.
2. A **data cleaning step** is an invocation of a particular data cleaning **operation** on a specific subset of cells in a data set.
3. A data cleaning **operation** is applied to dataset in different dimensions, including row level, column level, and cell level. 

### Data cleaning operations and features
1. The **write-scope** of a data cleaning operation is the set of cells whose values can be updated as a results of the operation.
2. The **read-scope** of a data cleaning operation is the set of cells that can affect the outcome of the operation.
3. If cells within the **write-scope** of the first operation are **read-by** the second operation, we call **dependency** exists between these two operations. Otherwise, we call these two operations are **concurrent**.
4. **Linear Processing** occurs if changing **read-scope** of one operation may alter the usability of all the downstream **dependent** operations. Otherwise, it is **Parallel Processing**.


**Compatible**: The updates applied during a data cleaning process are compatible with the updates applied by a second data cleaning process if no cells within the *read-scope* of any of the data cleaning operations comprising the first process were updated by the operations comprising the second.
7. Two data cleaning processes are mutually compatible if each is compatible with the other; otherwise, the processes are in conflict.
8.The updates made by two mutually compatible data cleaning processes can be merged simply by applying to the original dataset the updates made by either one of the processes followed by the updates made by the other.
9. Order-agnostic and Order-determined
10. Commutative and Compatibility 