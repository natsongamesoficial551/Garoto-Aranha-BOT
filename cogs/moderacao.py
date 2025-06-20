import discord
from discord.ext import commands
import asyncio
import re

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando: Limpar mensagens
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def limpar(self, ctx, quantidade: int):
        await ctx.channel.purge(limit=quantidade + 1)
        await ctx.send(f"✅ {quantidade} mensagens apagadas por {ctx.author.mention}!", delete_after=5)

    # Comando: Kick
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, membro: discord.Member, *, motivo="Nenhum motivo informado"):
        await membro.kick(reason=motivo)
        await ctx.send(f"✅ **Usuário expulso:** {membro.mention}\n📝 **Motivo:** {motivo}")

    # Comando: Ban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, membro: discord.Member, *, motivo="Nenhum motivo informado"):
        await membro.ban(reason=motivo)
        await ctx.send(f"✅ **Usuário banido:** {membro.mention}\n📝 **Motivo:** {motivo}")

    # Comando: Unban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, membro_nome_tag):
        bans = await ctx.guild.bans()
        nome, tag = membro_nome_tag.split('#')

        for ban_entry in bans:
            user = ban_entry.user
            if (user.name, user.discriminator) == (nome, tag):
                await ctx.guild.unban(user)
                await ctx.send(f"✅ **Usuário desbanido:** {user.name}#{user.discriminator}")
                return

        await ctx.send(f"❌ Usuário `{membro_nome_tag}` não encontrado na lista de banidos.")

    # Comando: Mute
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, membro: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name="Mutado")

        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Mutado")
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(mute_role, send_messages=False)

        await membro.add_roles(mute_role)
        await ctx.send(f"🔇 {membro.mention} foi silenciado!")

    # Comando: Unmute
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, membro: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name="Mutado")
        if mute_role in membro.roles:
            await membro.remove_roles(mute_role)
            await ctx.send(f"🔊 {membro.mention} pode falar novamente!")
        else:
            await ctx.send(f"❌ {membro.mention} não está mutado.")

    # Sistema Anti-Link com Castigo de 24h
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Ignorar admins
        if message.author.guild_permissions.administrator:
            return

        # Verificar se a mensagem contém link ou convite de servidor
        link_pattern = r"(https?://\S+|discord\.gg/\S+)"
        if re.search(link_pattern, message.content):
            try:
                await message.delete()
            except:
                pass

            # Criar cargo "Castigado" se não existir
            role_name = "Castigado"
            castigo_role = discord.utils.get(message.guild.roles, name=role_name)

            if not castigo_role:
                castigo_role = await message.guild.create_role(name=role_name)
                for channel in message.guild.text_channels:
                    await channel.set_permissions(castigo_role, send_messages=False)

            # Aplicar o castigo
            await message.author.add_roles(castigo_role)

            aviso = (
                f"🚫 {message.author.mention}, você foi colocado de **castigo por 24 horas** por enviar **links ou convites de servidor sem permissão!**\n\n"
                "⏳ Durante esse período, você **não poderá mandar mensagens em nenhum canal de texto**.\n"
                "📢 Se achar que isso foi um engano, entre em contato com a equipe de administração."
            )
            try:
                await message.channel.send(aviso)
            except:
                pass

            # Esperar 24 horas (86400 segundos)
            await asyncio.sleep(86400)

            # Remover o castigo
            await message.author.remove_roles(castigo_role)
            try:
                await message.author.send(f"✅ Seu castigo de 24 horas no servidor **{message.guild.name}** terminou! Você pode falar novamente nos chats.")
            except:
                pass

async def setup(bot):
    await bot.add_cog(Moderacao(bot))
