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

### Bound Method

Un **bound method** (metodo associato) è un oggetto chiamabile che associa una funzione definita in una classe a un'istanza. 

E' sostanzialmente il meccanismo con cui Python implementa i metodi.
Quando un metodo viene invocato, Python passa automaticamente quell'istanza come primo argomento, convenzionalmente chiamato `self`.
L'implementazione avviene tramite Descriptor, dunque attraverso `__get__`
```python
class Counter:
    def increment(self, amount):
        self.value += amount

c = Counter()
c.value = 0

print(Counter.increment)      # Function, corresponds to Counter.__dict__['increment']
print(c.increment)            # Bound method, corresponds to Counter.__dict__['increment'].__get__(c, Counter)

# Therefore this:
c.increment(3)
# is equivalent to this:
Counter.__dict__['increment'].__get__(c, Counter)(3)
```

Anche un `classmethod` produce un bound method, ma associa la classe a `cls`; uno `staticmethod` disabilita invece questo binding automatico.

## [C]

### Class

Una **classe** è un template che fornisce il punto di partenza per creare oggetti con comportamento comune.
Il template descrive un insieme di operazioni comune a tutti gli oggetti di tale classe, permettendo dunque di assumere un **comportamento uniforme**. 
Le classi espongono un insieme di operazioni (**public interface**) a chi vuole interagire con esse in qualità di *client*.

In Python, una classe non è un template rigido: è essa stessa un oggetto, costruito normalmente dalla metaclasse `type`, con un proprio **namespace modificabile a runtime**. 

La chiamata `C(...)` crea un'istanza chiamando prima `C.__new__()` e poi inizializzandola con `C.__init__()`. Gli attributi assegnati a `self` appartengono all'istanza; quelli definiti nel corpo della classe appartengono alla classe e sono condivisi:
```python
class Counter:
    unit = "items"                  # class attribute

    def __init__(self, value=0):
        self.value = value          # instance attribute

    def increment(self):            # instance method (with self)
        self.value += 1

    @staticmethod                   # static method (no self nor cls)
    def is_valid_value(value):
        return type(value) == int

    @classmethod                    # class method (cls instead of self)
    def from_counter(cls, other_counter):
        return cls(other_counter.value)
```

L'espressione `obj.name` viene risolta affidando ogni lettura a `type(obj).__getattribute__(obj, "name")`. L'implementazione di `__getattribute__` cerca poi il nome `name` nell'ordine seguente:

1. Cerca nel `__dict__` della classe di `obj` e in quello delle sue superclassi, seguendo la MRO. Se trova un attributo il cui tipo definisce `__get__()` e anche `__set__()` o `__delete__()`, invoca subito `__get__()`. Un oggetto di questo tipo è detto **data descriptor**.
2. Se non esiste un data descriptor leggibile, cerca il nome nel namespace dell'istanza, normalmente `obj.__dict__`. Un attributo trovato qui può quindi mascherare un normale attributo di classe o un non-data descriptor.
3. Se il nome non è nell'istanza, usa ciò che aveva trovato nella classe o lungo la MRO (che può essere un descriptor senza `__set__()` né `__delete()__`). Se tale oggetto definisce `__get__()`, Python invoca il protocollo dei descriptor; altrimenti restituisce direttamente l'attributo di classe. Questo è ciò che accade, ad esempio, per i metodi di classe (che sono **non-data descriptor**).
4. Se nessuno dei passaggi precedenti trova il nome, e la classe definisce `__getattr__()`, Python chiama `obj.__getattr__("name")` come fallback.
5. Se il fallback non esiste o solleva a sua volta `AttributeError`, l'accesso fallisce con tale eccezione.

```python
class Example:
    category = "class attribute"

    def __init__(self):
        self.value = 10

    @property
    def doubled(self):              # data descriptor
        return self.value * 2

    def show(self):                 # non-data descriptor
        return self.value

    def __getattr__(self, name):
        return f"{name!r} is missing"

obj = Example()
print(obj.value)                    # 10, found in obj.__dict__ (Case 2)
print(obj.category)                 # 'class attribute', found in Example.__dict__ (Case 1)
print(obj.show)                     # bound method, found in Example.__dict but only used at Case 3
print(obj.doubled)                  # 20, found in Example.__dict__ (Case 1)
print(obj.unknown)                  # "'unknown' is missing" (Case 5)

obj.category = "instance attribute" # 'instance attribute', found in Example.__dict__ (Case 1) but not immediately 
print(obj.category)                 #executed as not a data descriptor; then found in obj.__dict__ (Case 2)
                                    
obj.__dict__["doubled"] = 999      
obj.doubled                         # 20, found in Example.__dict__ and a data descriptor (Case 1)
```

