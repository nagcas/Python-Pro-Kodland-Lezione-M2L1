# Discord Bot didattico --- Kodland

Un semplice bot Discord scritto in Python per imparare a creare comandi,
usare file locali e recuperare immagini da API pubbliche.

## Funzionalità

Il bot include questi comandi:

  --------------------------------------------------------------------------
  Comando                    Descrizione             Esempio
  -------------------------- ----------------------- -----------------------
  `$somma numero1 numero2`   Somma due numeri interi `$somma 5 3`

  `$mem`                     Invia un'immagine       `$mem`
                             specifica dalla         
                             cartella `images`       

  `$memr`                    Sceglie e invia         `$memr`
                             un'immagine casuale     
                             dalla cartella `images` 

  `$duck`                    Recupera un'immagine    `$duck`
                             casuale di un'anatra    

  `$dog`                     Recupera un'immagine    `$dog`
                             casuale di un cane      

  `$poke nome`               Recupera                `$poke pikachu`
                             l'illustrazione         
                             ufficiale di un Pokémon 
  --------------------------------------------------------------------------

## 1. Requisiti

-   Python 3.11 o una versione compatibile.
-   Un account Discord.
-   Un'applicazione bot creata nel [Discord Developer
    Portal](https://discord.com/developers/applications).
-   Visual Studio Code o un altro editor Python.

## 2. Installazione delle librerie

Apri il terminale nella cartella del progetto ed esegui:

``` bash
- per WINDOWS
py -3.11 -m pip install discord requests

-per MAC OS
python3 -3.100 -m pip install discor requests
```

Se il comando `py -3.11` non è disponibile, prova:

``` bash
python -m pip install discord requests

oppure

python3 -m pip install discord requests
```

### A cosa servono le librerie?

  ------------------------------------------------------------------------
  Libreria                 Tipo                    Utilizzo
  ------------------------ ----------------------- -----------------------
  `random`                 Standard Python         Sceglie casualmente un
                                                   elemento da una lista.

  `os`                     Standard Python         Legge i contenuti di
                                                   cartelle e costruisce
                                                   percorsi dei file.

  `requests`               Esterna                 Invia richieste HTTP
                                                   alle API e riceve le
                                                   risposte.

  `discord.py` (`discord`) Esterna                 Permette di creare un
                                                   bot e interagire con
                                                   Discord.

  `discord.ext.commands`   Parte di `discord.py`   Gestisce i comandi, i
                                                   parametri e il prefisso
                                                   `$`.
  ------------------------------------------------------------------------

Le librerie standard `random` e `os` sono già incluse in Python. Non
occorre installarle separatamente.

## 3. Struttura del progetto

Organizza i file in questo modo:

``` text
progetto_bot/
├── bot.py
├── settings.py
└── images/
    ├── mem1.png
    ├── mem2.png
    └── mem3.png
```

-   `bot.py`: contiene il codice del bot.
-   `settings.py`: contiene il token segreto del bot.
-   `images/`: contiene le immagini utilizzate dai comandi `$mem` e
    `$memr`.

I nomi e i formati dei file nella cartella `images` devono corrispondere
a quelli effettivamente presenti.

## 4. Configurare Discord e il token

1.  Apri il [Discord Developer
    Portal](https://discord.com/developers/applications).
2.  Crea una nuova applicazione.
3.  Apri la sezione **Bot** e crea il bot, se necessario.
4.  Nella sezione **Bot**, abilita **Message Content Intent**.
5.  Copia il token e inseriscilo nel file `settings.py`.
6.  Invita il bot nel server tramite la sezione **OAuth2 / URL
    Generator**, selezionando gli scope `bot` e, se desideri usare i
    comandi slash in futuro, `applications.commands`. Per questo
    progetto con prefisso `$`, è sufficiente lo scope `bot`.
7.  Concedi soltanto i permessi necessari, come leggere i messaggi e
    inviare messaggi e allegati.

Crea il file `settings.py` con questo contenuto:

``` python
settings = {
    'TOKEN': 'INSERISCI_QUI_IL_TOKEN'
}
```

**Sicurezza:** il token è una credenziale segreta. Non pubblicarlo su
GitHub, non inviarlo in chat e non inserirlo direttamente nel codice
condiviso. Aggiungi `settings.py` al file `.gitignore`. Se il token
viene esposto, rigeneralo dal Developer Portal.

Esempio di `.gitignore`:

``` gitignore
settings.py
__pycache__/
.venv/
```

## 5. Avviare il bot

Dal terminale, nella cartella che contiene `bot.py`, esegui:

``` bash
py -3.11 bot.py
```

Se la configurazione è corretta, nel terminale apparirà un messaggio
simile a:

``` text
Bot online: NomeDelTuoBot
```

Lascia il programma in esecuzione mentre provi i comandi nel server
Discord.

## 6. Come funzionano i comandi

### `$somma 5 3`

Il bot riceve due parametri, li converte in numeri interi grazie alle
annotazioni `int` e calcola la somma.

``` python
@bot.command()
async def somma(ctx, numero1: int, numero2: int):
    risultato = numero1 + numero2
    await ctx.send(f'La somma è: {risultato}')
```

-   `@bot.command()` registra la funzione come comando.
-   `ctx` è il contesto del comando: contiene informazioni sul messaggio
    e sul canale.
-   `numero1` e `numero2` sono i parametri ricevuti.
-   `await ctx.send(...)` invia una risposta nel canale Discord.

Se i parametri non sono numeri interi validi, `discord.py` segnala un
errore di conversione. In un progetto più avanzato è possibile gestire
questi errori con un gestore dedicato.

### `$mem`

Apre un file locale in modalità binaria (`rb`), lo converte in un
allegato Discord e lo invia nel canale.

``` python
with open('images/mem1.png', 'rb') as file:
    picture = discord.File(file)
    await ctx.send(file=picture)
```

La cartella `images` deve essere raggiungibile dal percorso di
esecuzione del programma.

### `$memr`

`os.listdir('images')` restituisce i nomi degli elementi presenti nella
cartella. `random.choice(...)` ne sceglie uno casualmente.
`os.path.join(...)` costruisce il percorso del file.

Il codice didattico presuppone che la cartella contenga soltanto
immagini valide. Se inserisci anche sottocartelle o file non supportati,
filtra l'elenco prima di scegliere un elemento.

### `$duck` e `$dog`

Questi comandi usano API pubbliche per recuperare immagini di animali.

Il procedimento è:

1.  `requests.get(url, timeout=10)` invia una richiesta HTTP.
2.  `raise_for_status()` segnala una risposta HTTP di errore.
3.  `response.json()` converte il JSON ricevuto in un dizionario Python.
4.  Il codice estrae il campo `url`.
5.  `ctx.send(image_url)` invia il link su Discord, che normalmente
    mostra un'anteprima se il collegamento è accessibile e supportato.

Le API esterne possono essere temporaneamente non disponibili; per
questo è importante gestire gli errori di rete.

### `$poke pikachu`

Il comando utilizza la [PokeAPI](https://pokeapi.co/) per recuperare i
dati di un Pokémon.

L'indirizzo viene costruito inserendo il nome:

``` python
url_pokemon = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
```

Per esempio, per Pikachu:

``` text
https://pokeapi.co/api/v2/pokemon/pikachu
```

La risposta è un JSON. L'immagine ufficiale ad alta risoluzione si trova
nel percorso:

``` python
data['sprites']['other']['official-artwork']['front_default']
```

Questa espressione attraversa più dizionari annidati: prima `sprites`,
poi `other`, quindi `official-artwork` e infine `front_default`.

Esempi di comandi:

``` text
$poke pikachu
$poke charmander
$poke bulbasaur
$poke eevee
$poke lucario
```

Scrivi i nomi dei Pokémon in inglese, senza spazi. Se il Pokémon non
esiste o l'API non risponde, il bot deve mostrare un messaggio d'errore
invece di terminare.

## 7. Concetti Python da ricordare

-   **Import:** rende disponibili moduli e funzionalità.
-   **Funzione:** raggruppa istruzioni riutilizzabili.
-   **Parametro:** è un dato passato a una funzione o a un comando.
-   **Decoratore:** `@bot.command()` registra una funzione come comando
    Discord.
-   **Funzione asincrona:** `async def` definisce una funzione che può
    usare `await`.
-   **Richiesta HTTP:** permette di comunicare con un servizio web.
-   **JSON:** formato testuale utilizzato dalle API per restituire dati
    strutturati.
-   **Eccezione:** rappresenta un errore che può essere gestito con
    `try` e `except`.

## 8. Esercizi per gli studenti

1.  Modifica `$somma` per calcolare anche la sottrazione.
2.  Aggiungi nuove immagini nella cartella `images` e prova `$memr`.
3.  Crea un comando `$coin` che restituisca casualmente `testa` oppure
    `croce`.
4.  Modifica `$poke` per stampare anche il nome e il numero
    identificativo del Pokémon.
5.  Aggiungi un controllo per gestire un nome Pokémon vuoto o non
    valido.
6.  Crea un comando che recuperi più informazioni del Pokémon, come
    altezza, peso e tipo.

## 9. Risoluzione dei problemi

**Il bot è online ma non riconosce i comandi** - Controlla che **Message
Content Intent** sia abilitato nel Developer Portal e nel codice. -
Verifica che il comando inizi con `$`. - Controlla che il bot possa
leggere i messaggi e inviare risposte nel canale.

**`ModuleNotFoundError`** - Installa le dipendenze usando lo stesso
interprete Python con cui avvii il bot.

**`FileNotFoundError`** - Controlla che `images/` esista e che il nome
del file sia corretto. - Avvia il programma dalla cartella del progetto.

**Il comando Pokémon risponde che il Pokémon non è stato trovato** -
Controlla la grafia inglese del nome. - Verifica che la PokeAPI sia
raggiungibile.

**Il bot non si collega** - Controlla il token in `settings.py`. - Se il
token è stato condiviso accidentalmente, rigeneralo.

------------------------------------------------------------------------

Progetto didattico per esercitarsi con Python, Discord, file locali,
funzioni, richieste HTTP e API pubbliche.
