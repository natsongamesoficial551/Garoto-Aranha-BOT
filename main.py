import discord
from discord.ext import commands
import os
import asyncio

# Carregar configuração das Environment Variables
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")  # Valor padrão caso não setar no Render

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 Bot {bot.user.name} está online!')

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ Cog carregado: {filename}')
            except Exception as e:
                print(f'❌ Erro ao carregar {filename}: {e}')

async def main():
    await load_extensions()
    await bot.start(TOKEN)

asyncio.run(main())
