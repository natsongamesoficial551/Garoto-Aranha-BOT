import discord
from discord.ext import commands, tasks
import itertools

class MensagensAutomaticas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Lista de mensagens que o bot vai enviar
        self.mensagens = itertools.cycle([
            "📌 Precisa de ajuda? Poste suas dúvidas em <#1376584073136308317>!",
            "📢 Já leu as regras do servidor? Veja em <#1378810461977579735> e fique por dentro de tudo ✅",
            "📝 Precisa de suporte? Abra um ticket usando o comando: `!ticket <motivo>` e a equipe vai te ajudar!"
        ])

        self.enviar_mensagens.start()

    @tasks.loop(hours=1)
    async def enviar_mensagens(self):
        canal = self.bot.get_channel(1376584021823193179)
        if canal:
            mensagem = next(self.mensagens)
            await canal.send(mensagem)

    @enviar_mensagens.before_loop
    async def before_mensagens(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MensagensAutomaticas(bot))
