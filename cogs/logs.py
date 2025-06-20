from discord.ext import commands
import discord

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Canal de logs (ajuste o nome se quiser outro canal)
    async def get_log_channel(self, guild):
        return discord.utils.get(guild.text_channels, name="📑・logs-do-servidor")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = await self.get_log_channel(member.guild)
        if canal:
            await canal.send(f"✅ **{member.name}#{member.discriminator} entrou no servidor.**")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = await self.get_log_channel(member.guild)
        if canal:
            await canal.send(f"❌ **{member.name}#{member.discriminator} saiu do servidor.**")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        canal = await self.get_log_channel(guild)
        if canal:
            await canal.send(f"🔨 **{user.name}#{user.discriminator} foi banido do servidor.**")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        canal = await self.get_log_channel(guild)
        if canal:
            await canal.send(f"✅ **{user.name}#{user.discriminator} foi desbanido.**")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Exemplo simples: detectar se um cargo foi adicionado ou removido (como mute)
        if before.roles != after.roles:
            canal = await self.get_log_channel(after.guild)
            if canal:
                await canal.send(f"🔔 **{after.name}#{after.discriminator} teve mudança de cargos.**")

async def setup(bot):
    await bot.add_cog(Logs(bot))
