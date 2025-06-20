import os
import discord
from discord.ext import commands
from flask import Flask
import threading

# Setup Flask server fake
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot está online!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Inicia o servidor Flask em uma thread separada
threading.Thread(target=run_flask).start()

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Carregar os cogs dinamicamente (suporta cogs com async setup)
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cog carregado: {filename}")
            except Exception as e:
                print(f"❌ Erro ao carregar o cog {filename}: {e}")

async def main():
    await load_cogs()
    await bot.start(os.getenv("TOKEN"))

import asyncio
asyncio.run(main())
