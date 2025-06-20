import os
import discord
from discord.ext import commands
from flask import Flask
import threading
import requests
import time
import asyncio

# ==== Flask Server (Keep Alive) ====
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot está online!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))  # Usa a porta que o Render fornece, ou 8080 por padrão
    app.run(host='0.0.0.0', port=port)

# ==== Auto-ping: O bot se auto-pinga a cada 10 minutos ====
def auto_ping():
    while True:
        try:
            url = os.getenv("RENDER_EXTERNAL_URL")
            if url:
                requests.get(url)
                print(f"✅ Auto-ping enviado para: {url}")
            else:
                print("⚠️ Variável RENDER_EXTERNAL_URL não encontrada. Auto-ping desativado.")
        except Exception as e:
            print(f"❌ Erro no auto-ping: {e}")
        time.sleep(600)  # A cada 10 minutos (600 segundos)

# ==== Discord Bot Setup ====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

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

# ==== Iniciar tudo ====
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    threading.Thread(target=auto_ping).start()
    asyncio.run(main())
