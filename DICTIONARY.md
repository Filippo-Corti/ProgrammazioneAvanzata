# Programmazione Avanzata

Dizionario dei termini fondamentali presentati durante il corso, con riferimento al contesto del linguaggio Python.

## [A]

### Activation Record

Un **record di attivazione**, chiamato anche *frame*, è una struttura creata ogni volta che viene fatta una chiamata di funzione. 
Conserva (freezandole) le informazioni necessarie alla esecuzione della chiamata stessa, come parametri, variabili locali e punto a cui tornare al termine della chiamata. 

I record di attivazione sono organizzati in uno stack e permettono, tra le altre cose, l'esecuzione di funzioni ricorsive.
Tra i diversi livelli dello stack vengono passati:
- Gli argomenti con cui è chiamata la funzione, dal livello inferiore a quello superiore.
- I valori di return della funzione, dal livello superiore a quello inferiore.

## [B]

## [C]

### Class-Based Programming

TODO (dispensa 7)

La **programmazione class-based** è una forma di programmazione a oggetti che implementa:
* Il concetto di oggetto, come TODO;
* Il concetto di classe, come template TODO.
Non supporta invece il terzo concetto che caratterizza la programmazione orientata agli oggetti, ovvero l'inheritance.

Python non supporta il concetto di classe in quanto template rigido che descrive una certa istanza. Per questo motivo, non è class-based.

### Closure

Una **closure** è una funzione che conserva il *binding* tra le variabili dell'ambiente in cui è definita ed i loro valori al tempo di definizione.
I valori sono preservati anche quando la funzione è eseguita in un contesto diverso. 

Ad esempio:
```python
def build_match_and_apply_functions(pattern, search, replace):
    matches_rule = lambda word: re.search(pattern, word)
    apply_rule = lambda word: re.sub(search, replace, word)
    return (matches_rule, apply_rule)

rules = [
    build_match_and_apply_functions(pattern, search, replace)
    for (pattern, search, replace) in PATTERNS
]
```
In questo contesto, le funzioni create `matches_rule` e `apply_rule` sono closures: conservano i valori di `pattern`, `search` e `replace` con cui sono state costruite.

### Compiled Programming Language

Un **linguaggio di programmazione compilato** viene tradotto da un compilatore, prima dell'esecuzione, in codice macchina o in un'altra rappresentazione eseguibile. 
In genere questo riduce il lavoro necessario durante l'esecuzione, ma richiede una fase di compilazione.

Il paradigma complementare è quello dei linguaggi di programmazione interpretati.
La distinzione non è sempre netta: Python, per esempio, è considerato generalmente un linguaggio interpretato.
Tuttavia, nella pratica, il codice sorgente Python viene prima compilato in *bytecode* e poi eseguito dalla macchina virtuale Python.

### Currying

Il **currying** (o applicazione parziale) consiste nell'operazione di trasformazione di una funzione con più argomenti in una sequenza di funzioni, ciascuna delle quali riceve un argomento e restituisce la funzione successiva. 
In questo modo è possibile fissare progressivamente alcuni argomenti e ottenere funzioni più specifiche. 

Ad esempio:
```python
def make_currying(f, a):
    '''Fixes the first parameter of f to a'''
    def fc(*args):
        return f(a, *args)
    return fc

f = lambda x, y: y/x # f(x, y) = y/x
g = make_currying(f, 2) # g(y) = y/2
h = make_currying(g, 3) # h() = 3/2
```
In Python un'operazione simile a quanto fa `make_currying` è fornita da `functools.partial`.

> **Nota**: Il currying è una tecnica basata sul principio delle closures.

## [D]

### Shallow e Deep Copying

La **copia shallow** di un elemento crea un nuovo oggetto esterno, ma non duplica gli oggetti contenuti al suo interno: ne copia soltanto i riferimenti. 
Originale e copia sono distinti, ma continuano a condividere gli eventuali oggetti annidati.

La **copia profonda** crea un nuovo oggetto e copia ricorsivamente anche gli oggetti contenuti al suo interno. 
L'originale e la copia non condividono quindi gli oggetti annidati copiati: modificare una struttura interna della copia non modifica quella dell'originale. 

```python
from copy import deepcopy

x = SomeClass(val=3)
y = x # This is a shallow copy
z = deepcopy(x) # This is a deep copy

z.val = 5
print(x.val) # This is still 3
y.val = 5
print(x.val) # This is now 5 
```

In Python, per sapere quante variabili hanno una stessa **object identity** (ovvero referenziano lo stesso indirizzo di memoria) è possibile usare `sys.getrefcount(obj)`.
Questo non funziona per numeri e stringhe, che vengono referenziati come singleton (dunque, tutte le variabili numeriche con valore `50` puntano in realtà alla stessa cella).

### Dynamic Typing

Il **dynamic typing** caratterizza i linguaggi di programmazione che non richiedono di specificare il tipo delle variabili a tempo di compilazione, ma che invece lo inferiscono a runtime.

