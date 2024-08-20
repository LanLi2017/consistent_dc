## Data cleaning conflicts – Model TBL-1

### Data cleaning history and components: retrospective, happend one time
1. A **data cleaning history** is a sequence of **data cleaning steps** carried out on a particular data set.
2. A **data cleaning step** is an invocation of a particular data cleaning **operation** on a specific subset of cells in a data set.
3. **Operations** can differ from each other in terms of (a). what they do and (b). the subset (e.g., a single cell, a set of cells, a row, a column, and etc) of a total dataset that they are applied.


### A conceptual model for operation description: prospective 
There are three different levels of description for an operation:
- The **operation definition** that is independent of the schema of the data set.
- The binding of the definition (the **operation binding**) to the schema of a particular data set. 
- The application of the bound operation (**operation application**) is when the operation is used on a particular pair of cells. 

*!Question: while we talk about read-scope and write-scope, which level of operation level it is?*
**/*operation application*/**

4. The **write-scope** of a data cleaning operation is the set of cells whose values can be updated as a results of the **operation application**.
5. The **read-scope** of a data cleaning operation is the set of cells that can affect the outcome of the **operation application**.
6. The **full-scope** (or just **scope**) of a data cleaning operation is the union of **write-scope** and **read-scope** of the **operation application**.

*!Question: what's the relationship between read-scope and write-scope?*
**/*read-scope contains write-scope: (a).read-scope.equals(write-scope); (b).read-scope>write-scope*/**


7. If cells within the **write-scope** of one **operation application** is within the **read-scope** of a second operation, we say that the second **operation application** depends on the first. 

*(Do we want a more specific term than “depends” or “dependency”, like “functionally depends” (but not this).*
Dependency types:
(a). Functionally depends
(b). Value-passed depends 

### Different levels of strictness for compatibility/concurrency

8. The most strict level of compatibility means when the **full-scopes** of two processes are disjoint.

9. There is a second, less strict level where **read-scopes** can overlap safely, but **write-scopes** within the read scopes of another process still conflict.
e.g.,
[city, zipcode] &rarr; [city] ("lookup zipcode to repair city")
[state, zipcode] &rarr; [state] ("lookup zipcode to repair state")


10. The third strict level where, given knowledge about the operations involved (e.g. that the operations are commutative) the **write scopes** and **read scopes** of two processes may overlap and still be compatible. 
e.g.,
op1: [place] &rarr; [state,city,street] ("extract city information by splitting cell values in place")
op2: [place] &rarr; [place] ("normalize the separators in place by value replacement")

### Resolving Methods
11. Choose one of conflict

12. The other difference here is that “resolved/combined” data set has in some cells values that were assigned by neither data cleaner–”merging” the datasets here means more than picking values of cells in one modified data or another, because we have to rerun the two operations on the original value in the cell.




### Data cleaning workflow
A well-formed **data cleaning workflow** is depicted to represent **data cleaning workflow**. It comprises a sequence of data cleaning operations with **no violations**.

<!-- TODO: what is compatible -->
<!-- 3. **Order** is determined in the finalized **Linear Processing**. **Order** is agnostic across **Parallel Processing**. -->