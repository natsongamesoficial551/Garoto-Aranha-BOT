import os
import discord
from discord.ext import commands
from flask import Flask
import threading

# --- Parte 1: Servidor Flask para o Render não derrubar a app ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot Discord Rodando!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# --- Parte 2: Bot Discord com carregamento automático de Cogs ---
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("❌ TOKEN não encontrado nas variáveis de ambiente do Render!")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# Carregando todos os Cogs automaticamente
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"✅ Cog carregado: {filename}")
        except Exception as e:
            print(f"❌ Erro ao carregar o cog {filename}: {e}")

# Manter o Flask rodando em paralelo
keep_alive()

# Iniciar o bot
bot.run(TOKEN)
