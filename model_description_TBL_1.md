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
**[*read-scope contains write-scope*]**: 
(a) read-scope $=$ write-scope; 
(b) read-scope $\gt$ write-scope
If so, there is no need to define **full-scope**?! Because $write{-}scope \bigcup read{-}scope$ &rarr; $read{-}scope$

*Rationale*: It is *impossible* to have a *disjoint* read-scope and write-scope. Or in other words, will it be possible to write the target cell values without reading them?


7. If cells within the **write-scope** of one **operation application** is within the **read-scope** of a second operation, we say that the second **operation application** depends on the first. 

*Do we want a more specific term than “depends” or “dependency”, like “functionally depends” (but not this).*
Dependency types:
(a). Functionally depends
same operation, different parameters 

(b). Value-passed depends 
different operations, different parameters 


### Different levels of strictness for compatibility/concurrency

8a. The most strict level of compatibility means when the **full-scopes** of two processes are disjoint.
*Or... read-scope*

8b. There is a second, less strict level where **read-scopes** can overlap safely, but **write-scopes** within the read scopes of another process still conflict.

*There is a second, less strict level of compatibility when **write-scopes** are disjoint, but **read-scopes** can overlap safetly.*
e.g.,
[city, zipcode] &rarr; [city] ("lookup zipcode to repair city")
[state, zipcode] &rarr; [state] ("lookup zipcode to repair state")


8c. The third strict level where, given knowledge about the operations involved (e.g. that the operations are commutative) the **write scopes** and **read scopes** of two processes may overlap and still be compatible. 

e.g., functionally dependent
[city] &rarr; [city] ("uppercase on city")
[city] &rarr; [city] ("trim whitespaces on city")

### Resolving Methods
9a. Choose one of conflict

9b. The other difference here is that “resolved/combined” data set has in some cells values that were assigned by neither data cleaner–”merging” the datasets here means more than picking values of cells in one modified data or another, because we have to rerun the two operations on the original value in the cell.


*Tim asks: Is it possible that the word we need for “no conflict”, “concurrent”, is actually “commutative”?  Or is Commutativity a special case of something, or vice versa?*

Hypotheses 8a and 8b are also about commutativity, so fundamentally not that different from 8c. Or is there something even more general than commutativity, that covers all data cleaning merging issues.

Next action:

1 + 2 + 3 + 4 = (1 + 2) + (3 + 4) = (3 + 4) + (1 + 2), etc
This means that commutativity of individual operations may lead to sequences of operations that are also commutative; this looks like “data cleaning processes” are analogous to “operation applications” in terms of commutativity. 


1,2,3,4.. Stands for different operations, in a data cleaning process followed by some order. 
Questions:
How fine grained should it be when we talk about “commutative”?
Within the operation level: op0, op1,op2,...
op0 and op1
op2 and op3
op4 and op5
Group of operations (two or more operations): g0, g1,g2,...
g0 = op0 o op2 o op4 …
g1 = op1 o op3 o op5…
g0 and g1 are commutative 
Complicated case: op0 not commutative with op1, but op0 and op2 binding together will be commutative with op1. 


### Data cleaning workflow
A well-formed **data cleaning workflow** is depicted to represent **data cleaning workflow**. It comprises a sequence of data cleaning operations with **no violations**.

<!-- TODO: what is compatible -->
<!-- 3. **Order** is determined in the finalized **Linear Processing**. **Order** is agnostic across **Parallel Processing**. -->