### Clientship

La **clientship** è una relazione strutturale nella quale un oggetto, detto *client*, conosce e utilizza i servizi offerti da un altro oggetto. Esprime quindi una relazione *uses-a* o *has-a*, non una relazione *is-a* come l'ereditarietà:

```python
class Formatter:
    def format(self, text):
        return text.upper()

class Report:
    def __init__(self, formatter):
        self.formatter = formatter     # Report usa/possiede un Formatter

    def render(self, text):
        return self.formatter.format(text)
```

La clientship viene spesso realizzata mediante **composition**, conservando l'altro oggetto in un attributo. I due termini non sono quindi da intendere come sinonimi (la composition permette la clientship), ma nella pratica sono spesso usati come tali.

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

### Data Abstraction

La **data abstraction** consiste nel rappresentare un'entità attraverso le operazioni che offre, separando l'interfaccia pubblica dai dettagli della sua rappresentazione interna. Un oggetto è quindi usato in base a *che cosa sa fare*, senza richiedere al client di conoscere *come lo fa*.

Per esempio, chi usa un oggetto `Stack` dovrebbe poter chiamare `push()`, `pop()` e `is_empty()` senza dipendere dal fatto che gli elementi siano conservati in una lista o in un'altra struttura. L'implementazione potrà così cambiare senza modificare il codice client.

L'astrazione è un principio di progettazione; il **data hiding** è uno dei meccanismi con cui si protegge la separazione ottenuta.

### Data Hiding

Il **data hiding** consiste nel limitare l'accesso diretto allo stato interno di un oggetto e nel farlo manipolare attraverso operazioni controllate. Riduce l'accoppiamento con la rappresentazione concreta e permette alla classe di preservare i propri invarianti.

Python segue una filosofia di accesso consensuale, non di privacy rigida:
* Un nome `_internal` è non pubblico (protected) per convenzione, ma non attiva name mangling; 
* Un nome `__internal` è privato per convenzione ed attiva il name mangling, ma rimane accessibile. 

### Dataclass

Una **dataclass** è una classe decorata con `@dataclass`, pensata per conservare e rappresentare dati. 
Il decorator legge gli attributi annotati e genera automaticamente metodi come `__init__()`, `__repr__()` e `__eq__()`; con `order=True` genera anche i confronti d'ordine (`__lt__()`, `__le__()`, etc).

```python
from dataclasses import dataclass, field

@dataclass(slots=True)
class Student:
    name: str
    exams: list[int] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            raise ValueError("empty name")
```

Una dataclass può avere metodi ed essere ereditata come qualsiasi altra classe. 
Opzioni di uso frequente sono:
* `frozen=True`: emula istanze immutabili, lanciando un'eccezione se si tenta di riassegnare un attributo; 
* `slots=True`: genera l'attributo `__slots__`, contenente i campi della dataclass.

### Delegation

La **delegation** è il meccanismo comportamentale con cui un oggetto, invece di eseguire interamente un'operazione, ne affida l'esecuzione a un altro oggetto. 

Due modi con cui può avvenire la delegation sono:
* Tramite **inheritance**, con cui un metodo delega all'implementazione successiva nella MRO, tramite il costrutto `super()`.
    ```python
    class Service:
        def process(self, data):
            return data.strip()

    class LoggedService(Service):
        def process(self, data):
            print("processing")
            return super().process(data)   # delegates via __mro__
    ```
* Tramite **composition**, con cui l'oggetto conserva un collaboratore tra i propri attributi ed inoltra ad esso l'operazione. L'oggetto delegante è *client* del delegato.
    ```python
    class Logger:
        def write(self, message):
            print(message)

    class Service:
        def __init__(self, logger):
            self.logger = logger           # clientship/composition

        def report(self, message):
            self.logger.write(message)     # delegation
    ```

### Descriptors

Un **descriptor** è un oggetto la cui classe definisce almeno uno dei metodi `__get__()`, `__set__()` o `__delete__()`, e che viene assegnato ad un attributo di una classe.

