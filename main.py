import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# === Servidor web fake para enganar o Render ===
app = Flask('')

@app.route('/')
def home():
    return "✅ GarotoAranhaBOT está online!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# === Token do Discord ===
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("❌ O TOKEN do bot não foi definido. Configure a variável de ambiente 'TOKEN' no Render.")

# === Intents do bot ===
intents = discord.Intents.default()
intents.message_content = True  # Necessário para o bot ler mensagens

# === Instância do bot ===
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento: Quando o bot fica online
@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

# Exemplo de comando
@bot.command()
async def ping(ctx):
    await ctx.send('🏓 Pong!')

# === Mantém o web server vivo e inicia o bot ===
keep_alive()
bot.run(TOKEN)
