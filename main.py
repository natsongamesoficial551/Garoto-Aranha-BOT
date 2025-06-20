import os
import discord
from discord.ext import commands

# Pega o token da variável de ambiente
TOKEN = os.getenv("TOKEN")

# Verificação simples para evitar o erro "NoneType"
if TOKEN is None:
    raise ValueError("O TOKEN do bot não foi definido. Configure a variável de ambiente 'TOKEN' no Render.")

# Intents necessários (ajuste se quiser adicionar mais)
intents = discord.Intents.default()
intents.message_content = True  # Necessário para bots que leem mensagens

# Instância do bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento simples pra teste
@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

# Exemplo de comando
@bot.command()
async def ping(ctx):
    await ctx.send('🏓 Pong!')

# Inicializa o bot
bot.run(TOKEN)