I metodi del descriptor personalizzano ciò che accade quando l'attributo viene rispettivamente letto, assegnato o cancellato:
```python
class Positive:
    def __set_name__(self, owner, name):
        self.storage_name = "_" + name

    def __get__(self, obj, owner=None):
        print("getting...")
        if obj is None:
            return self
        return getattr(obj, self.storage_name)

    def __set__(self, obj, value):
        print("setting...")
        if value <= 0:
            raise ValueError("value must be positive")
        setattr(obj, self.storage_name, value)

class Product:
    price = Positive()

    def __init__(self, price):
        self.price = price

p = Product(10) # prints 'setting...'
p.price = 0 # ValueError: value must be positive
print(p.price) # prints 'getting...' and then 10
```

Un descriptor che definisce soltanto `__get__()` è un **non-data descriptor**.
Un descriptor che definisce `__set__()` o `__delete__()` è un **data descriptor** e ha precedenza sugli attributi presenti nell'istanza.



### `__dict__`

`__dict__` è l'attributo che espone il **namespace** degli oggetti Python, ovvero i nomi che possono essere posti come `obj.name`:
* Per un'istanza di una classe, `__dict__` è un dizionario **mutabile** contenente i suoi attributi user-provided;
* Per un oggetto classe, `__dict__` è una vista di sola lettura (di tipo `mappingproxy`) sul namespace della classe:

```python
class C:
    category = "example"

    def __init__(self):
        self.v = 'param'

    def method():
        return "method"

c = C()
c.answer = '42'

print(C.__dict__)       # mappingproxy({'category': 'example', '__init__': ..., '__method__': ..., ...})
print(c.__dict__)       # {'v': 'param', 'answer': 42}
```

L'attributo `__dict__` permette **introspezione**, ovvero osservare struttura e stato, e **intercessione**, ovvero modificarli a runtime. 
Gli attributi ereditati o risolti nella classe, come `category`, non compaiono nel dizionario dell'istanza. 

Non tutte le istanze possiedono un `__dict__`. 
Una classe può impedire che le sue istanze abbiano un `__dict__` personale, dichiarare `__slots__` con i soli nomi ammessi.
Per ciascun nome, Python crea un **member descriptor** che conserva il valore in uno spazio prefissato. Se nessuna classe base introduce un dizionario e `"__dict__"` non è fra gli slot, le istanze non hanno `__dict__` e non accettano attributi arbitrari. 

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.z = 3 # AttributeError: 'Point' object has no attribute 'z' and no __dict__ for setting new attributes
```

### Dispatching

Il **dispatching** è il processo con cui viene scelta l'implementazione da eseguire per una certa operazione. In una chiamata come `obj.method()`, Python considera il tipo effettivo di `obj` e cerca `method` lungo la sua MRO; poiché la scelta avviene a runtime, si parla di **dynamic dispatch** e quindi di late binding.

```python
class Shape:
    def draw(self): pass

class Circle(Shape):
    def draw(self): return "circle"

shape = Circle()
shape.draw()                    # dispatcher selects Circle.draw
```

### Duck Typing

Il **duck typing** stabilisce se un oggetto è adatto a un'operazione in base al comportamento che offre, non alla classe dichiarata.
Applica il detto “se cammina e starnazza come un'anatra, allora è [trattabile a tutti gli effetti come] un'anatra”.

```python
def print_area(shape):
    print(shape.calculate_area())
```
`print_area()` accetta qualunque oggetto che fornisca un `calculate_area()` compatibile, anche senza una superclasse comune o una dichiarazione formale di interfaccia (e.g. `Shape`). 
Questo produce **polimorfismo strutturale a runtime** ed è coerente con il dynamic typing di Python: se il protocollo richiesto non è rispettato, l'errore emerge quando l'operazione viene eseguita.

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

### Inheritance

L'**inheritance** (ereditarietà) permette a una classe di riusare e specializzare attributi e operazioni di una o più superclassi. 
La nuova classe è detta sottoclasse; può aggiungere nuovi membri oppure fare **override** di quelli ereditati:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
```
Python supporta ereditarietà singola e multipla. La ricerca di un attributo segue la **Method Resolution Order** (MRO) della classe; `super()` consente alle implementazioni di cooperare rispettando tale ordine. `isinstance(obj, C)` e `issubclass(D, C)` verificano le relazioni con classi e superclassi.

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

### Late Binding

Il **late binding** (binding tardivo o dinamico) rimanda fino a runtime la scelta dell'operazione concreta da eseguire. 
Nell'OOP riguarda soprattutto il **dynamic dispatch**: quando viene valutato `obj.method()`, l'implementazione non viene fissata in base al nome della variabile, ma viene cercata sul tipo effettivo di `obj`, seguendo il normale protocollo di accesso agli attributi e la sua MRO.

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

