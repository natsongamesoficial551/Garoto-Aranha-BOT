from discord.ext import commands
import discord

class Sugestoes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sugerir(self, ctx, *, sugestao):
        # Nome exato do canal onde vão as sugestões
        canal_sugestoes_nome = "📢・sugestoes"

        canal = discord.utils.get(ctx.guild.text_channels, name=canal_sugestoes_nome)
        if not canal:
            await ctx.send(f"❌ Não encontrei o canal de sugestões chamado **{canal_sugestoes_nome}**.")
            return

        embed = discord.Embed(
            title="💡 Nova Sugestão!",
            description=f"**Sugestão de:** {ctx.author.mention}\n\n**Sugestão:** {sugestao}",
            color=discord.Color.blue()
        )
        mensagem = await canal.send(embed=embed)
        await mensagem.add_reaction("👍")
        await mensagem.add_reaction("👎")

        await ctx.send(f"✅ Sua sugestão foi enviada para o canal {canal.mention}!")

async def setup(bot):
    await bot.add_cog(Sugestoes(bot))
