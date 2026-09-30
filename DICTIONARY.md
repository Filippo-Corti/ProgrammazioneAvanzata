# Programmazione Avanzata

Dizionario dei termini fondamentali presentati durante il corso, con riferimento al contesto del linguaggio Python.

**Indice**:

- Activation Record
- Class-Based Programming
- Closure
- Compiled Programming Language
- Currying
- Deep Copying
- Dynamic Typing
- Functional Programming
- Garbage Collection
- Generator
- Imperative Programming
- In-Memory Reference
- Interpreted Programming Language
- Lambda Function
- Lazy Approach
- Monad
- Object-Based Programming
- Object-Oriented Programming
- Pass by Value vs Pass by Reference
- Programming Paradigm
- Recursive Function
- Regular Expression
- Shallow Copying
- Short-Circuiting
- Tail-Recursive Function

### Activation Record

Un **record di attivazione**, chiamato anche *frame*, è una struttura creata durante ogni chiamata di funzione. 
Conserva le informazioni necessarie alla sua esecuzione, come parametri, variabili locali e punto a cui tornare al termine della chiamata. 
I record di attivazione sono organizzati in uno stack e permettono, tra le altre cose, l'esecuzione di funzioni ricorsive.


### Class-Based Programming

La **programmazione basata su classi** è una forma di programmazione orientata agli oggetti in cui gli oggetti vengono creati a partire da classi. Una classe descrive struttura e comportamento comuni agli oggetti che ne sono istanze e può riutilizzare o estendere altre classi tramite l'ereditarietà. Python supporta questo modello.

### Closure

Una **closure** è una funzione che conserva l'accesso alle variabili dell'ambiente in cui è stata definita, anche quando viene eseguita al di fuori di quell'ambiente. Permette quindi di creare funzioni che ricordano alcuni valori fissati durante la loro costruzione.

### Compiled Programming Language

Un **linguaggio di programmazione compilato** viene tradotto da un compilatore, prima dell'esecuzione, in codice macchina o in un'altra rappresentazione eseguibile. In genere questo riduce il lavoro necessario durante l'esecuzione, ma richiede una fase di compilazione. La distinzione non è sempre netta: Python, per esempio, compila normalmente il codice sorgente in *bytecode*, che viene poi eseguito dalla macchina virtuale Python.

### Currying

Il **currying** trasforma una funzione con più argomenti in una sequenza di funzioni, ciascuna delle quali riceve un argomento e restituisce la funzione successiva. In questo modo è possibile fissare progressivamente alcuni argomenti e ottenere funzioni più specifiche. In Python un'operazione simile, detta applicazione parziale, è fornita da `functools.partial`.

### Deep Copying

La **copia profonda** crea un nuovo oggetto e copia ricorsivamente anche gli oggetti contenuti al suo interno. L'originale e la copia non condividono quindi gli oggetti annidati copiati: modificare una struttura interna della copia non modifica quella dell'originale. In Python si può usare `copy.deepcopy()`.

### Dynamic Typing

La **tipizzazione dinamica** è un sistema nel quale il tipo non è associato in modo fisso al nome di una variabile, ma all'oggetto a cui essa fa riferimento. In Python la stessa variabile può quindi riferirsi, in momenti diversi, a oggetti di tipi diversi; la correttezza delle operazioni viene controllata durante l'esecuzione.

### Functional Programming

La **programmazione funzionale** costruisce i programmi principalmente tramite la composizione e la valutazione di funzioni. Le funzioni sono valori di prima classe, quindi possono essere assegnate a variabili, passate come argomenti e restituite da altre funzioni. Questo paradigma privilegia espressioni, dati immutabili, ricorsione e assenza di effetti collaterali. Python ne supporta diversi elementi, pur non essendo un linguaggio funzionale puro.

### Garbage Collection

La **garbage collection** è il recupero automatico della memoria occupata da oggetti che non sono più raggiungibili dal programma. Il programmatore non deve quindi liberarli manualmente. CPython, l'implementazione più diffusa di Python, usa principalmente il conteggio dei riferimenti, affiancato da un meccanismo capace di individuare anche gruppi di oggetti che si riferiscono ciclicamente tra loro.

### Generator

Un **generatore** è una funzione che produce un valore alla volta invece di calcolare subito l'intera sequenza. In Python usa `yield`: a ogni valore prodotto, l'esecuzione viene sospesa mantenendo il proprio stato e riprende alla successiva richiesta, per esempio tramite `next()` o un ciclo `for`.

### Imperative Programming

La **programmazione imperativa** descrive passo dopo passo le istruzioni che il calcolatore deve eseguire. Il risultato viene ottenuto modificando lo stato del programma tramite assegnamenti, condizioni e cicli. È il paradigma a cui appartiene gran parte del normale codice procedurale Python.

### In-Memory Reference

