from discord.ext import commands
import discord

class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Evento: Membro entrou
    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = discord.utils.get(member.guild.text_channels, name="💬・chat-geral")
        if canal:
            mensagem_boas_vindas = (
                f"👋✨ Olá {member.mention}, seja muito bem-vindo(a) ao servidor **{member.guild.name}!**\n\n"
                "🚀 Esperamos que você aproveite ao máximo sua estadia por aqui!\n"
                "💬 Participe das conversas no canal **#💬・chat-geral**\n"
                "📌 Leia as regras em **#📜・regras** para garantir uma boa convivência\n\n"
                "Qualquer dúvida, chame a staff! 😉\n\n"
                "**Divirta-se e seja respeitoso com todos! ❤️**"
            )
            await canal.send(mensagem_boas_vindas)

    # Evento: Membro saiu
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = discord.utils.get(member.guild.text_channels, name="💬・chat-geral")
        if canal:
            mensagem_despedida = (
                f"😢 **{member.name}** acabou de sair do servidor...\n\n"
                "🚪 Esperamos que volte algum dia!\n\n"
                "🫡 Boa sorte em sua jornada!\n\n"
                "_(A sala fica um pouco mais vazia sem você... 😔)_"
            )
            await canal.send(mensagem_despedida)

async def setup(bot):
    await bot.add_cog(Eventos(bot))
