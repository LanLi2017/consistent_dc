## Data cleaning conflicts – Model LL-1

### Data cleaning process and components
1. A **data cleaning process** is a sequence of **data cleaning steps** carried out on a particular data set.
2. A **data cleaning step** is an invocation of a particular data cleaning **operation** on a specific subset of cells in a data set.
3. A data cleaning **operation** is applied to dataset in different dimensions, including row level, column level, and cell level. 

### Operation characteristics and relationships 
1. The **write-scope** of a data cleaning operation is the set of cells whose values can be updated as a results of the operation.
2. The **read-scope** of a data cleaning operation is the set of cells that can affect the outcome of the operation.
3. The **full-scope** (or just **scope**) of a data cleaning operation is the union of write-scope and read-scope of the operation.
4. If cells within the **write-scope** of the first operation are **read-by** the second operation, we call **dependency** exists between these two operations.
5. The updates applied during a data cleaning process are **absolute concurrent** with the updates applied by a second data cleaning process if no cells within the **full-scope** of any of the data cleaning operations comprising the first process were updated by the operations comprising the second.

> I replace *compatible* with *absolute concurrent*
6. **Relative concurrent (RC)** operation is categorized into two types:
- **RC** originated from **read-scope**: cells within **read-scope** by two operations overlap.
e.g.,
[city, zipcode] &rarr; [city] ("lookup zipcode to repair city")
[state, zipcode] &rarr; [state] ("lookup zipcode to repair state")

- **RC** originated from **write-scope**: cells within **write-scope** by two operations overlap.
e.g.,
op1: [place] &rarr; [state,city,street] ("extract city information by splitting cell values in place")
op2: [place] &rarr; [place] ("normalize the separators in place by value replacement")


4. **Dependency violations**: 
- [Must]**RC** originated from **write-scope**
- [Might] **Dependent operation**



### Workfow types
1. **Linear Processing** occurs if changing **read-scope** of one operation may alter the usability of all the downstream **dependent** operations. Otherwise, it is **Parallel Processing**.
2. A well-formed workflow should be **no violations** between **Linear** or **Parallel** processings.

3. **Order** is determined in the finalized **Linear Processing**. **Order** is agnostic across **Parallel Processing**.


### Merging conflicts detection and definition 
1. **Compatible**: (1). Within the **Linear Processing**, the updates applied during a data cleaning process are compatible with the updates applied by a second data cleaning process if no cells within the **read-scope** of any of the data cleaning operations comprising the first process were **written** by the operations comprising the second.
2. Two data cleaning processes are mutually compatible if each is compatible with the other; otherwise, the processes are in conflict.
3.The updates made by two mutually compatible data cleaning processes can be merged simply by applying to the original dataset the updates made by either one of the processes followed by the updates made by the other.
4. Order-agnostic and Order-determined
5. Commutative and Compatibility 

### Merging conflicts resolving 