Un **riferimento in memoria** è il collegamento tra un nome e un oggetto memorizzato. In Python una variabile non contiene direttamente l'oggetto: contiene un riferimento a esso. Per questo due variabili possono indicare lo stesso oggetto e, se l'oggetto è mutabile, una modifica effettuata attraverso una variabile è visibile anche attraverso l'altra.

### Interpreted Programming Language

Un **linguaggio di programmazione interpretato** viene eseguito con l'aiuto di un interprete, senza produrre necessariamente in anticipo un programma nativo autonomo. Questo rende spesso più immediata l'esecuzione e favorisce l'uso interattivo. Python è comunemente definito interpretato, anche se la sua implementazione più diffusa compila prima il sorgente in *bytecode*.

### Lambda Function

Una **funzione lambda** è una piccola funzione anonima, cioè definita senza un nome tramite la parola chiave `lambda`. In Python può contenere una sola espressione ed è utile quando una funzione breve deve essere passata come valore, per esempio a `map()`, `filter()` o `sorted()`.

### Lazy Approach

Un **approccio lazy** rimanda un calcolo fino al momento in cui il suo risultato è davvero richiesto. Evita così di calcolare o caricare in memoria valori che potrebbero non servire. I generatori Python adottano questo approccio, producendo gli elementi uno alla volta.

### Monad

Una **monade** è un'astrazione che racchiude un valore o un calcolo in un contesto e stabilisce come concatenare operazioni che lavorano in quel contesto. Può essere usata, per esempio, per rendere esplicita la gestione degli effetti collaterali. Nelle dispense il termine è usato in senso semplificato: `monadic_print` esegue la stampa ma restituisce anche il valore ricevuto, così il calcolo può proseguire all'interno di un'espressione.

### Object-Based Programming

La **programmazione basata su oggetti** organizza il programma attorno a oggetti che contengono dati e operazioni. A differenza della definizione più completa di programmazione orientata agli oggetti, non richiede necessariamente classi ed ereditarietà. Python è *object-based* nel senso che ogni valore, comprese funzioni e moduli, è un oggetto.

### Object-Oriented Programming

La **programmazione orientata agli oggetti** rappresenta il programma come un insieme di oggetti che combinano stato e comportamento e comunicano tramite operazioni o metodi. Concetti comuni sono incapsulamento, ereditarietà e polimorfismo. Python supporta questo paradigma attraverso classi e oggetti.

### Pass by Value vs Pass by Reference

Nel **passaggio per valore** una funzione riceve una copia del valore dell'argomento, mentre nel **passaggio per riferimento** può agire direttamente sulla variabile del chiamante. Python usa più precisamente il *passaggio per condivisione*: alla funzione viene passato per valore un riferimento allo stesso oggetto. La funzione può quindi modificare un oggetto mutabile ricevuto, come una lista, ma riassegnare il parametro non cambia la variabile del chiamante.

### Programming Paradigm

Un **paradigma di programmazione** è un modello generale che stabilisce come organizzare ed esprimere un programma.

Esempi di paradigmi sono:

- programmazione imperativa;
- programmazione orientata agli oggetti;
- programmazione funzionale.

Un linguaggio può seguire pienamente un solo paradigma, ed essere quindi considerato *puro*, oppure combinare elementi di più paradigmi. Python è un linguaggio multiparadigma: è basato su oggetti e supporta, tra gli altri, gli stili imperativo, orientato agli oggetti e funzionale.

### Recursive Function

Una **funzione ricorsiva** è una funzione la cui esecuzione provoca una nuova chiamata a sé stessa, direttamente oppure attraverso altre funzioni. Deve avere almeno un caso base, che termina la ricorsione, e un passo ricorsivo che avvicina il problema a tale caso.

### Regular Expression

Un'**espressione regolare**, o *regex*, è un modello usato per descrivere e riconoscere insiemi di stringhe. Consente di cercare, controllare, estrarre o sostituire parti di testo. In Python queste operazioni sono offerte dal modulo `re`.

### Shallow Copying

La **copia superficiale** crea un nuovo oggetto esterno, ma non duplica gli oggetti contenuti al suo interno: ne copia soltanto i riferimenti. Originale e copia sono distinti, ma continuano a condividere gli eventuali oggetti annidati. In Python si può usare `copy.copy()`.

### Short-Circuiting

Lo **short-circuiting** è la valutazione parziale di un'espressione logica: l'esecuzione si ferma appena il risultato è già determinabile. In Python `A and B` non valuta `B` se `A` è falso, mentre `A or B` non valuta `B` se `A` è vero. Gli operatori restituiscono uno degli operandi, non necessariamente un valore booleano.

### Tail-Recursive Function

Una **funzione tail-recursive**, o ricorsiva in coda, esegue la chiamata ricorsiva come ultima operazione, senza dover svolgere altri calcoli al suo ritorno. Alcuni linguaggi possono ottimizzarla riutilizzando lo stesso record di attivazione. Python non applica questa ottimizzazione, quindi anche una ricorsione in coda consuma un nuovo frame a ogni chiamata ed è soggetta al limite di ricorsione.