shape = Square(4)
shape.area()                    # 16 (at runtime, we choose Square.area over Shape.area)
```

L'espressione *late binding* viene usata anche in un secondo senso per le **closure**: le variabili libere sono normalmente cercate quando la funzione viene chiamata, non quando viene creata. Tutte le lambda seguenti osservano quindi il valore finale di `i`:

```python
functions = [lambda: i for i in range(3)]       # due to late-binding, i is evaluated on next line, where i=2
print([f() for f in functions])                 # [2, 2, 2]

functions = [lambda i=i: i for i in range(3)]   # i=i forces early binding of i inside the lambda
print([f() for f in functions])                 # [0, 1, 2]
```

### Lazy Approach

Un **approccio lazy** rimanda un calcolo fino al momento in cui il suo risultato è davvero richiesto. 
Evita così di calcolare o caricare in memoria valori che potrebbero non servire. 

I generatori Python adottano questo approccio, producendo gli elementi uno alla volta.
I tipi stessi di Python utilizzano una **lazy evaluation**: la validità di un'espressione è valutata al momento dell'esecuzione dell'espressione stessa, mai prima.

## [M]

### Method Resolution Order (MRO)

La **Method Resolution Order** (**MRO**) è la sequenza di classi in cui Python cerca un attributo. È disponibile nella tupla `ClassName.__mro__` o tramite `ClassName.mro()` e comprende la classe stessa, le superclassi una sola volta e infine `object`.

Con ereditarietà multipla Python calcola la MRO tramite la linearizzazione **C3**, che preserva contemporaneamente:
- la precedenza locale dichiarata nell'elenco delle basi;
- l'ordine imposto dalle MRO delle superclassi;
- la monotonicità, cioè un ordine coerente anche nelle sottoclassi.

Se non esiste una linearizzazione coerente, la definizione della classe fallisce con `TypeError`. C3 risolve in modo deterministico anche il *diamond problem*, nel quale una classe base è raggiungibile attraverso più rami:

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)  # (D, B, C, A, object)
```

Il metodo `super()` restituisce quindi il riferimento alla classe successiva nella sequenza indicata dall'MRO.
Dentro un metodo, `super().method()` equivale a `super(CurrentClass, self).method()`; l'implementazione successiva dipende dunque anche dal tipo effettivo di `self`.

```python
class A: 
    def do_stuff(self):
        print(f'A from {type(self)}')

class B(A): 
    def do_stuff(self):
        super(B, self).do_stuff()
        print('B')

class C(B):
    def do_stuff(self):
        super(C, self).do_stuff()
        print('C')

print(C.__mro__) # (C, B, A, object)
C().do_stuff() # A from C, B, C
B().do_stuff() # A from B, B
```


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

### Name Mangling

Il name mangling è una tecnica di trasformazione del nome con cui una certa entità può essere riferita. Viene utilizzato principalemnte per risolvere il problema di avere un nome univoco per ogni entità.

In Python, il name mangling è applicato a tutti gli attributi di una classe il cui nome è nel formato `__label`. Il risultato del mangling è `_ClassName__label`.
Python assume che gli attributi che iniziano con due underscore siano idealmente **privati**. Non implementando nativamente un meccanismo di controllo degli accessi tra oggetti, utilizza il mangling come mezzo per oscurare (superficialmente) la loro presenza.

```python
class rectangle:
    def __init__(self, w, h):
        self.__w = w
        self.__h = h

    def area(self):
        return self.__w * self.__h
    
    def perimeter(self):
        return 2 * (self.__w + self.__h)

    def __str__(self):
        return f"I'm a Rectangle! My sides are {self.__w} and {self.__h}, my area is {self.area()}"

class square(rectangle):
    def __init__(self, w):
        self.__w = w
        self.__h = w

    def __str__(self):
        return f"I'm a Square! My side is {self.__w} and my area is {self.area()}"


r = rectangle(3, 4)
s = square(3)
print(r) # I'm a Rectangle! My sides are 3 and 4, my area is 12
print(r.__w) # AttributeError: 'rectangle' object has no attribute '__w'
print(r._rectangle__w) # 3
print(s) # AttributeError: 'square' object has no attribute '_rectangle__w'
```


## [O]

### Object-Oriented Programming (OOP)

La **programmazione orientata agli oggetti** organizza il programma intorno a oggetti che possiedono identità, stato e comportamento e che collaborano tramite operazioni.

Secondo la tassonomia di Wagner, si distinguono tre livelli:

- **Object-based programming**: offre oggetti, cioè stato persistente e operazioni che agiscono su di esso;
- **Class-based programming**: rispetto all'object-based programming, aggiunge classi da cui creare famiglie di oggetti con operazioni comuni;
- **Object-oriented programming** in senso stretto: rispetto al class-based programming, aggiunge anche l'ereditarietà fra classi.

Python è normalmente considerato un linguaggio **object-oriented** (o meglio, include l'object-orientation tra i diversi paradigmi che implementa), ma formalmente è solo **object-based**.
Nella pratica, offre un insieme di strumenti che ci permette di trattarlo come se fosse object-oriented, con l'accortezza che le **classi** sono però più dinamiche di un tradizionale linguaggio ad oggetti.

### Object

Un **oggetto** è un'entità dotata di:

- **identità**, stabile per tutta la sua vita e osservabile con `id()` o confrontabile con `is`;
- **tipo**, restituito da `type()`, che ne determina operazioni e comportamento;
- **stato**, che può essere immutabile oppure cambiare nel tempo;
- **operazioni**, esposte attraverso attributi e metodi e operanti tipicamente sullo stato.

In Python ogni valore è un oggetto, incluse funzioni, classi e moduli. 
Un nome di variabile non contiene l'oggetto, ma un riferimento ad esso. Questo fa sì che più nomi possano indicare lo stesso oggetto.
Inoltre, il tipo non è proprietà della variabile ma dell'oggetto stesso.

```python
a = 10
print(type(a)) # <class 'int'>
print(id(a)) # 139972830084680
b = 10
print(a is b) # True (because integers are singletons)
```


## [P]

### Polymorphism

Il **polimorfismo** è il meccanismo che permette di usare la stessa operazione con oggetti di tipi diversi, ottenendo un comportamento appropriato al tipo effettivo dell'oggetto. 
Per esempio, `shape.area()` può invocare implementazioni differenti per un rettangolo e un cerchio.

In Python si manifesta attraverso:
- **polimorfismo per sottotipo**, quando una sottoclasse ridefinisce un metodo ereditato;
- **duck typing**, quando tipi senza una base comune soddisfano comunque lo stesso protocollo;
- **overloading degli operatori**, quando special methods come `__add__()` danno significati specifici a operazioni standard.


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

### Special Methods

I **metodi speciali**, informalmente chiamati *magic methods* o *dunder methods*, sono hook con nomi riservati della forma `__name__` ai quali il data model di Python associa un significato. 
Permettono a una classe di partecipare ai protocolli del linguaggio: costruzione, stampa, operatori, indicizzazione, iterazione, context managment, etc.

Si distinguono dai metodi ordinari per il fatto che Python li può invocare implicitamente in risposta a un'operazione. Per esempio, `len(x)` cerca `type(x).__len__`, mentre `x + y` prova `type(x).__add__` e, quando previsto, `type(y).__radd__`.

La ricerca implicita avviene normalmente sulla **classe**, non nel `__dict__` dell'istanza, e può bypassare anche il normale `__getattribute__()` dell'istanza:
```python
class C():
    def __len__(self):
        return 0
c = C()
print(len(C))   # 0
c.__len__ = lambda: 1
print(len(C))   # still 0
```

Il seguente è il catalogo dei metodi speciali del **data model del linguaggio Python 3**, raggruppati per protocollo.

| Protocollo | Metodi speciali |
|---|---|
| Creazione e ciclo di vita | `__new__`, `__init__`, `__del__` |
| Rappresentazione e conversione testuale | `__repr__`, `__str__`, `__bytes__`, `__format__` |
| Confronto ricco | `__lt__`, `__le__`, `__eq__`, `__ne__`, `__gt__`, `__ge__` |
| Hash e valore di verità | `__hash__`, `__bool__` |
| Accesso agli attributi | `__getattribute__`, `__getattr__`, `__setattr__`, `__delattr__`, `__dir__` |
| Protocollo dei descriptor | `__get__`, `__set__`, `__delete__`, `__set_name__` |
| Oggetti chiamabili | `__call__` |
| Creazione e personalizzazione delle classi | `__init_subclass__`, `__mro_entries__`, `__prepare__`, `__class_getitem__`, `__instancecheck__`, `__subclasscheck__` |
| Dimensione e accesso a collezioni | `__len__`, `__length_hint__`, `__getitem__`, `__setitem__`, `__delitem__`, `__missing__` |
| Iterazione e appartenenza | `__iter__`, `__next__`, `__reversed__`, `__contains__` |
| Operatori unari | `__neg__`, `__pos__`, `__abs__`, `__invert__` |
| Conversioni numeriche | `__complex__`, `__int__`, `__float__`, `__index__` |
| Arrotondamento | `__round__`, `__trunc__`, `__floor__`, `__ceil__` |
| Context manager | `__enter__`, `__exit__` |
| Awaitable e iterazione asincrona | `__await__`, `__aiter__`, `__anext__` |
| Context manager asincrono | `__aenter__`, `__aexit__` |
| Buffer protocol | `__buffer__`, `__release_buffer__` |
| Valutazione lazy delle annotazioni (Python 3.14+) | `__annotate__` |

Gli operatori binari hanno tre famiglie. Il metodo **diretto** gestisce `x op y`; quello **riflesso** permette all'operando destro di gestire l'operazione quando il sinistro non la supporta, restituendo `NotImplemented`; quello **in-place** gestisce `x op= y`. I nomi completi sono:

| Operazione | Diretto | Riflesso | In-place |
|---|---|---|---|
| `+` | `__add__` | `__radd__` | `__iadd__` |
| `-` | `__sub__` | `__rsub__` | `__isub__` |
| `*` | `__mul__` | `__rmul__` | `__imul__` |
| `@` | `__matmul__` | `__rmatmul__` | `__imatmul__` |
| `/` | `__truediv__` | `__rtruediv__` | `__itruediv__` |
| `//` | `__floordiv__` | `__rfloordiv__` | `__ifloordiv__` |
| `%` | `__mod__` | `__rmod__` | `__imod__` |
| `divmod()` | `__divmod__` | `__rdivmod__` | — |
| `pow()` o `**` | `__pow__` | `__rpow__` | `__ipow__` |
| `<<` | `__lshift__` | `__rlshift__` | `__ilshift__` |
| `>>` | `__rshift__` | `__rrshift__` | `__irshift__` |
| `&` | `__and__` | `__rand__` | `__iand__` |
| `^` | `__xor__` | `__rxor__` | `__ixor__` |
| `\|` | `__or__` | `__ror__` | `__ior__` |

Alcune precisazioni evitano confusioni frequenti:

- `__repr__()` dovrebbe produrre una rappresentazione non ambigua, utile allo sviluppatore; `__str__()` una rappresentazione leggibile per l'utente. In assenza di `__str__()`, viene usato `__repr__()`.
- `__eq__()` non deve sollevare automaticamente un errore per tipi non supportati: può restituire `NotImplemented`, lasciando a Python la possibilità di provare l'operazione riflessa o il fallback appropriato.
- `__iter__()` restituisce un iteratore; l'iteratore stesso espone `__next__()` e solleva `StopIteration` quando è esaurito.
- `__getitem__()` può rendere un oggetto indicizzabile e, come fallback storico, iterabile. `__missing__()` viene consultato soltanto dalle sottoclassi di `dict` per una chiave assente.
- `__enter__()` restituisce il valore legato da `as`; `__exit__()` riceve le informazioni sull'eventuale eccezione e può sopprimerla restituendo un valore vero.
- `__del__()` è un finalizzatore, non un distruttore deterministico: non bisogna basare su di esso il rilascio tempestivo di risorse. Per questo si preferiscono context manager e `with`.

Esistono inoltre hook `dunder` definiti da protocolli della **standard library**, non dalle operazioni fondamentali del data model. Fra quelli più comuni:

- copia: `__copy__`, `__deepcopy__`;
- serializzazione con `pickle`: `__reduce__`, `__reduce_ex__`, `__getnewargs__`, `__getnewargs_ex__`, `__getstate__`, `__setstate__`;
- percorsi del filesystem: `__fspath__`;
- Abstract Base Classes: `__subclasshook__`.

Infine, non ogni nome `dunder` è un metodo. `__dict__`, `__slots__`, `__class__`, `__bases__`, `__mro__`, `__name__`, `__qualname__`, `__module__`, `__doc__`, `__annotations__` e `__match_args__`, per esempio, sono **attributi speciali**. Il loro valore partecipa a un protocollo, ma non viene chiamato come una funzione. `__annotate__`, introdotto in Python 3.14 per la valutazione differita delle annotazioni, è invece un attributo speciale chiamabile e costituisce quindi un caso di confine. Non si dovrebbero inventare nuovi nomi `__qualcosa__`, perché questa forma è riservata a Python e potrebbe acquisire un significato in versioni future.

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