In Python, questo sistema è permesso poiché il tipo non è associato in modo fisso al nome di una variabile, ma all'oggetto a cui essa fa riferimento. 
In Python la stessa variabile può quindi riferirsi, in momenti diversi, a oggetti di tipi diversi; la correttezza delle operazioni viene controllata durante l'esecuzione (non ho modo di validare un'espressione fino a che non la sto eseguendo).

```python
x = 5
x = "10-10-2026"
x.split("-") # If x were associated to 'int', this operation should fail a-priori
```

## [E]

## [F]

### Functional Programming

La **programmazione funzionale** è un paradigma di programmazione basato (in breve) su quattro concetti:
1) Le funzioni sono **first class objects**: tutto ciò che posso fare con dei "dati" lo posso fare anceh con le funzioni. Possono essere assegnate a variabili, passate come argomenti e restituite da altre funzioni.
2) La ricorsione è il meccanismo primario di strutturazione del codice. Ad esempio, per poter eseguire un insieme di step sequenzialmente occorrerebbe fare:
```python
do_it = lambda f: f()
map(do_it, [task1, task2, task3]) # each task is a function (there should be no state shared between them)
``` 
3) Il linguaggio si concentra sul fornire strumenti di **list processing**, come `map`, `filter`, `reduce`, etc.
4) Le funzioni evitano il più possibile **side-effects**. Ciò include operazioni che mantengono uno stato del programma (il termine funzione ha significato matematico, un mapping `input -> output`).

Queste caratteristiche consentono di scrivere codice meno soggetto ad errori e più facilmente verificabile da strumenti di verifica automatica.

Python supporta diversi elementi della programmazione funzionale, pur non essendo chiaramente un linguaggio funzionale puro.

## [G]

### Garbage Collection

La **garbage collection** è il meccanismo di recupero automatico della memoria occupata da oggetti che non sono più raggiungibili dal programma. 
Questo evita al programmatore lo sforzo di tenere traccia di quali elementi siano ancora referenziati e di quali invece si possa liberare.

CPython, l'implementazione più diffusa di Python, usa per la garbage collection il conteggio dei riferimenti, affiancato da un meccanismo capace di individuare anche gruppi di oggetti che si riferiscono ciclicamente tra loro.

### Generator

Un **generatore** è una funzione che produce un valore alla volta, invece di calcolare subito un'intera sequenza. 
Possiamo immaginarlo come una funzione con memoria, che ricorda dove è arrivata l'ultima volta che è stata chiamata e riprende da essa.

In Python, un generatore usa `yield` invece di `return` per restituire ogni valore prodotto.
La funzione built-in `next()` restituisce il prossimo valore prodotto da un generatore ed è utilizzato, ad esempio, dal ciclo `for` per iterare su di esso:

```python
def primes():
    i = 2
    while True:
        if isprime(i):
            yield i
        i += 1

for prime in primes():
    ...
```

## [H]

## [I]

### Imperative Programming

La **programmazione imperativa** è un meccanismo di programmazione che descrive passo dopo passo le istruzioni che il calcolatore deve eseguire. 
Il risultato viene ottenuto modificando lo stato del programma tramite assegnamenti, condizioni e cicli. 

È il paradigma a cui appartiene gran parte del normale codice procedurale Python.

### In-Memory Reference

Un **riferimento in memoria** è il collegamento tra un nome e un oggetto memorizzato. 

In Python una variabile non contiene direttamente l'oggetto: contiene un riferimento a esso. 
Per questo due variabili possono indicare lo stesso oggetto e, se l'oggetto è mutabile, una modifica effettuata attraverso una variabile è visibile anche attraverso l'altra.

La funzione built-in `id(x)` restituisce l'**object identity** correntemente associato alla variabile `x`. Questo corrisponde all'indirizzo di memoria in cui esso è preservato:

```python
x = 10
id(x) # 140708088072920
y = 10
id(y) # same as x, because ints are singletons

v = SomeClass()
id(v) # ...
```

> L'operatore `==` verifica l'**equality** tra i contenuti delle due variabili, determinata tramite il metodo `__eq__`.

> L'operatore `is` verifica invece la **object identity**, ovvero che la corrispondenza tra gli id delle due variabili coinvolte.


### Interpreted Programming Language

Un **linguaggio di programmazione interpretato** viene eseguito con l'aiuto di un interprete, senza produrre necessariamente in anticipo un programma nativo autonomo. 
Questo rende spesso più semplice l'esecuzione e favorisce l'uso interattivo, ma rallenta anche la procedura di esecuzione stessa.

Python è comunemente definito interpretato, anche se la sua implementazione più diffusa compila prima il sorgente in *bytecode*.

## [J]

## [K]

## [L]

### Lambda Function

Una **lambda** è una funzione anonima, cioè definita senza un nome tramite la parola chiave `lambda`. 
Il nome lambda è ereditato dal $\lambda$-calculus, the utilizza la lettera $\lambda$ per indicare un concetto analogo.

In Python può contenere una sola espressione ed è utile quando una funzione breve deve essere passata come valore, per esempio a `map()`, `filter()` o `sorted()`:
```python
from functools import reduce

print(reduce(lambda i, j: i*j, range(1, 10))) 
```

### Lazy Approach

