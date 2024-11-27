We have possibly three levels of the notion of **compatible**: compatible-8a (very strict), compatible-8b (middle), ...compatible-8c (less strict).
- 8a. The most strict level of compatibility means when the full-scopes of two processes are disjoint.
- 8b. There is second, less strict level of compatibility when write-scopes are disjoint, but read-scopes can overlap safely. 
- 8c. The third strict level where, given knowledge about the operations involved (e.g., that the operations are commutative) the write scopes and read scopes of two processes may overlap and still be compatible. 

### Task: Creating a set of examples as follows: 
**Ex1-pos:** P1 and P2 **are** compatible-8a &rarr; it makes sense (positive example)

**Ex1-neg:** P1 and P2 are **not** compatible-8a &rarr; it makes sense (negative example)

**Ex2:** P1 and P2 are not compatible-8a &rarr; too strict... &rarr;but compatible-8b &rarr; good!

**Ex2-neg:** P1 and P2 are not compatible-8b &rarr; it makes sense (negative example)!

**Ex3**: P1 and P3 are not compatible-8b &rarr; too strict... &rarr; but compatible-8c &rarr; good!

#### Strict I: Full scope (Read U Write) NO overlap
**Ex1-pos**: P1 and P2 are compatible-8a → it makes sense (positive example) 

P1: [opx, opx+1, opx+2]

P2: [opy, opy+1]

P1: opx, opx+1,...are operations working on the single column “city”. For instance, we first format “city” into TitleCase(opx), and remove consecutive spaces on “city” (opx+1),  then use regular expressions (opx+2) to strip extra weird characters from the “city”. 
The Full scope of P1 is [city].

P2: opy, opy+1, opy+2,... are operations working on the single column “state”, For instance, we first trim leading and trailing spaces from column “state” (opy), and acronymize the spellings (opy+1).
The Full scope of P2 is [state].

**P1 and P2 are compatible because: for any operation in P1 and P2, there is NO overlap between their Full scope.** 

**Ex1-neg**: P1 and P2 are not compatible-8a → it makes sense (negative example)

P1: [opx, opx+1, opx+2]

P2: [opy, opy+1]

P1: 
opx repairs city by checking auxiliary column zipcode: [city, zipcode] → [city];
opx+1 format city into TitleCase: [city] → [city]
opx+2 strip weird characters in city: [city] → [city]

P2:
opy revise zipcode according to city and area code: [zipcode, city, area code] → [zipcode]
opy+1 format zipcode into numerical type: [zipcode] → [zipcode]
P1 and P2 are not compatible because there exist opx and opy whose Full Scope overlaps with each other.

#### Strict II: Read-Only Scope Overlap 

**Ex2-pos**: P1 and P2 are not compatible-8a  → uh.. too strict → but compatible-8b →  good!

P1: [opx, opx+1, opx+2]
P2: [opy, opy+1]

P1:
opx repairs city names by checking zipcode: [city, zipcode] → [city]
opx+1 format city into TitleCase: [city] → [city]
opx+2 strip weird characters in city: [city] → [city]

P2:
opy repairs state names by checking zipcode: [state, zipcode] → [state]
opy+1 acronymize state name: [state] → [state]

**According to compatible-8a, there exists opx and opy whose full scope overlap, therefore P1 and P2 are not compatible. However, opx  and opy are read-only overlap (compatible-8b), therefore, they are supposed to be Compatible.**

**Ex2-neg**: P1 and P2 are not compatible-8b  → it makes sense (negative example)

P1: [opx, opx+1, opx+2]
P2: [opy, opy+1]

P1:
opx format city into TitleCase: [city] → [city]
opx+1 acronymize state: [state] → [state]
opx+2  create a new column place by concatenating city name and state name by **comma**: [city, state] → [place]

P2:
opy create a new column place by concatenating city name and state name by **semicolon**: [city, state] → [place]
opy+1 strip weird characters from place: [place] → [place]

**According to compatible-8b, there exists opx+2 and opy whose read scope overlaps, but their write scopes also overlap. Therefore P1 and P2 are not compatible.** 


#### Strict III: Read AND Write Overlap
**Ex3**:  P1 and P2 are not compatible-8b → uh.. too strict → but compatible-8c → good!

P1: [opx, opx+1, opx+2]
P2: [opy, opy+1]

P1:
opx trims leading and trailing whitespaces for column city: [city] → [city]
opx+1 strip weird characters (,/;/’/”/./s+) from column city: [city] → [city]
opx+2 repairs city by checking zipcode: [city, zipcode] → [city]


P2:
opy format city into TitleCase: [city] → [city]
opy+1 remove consecutive whitespaces from city: [city] → [city]

**According to compatible-8b, all operations in P1 share the same read and write scope of operations in P2. P1 and P2 are not compatible. But as we know that the functions are commutative, therefore, P1 and P2 are compatible instead.**

