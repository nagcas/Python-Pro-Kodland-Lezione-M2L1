
# IMPORT: librerie che utilizzeremo nel programma

import random  # Sceglie un elemento casuale da una lista
import os  # Permette di lavorare con cartelle e file
import requests  # Permette di comunicare con le API tramite Internet
import discord  # Libreria per creare bot Discord

from discord.ext import commands  # Permette di creare comandi come $somma

from settings import *  # Importa le impostazioni, incluso il TOKEN


# Configuriamo gli intent, cioè gli eventi che il bot può ricevere.
intents = discord.Intents.default()
intents.message_content = True  # Permette di leggere i messaggi per i comandi


# Creiamo il bot e scegliamo il prefisso dei comandi: $
bot = commands.Bot(
    command_prefix='$',
    intents=intents
)


# Questa funzione viene eseguita quando il bot si collega a Discord.
@bot.event
async def on_ready():
    print(f'Bot online: {bot.user}')

    # Mostriamo i nomi dei file presenti nella cartella images.
    print(os.listdir('images'))


# COMANDO 1: $somma 5 3
# I due numeri vengono ricevuti come parametri interi.
@bot.command()
async def somma(ctx, numero1: int, numero2: int):
    risultato = numero1 + numero2

    await ctx.send(f'La somma è: {risultato}')


# COMANDO 2: $mem
# Invia un'immagine specifica presente nella cartella images.
@bot.command()
async def mem(ctx):
    with open('images/mem1.png', 'rb') as file:
        picture = discord.File(file)

        # Inviamo l'immagine nel canale Discord.
        await ctx.send(file=picture)


# COMANDO 3: $memr
# Sceglie un'immagine casuale dalla cartella images.
@bot.command()
async def memr(ctx):
    immagini = os.listdir('images')

    # Se la cartella è vuota, non possiamo scegliere un file.
    if not immagini:
        await ctx.send('Non ci sono immagini nella cartella!')
        return

    image_random = random.choice(immagini)

    # Costruiamo il percorso del file selezionato.
    percorso = os.path.join('images', image_random)

    with open(percorso, 'rb') as file:
        picture = discord.File(file)
        await ctx.send(file=picture)


# FUNZIONE DI SUPPORTO: recupera un'immagine casuale di un'anatra.
def get_duck_image_url():
    url_duck = 'https://random-d.uk/api/random'

    # Inviamo una richiesta all'API.
    risposta = requests.get(url_duck, timeout=10)
    risposta.raise_for_status()

    # Convertiamo la risposta JSON in un dizionario Python.
    data = risposta.json()

    # Restituiamo l'indirizzo dell'immagine.
    return data['url']


# COMANDO 4: $duck
@bot.command()
async def duck(ctx):
    try:
        image_url = get_duck_image_url()
        await ctx.send(image_url)
    except (requests.RequestException, ValueError, KeyError):
        await ctx.send('Non riesco a recuperare un anatra adesso!')


# FUNZIONE DI SUPPORTO: recupera un'immagine casuale di un cane.
def get_dog_image_url():
    url_dog = 'https://random.dog/woof.json'

    risposta = requests.get(url_dog, timeout=10)
    risposta.raise_for_status()

    data = risposta.json()
    return data['url']


# COMANDO 5: $dog
@bot.command()
async def dog(ctx):
    try:
        image_url = get_dog_image_url()
        await ctx.send(image_url)
    except (requests.RequestException, ValueError, KeyError):
        await ctx.send('Non riesco a recuperare un cane adesso!')


# FUNZIONE DI SUPPORTO: recupera l'illustrazione di un Pokemon.
def get_pokemon_image_url(name):
    # Inseriamo il nome ricevuto nell'indirizzo dell'API.
    url_pokemon = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'

    risposta = requests.get(url_pokemon, timeout=10)
    risposta.raise_for_status()

    data = risposta.json()

    # Recuperiamo l'illustrazione ufficiale ad alta risoluzione.
    return data['sprites']['other']['official-artwork']['front_default']


# COMANDO 6: $poke pikachu
# Il nome del Pokemon viene passato come parametro.
@bot.command()
async def poke(ctx, name: str):
    try:
        image_url = get_pokemon_image_url(name)

        if image_url:
            # Discord visualizza normalmente l'immagine incorporata nel messaggio.
            await ctx.send(image_url)
        else:
            await ctx.send('Immagine non disponibile per questo Pokemon.')

    except requests.HTTPError:
        await ctx.send('Pokemon non trovato! Controlla il nome.')
    except (requests.RequestException, ValueError, KeyError, TypeError):
        await ctx.send('Si è verificato un errore nel recupero del Pokemon.')


# Avviamo il bot utilizzando il token presente nelle impostazioni.
bot.run(settings['TOKEN'])
