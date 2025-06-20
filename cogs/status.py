import discord
from discord.ext import commands, tasks
import itertools

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statuses = itertools.cycle([
            "👋 Use !ajuda para ver os comandos",
            f"🛡 Protegendo {len(bot.guilds)} servidores",
            "🎉 Desenvolvido por GarotoAranhaBot",
            "💬 Interaja no chat!"
        ])
        self.mudar_status.start()

    @tasks.loop(seconds=30)  # Troca o status a cada 30 segundos
    async def mudar_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.statuses)))

    @mudar_status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Status(bot))