Un **approccio lazy** rimanda un calcolo fino al momento in cui il suo risultato è davvero richiesto. 
Evita così di calcolare o caricare in memoria valori che potrebbero non servire. 

I generatori Python adottano questo approccio, producendo gli elementi uno alla volta.
I tipi stessi di Python utilizzano una **lazy evaluation**: la validità di un'espressione è valutata al momento dell'esecuzione dell'espressione stessa, mai prima.

## [M]

### Monad

Una **monade** è funzione **identità**, accompagnata da un side-effect.
Nasce con l'obiettivo di permettere la composizione di operazioni tramite concatenazione, poiché permette di *sollevare* (lifting) valori ordinari in un contesto.

Ad esempio, la funzione `monadic_print` esegue la stampa ma restituisce anche il valore ricevuto, così che il calcolo possa proseguire all'interno di un'espressione:
```python
def monadic_print(x):
    print(x)
    return x

def echo(): # prints what is inputed and then either quits or repeats
    monadic_print(input()) == 'quit' or echo()
```

## [N]

## [O]

### Object-Based Programming

TODO (dispensa 7)

### Object-Oriented Programming

TODO (dispensa 7)

## [P]

### Pass by Value vs Pass by Reference

Nel **passaggio per valore** una funzione riceve una copia del valore dell'argomento, mentre nel **passaggio per riferimento** riceve una copia del valore dell'indirizzo di memoria in cui l'argomento è memorizzato.
Nel passaggio per valore la funzione non ha dunque accesso al valore della variabile passata dall'esterno, mentre nel passaggio per riferimento è in grado di modificarlo dall'interno.

In Python:
* Gli argomenti sono passati **per valore**.
* Le collezioni, eccetto le tuple, sono passate **per riferimento**.

```python
X = 42
L = [1, 2, 3]

def fake_mutable(i, l): # l is the memory address in which the list starts
    i = i*2
    l[1] = '?!' # this effectively modifies l
    l = {1, 2, 3, 4, 5} # here we are just changing the meaning of the label 'l', so no changes to L is made

fake_mutable(X, L)
print(X, L) # prints 42, [1, '?!', 3]

```

### Programming Paradigm

Un **paradigma di programmazione** è un modello generale che stabilisce come organizzare ed esprimere un programma.

Esempi di paradigmi sono:

- programmazione imperativa;
- programmazione orientata agli oggetti;
- programmazione funzionale.

Un linguaggio può seguire pienamente un solo paradigma, ed essere quindi considerato *puro*, oppure combinare elementi di più paradigmi. 
Python è un linguaggio multiparadigma: è basato su oggetti e supporta, tra gli altri, gli stili imperativo, basato su oggetti e funzionale.

## [Q]

## [R]

### Recursive Function

Una **funzione ricorsiva** è una funzione la cui esecuzione provoca una nuova chiamata a sé stessa, direttamente (**ricorsione diretta**) oppure attraverso altre funzioni (**ricorsione indiretta**).
Deve avere almeno un caso base, che termina la ricorsione, e un passo ricorsivo che avvicina il problema a tale caso.

```python
def fact(n):
    return 1 if n <= 1 else n * fact(n-1)

def fibo(n):
    return n if n <= 1 else fibo(n-1) * fibo(n-2)
```

La ricorsione è generalmente *inefficiente*, a causa dell'**overhead** necessario a creare un nuovo frame (record di attivazione).
Per evitare questa inefficienza, alcuni compilatori (non quello di Python) effettuano un'ottimizzazione nel caso di **ricorsione di coda** (tail recursion): 
se la chiamata ricorsiva è l'ultima operazione della funzione, allora il compilatore può evitare di creare un nuovo record di attivazione e riciclare invece lo stesso, modificando opportunamente i parametri passati come argomenti alla funzione:

```python
def fact(n):
    return 1 if n <= 1 else n * fact(n-1)

def tailfact(n, acc=1):
    return acc if n == 0 else tailfact(n - 1, n * acc)
```

### Regular Expression

Un'**espressione regolare**, o *regex*, è un modello usato per descrivere e riconoscere insiemi di stringhe attraverso *pattern*. 
Consente di cercare, controllare, estrarre o sostituire parti di testo. 

In Python, operazioni con regular expression sono offerte dal modulo `re`:
```python
import re

email = 'test@dremove_thisi.unimi.it'
m = re.search('remove_this', email)
print(email[:m.start()] + email[m.end():]) # test@di.unimi.it 
```

## [S]

### Short-Circuiting

Lo **short-circuiting** è la valutazione parziale di un'espressione logica: l'esecuzione si ferma appena il risultato è già determinabile.
I compilatori sono soliti utilizzare questa proprietà per ottimizzare l'esecuzione.

Si noti che in Python un'espressione booleana restituisce sempre l'ultimo valore valutato. Questo può essere sfruttato all'interno dello short-circuiting:
```python
def fact(n):
    return (n <= 1 and 1) or n * fact(n-1)

def func(x):
    return (x==1 and 'one') or (x==2 and 'two') or 'other'
```

## [T]

## [U]

## [V]

## [W]

## [X]

## [Y]

## [Z]