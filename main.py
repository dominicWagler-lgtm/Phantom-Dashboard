import discord
import os
from fastapi import FastAPI
import uvicorn
import threading

# FastAPI-App für das Dashboard erstellen
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Mein Phantom-Dashboard mit FastAPI läuft!"}

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)

# Webserver im Hintergrund starten
def keep_alive():
    t = threading.Thread(target=run_server)
    t.start()

# Discord Bot starten
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user}')

if __name__ == "__main__":
    keep_alive()
    client.run(os.environ.get('DISCORD_TOKEN'))
