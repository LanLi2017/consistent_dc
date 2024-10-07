Data cleaning is a critical aspect of data science and data curation, yet it is often error-prone and demands significant time and effort when conducted by an individual. We recommend collaborative data cleaning as a strategy to enhance the efficiency and quality of the process by incorporating the expertise of multiple data curators. This approach is particularly beneficial for addressing data cleaning tasks that are shared and completed by different individuals with a shared objective. However, it also introduces challenges, such as conflicting data operations, which can lead to disagreements over the resulting data changes.

**Compatible Merging**
What is required for enabling data cleaning is a well-understood method for merging the changes made by the two different data cleaners when it is possible, and that identifies when it is not possible to losslessly merge the various changes.

**Pipeline**
We propose and demonstrate an approach to merging the progress made during independent cleaning sessions that does not entail viewing those sessions as “recipes” and does not require static analysis of the data cleaning ‘workflows’ that were performed during those sessions. 
*Distinguish history and recipe*

We do this by classifying the changes actually made in two the different sessions into 
(1) those changes that can trivially  merged by copying the final values in cells modified in one or the other of the data sets; 
(2) overlapping changes that are commutative and can be merged by performing the two sets of respective operations on the original data set in an arbitrary order with respect to each other; 
and (3) changes that overlap, are not commutative, but are the results of changes that have a known priority such that both sets of changes can be preserved by performing the two sets of operations in an appropriate order.  

Changes that do not fall into these three categories are considered to be conflict and require human decision to resolve.  We demonstrate a tool that merges two independent OpenRefine session via this approach and reports the subset of changes that could not be merged automatically (analogous to Git merges and conflicts). The problem merging the changes of class (3) can be viewed as a *constraint satisfaction problem* that we address using answer set programming.
