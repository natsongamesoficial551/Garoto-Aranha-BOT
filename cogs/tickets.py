import discord
from discord.ext import commands
import asyncio

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx, *, motivo="Sem motivo"):
        guild = ctx.guild
        categoria = discord.utils.get(guild.categories, name="Tickets")

        # Criar categoria se não existir
        if categoria is None:
            categoria = await guild.create_category("Tickets")

        # Criar canal privado para o ticket
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        canal = await guild.create_text_channel(f"ticket-{ctx.author.name}", category=categoria, overwrites=overwrites)
        await canal.send(f"🎟️ {ctx.author.mention}, seu ticket foi criado!\nMotivo: **{motivo}**\n\n🔒 Quando terminar, digite `!fecharticket` para fechar.")

    @commands.command()
    async def fecharticket(self, ctx):
        if ctx.channel.category and ctx.channel.category.name == "Tickets":
            await ctx.send("✅ Fechando o ticket em 5 segundos...")
            await asyncio.sleep(5)
            await ctx.channel.delete()
        else:
            await ctx.send("❌ Este comando só pode ser usado dentro de um ticket.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
