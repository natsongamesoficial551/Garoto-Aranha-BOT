from discord.ext import commands
import discord
from datetime import datetime

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Canal de logs (ajuste o nome se quiser outro canal)
    async def get_log_channel(self, guild):
        return discord.utils.get(guild.text_channels, name="📑・logs-do-servidor")
    
    def get_timestamp(self):
        return datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    
    # === EVENTOS DE MEMBROS ===
    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = await self.get_log_channel(member.guild)
        if canal:
            embed = discord.Embed(
                title="👋 Membro Entrou",
                description=f"**{member.mention}** entrou no servidor",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuário", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="🆔 ID", value=member.id, inline=True)
            embed.add_field(name="📅 Conta criada", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Total de membros: {member.guild.member_count}")
            await canal.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = await self.get_log_channel(member.guild)
        if canal:
            embed = discord.Embed(
                title="👋 Membro Saiu",
                description=f"**{member.name}#{member.discriminator}** saiu do servidor",
                color=0xff0000,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuário", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="🆔 ID", value=member.id, inline=True)
            embed.add_field(name="📅 Entrou em", value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "Desconhecido", inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Total de membros: {member.guild.member_count}")
            await canal.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        canal = await self.get_log_channel(guild)
        if canal:
            embed = discord.Embed(
                title="🔨 Membro Banido",
                description=f"**{user.name}#{user.discriminator}** foi banido do servidor",
                color=0x8B0000,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuário", value=f"{user.name}#{user.discriminator}", inline=True)
            embed.add_field(name="🆔 ID", value=user.id, inline=True)
            embed.set_thumbnail(url=user.display_avatar.url)
            await canal.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        canal = await self.get_log_channel(guild)
        if canal:
            embed = discord.Embed(
                title="✅ Membro Desbanido",
                description=f"**{user.name}#{user.discriminator}** foi desbanido",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuário", value=f"{user.name}#{user.discriminator}", inline=True)
            embed.add_field(name="🆔 ID", value=user.id, inline=True)
            embed.set_thumbnail(url=user.display_avatar.url)
            await canal.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        canal = await self.get_log_channel(after.guild)
        if not canal:
            return
        
        # Mudança de nickname
        if before.nick != after.nick:
            embed = discord.Embed(
                title="✏️ Nickname Alterado",
                color=0xffff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuário", value=after.mention, inline=False)
            embed.add_field(name="📝 Antes", value=before.nick or "Sem nickname", inline=True)
            embed.add_field(name="📝 Depois", value=after.nick or "Sem nickname", inline=True)
            embed.set_thumbnail(url=after.display_avatar.url)
            await canal.send(embed=embed)
        
        # Mudança de cargos
        if before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]
            
            if added_roles or removed_roles:
                embed = discord.Embed(
                    title="🔔 Cargos Alterados",
                    color=0x00bfff,
                    timestamp=datetime.now()
                )
                embed.add_field(name="👤 Usuário", value=after.mention, inline=False)
                
                if added_roles:
                    embed.add_field(
                        name="✅ Cargos Adicionados", 
                        value=", ".join([role.mention for role in added_roles]), 
                        inline=False
                    )
                
                if removed_roles:
                    embed.add_field(
                        name="❌ Cargos Removidos", 
                        value=", ".join([role.mention for role in removed_roles]), 
                        inline=False
                    )
                
                embed.set_thumbnail(url=after.display_avatar.url)
                await canal.send(embed=embed)
    
    # === EVENTOS DE MENSAGENS ===
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        
        canal = await self.get_log_channel(message.guild)
        if canal and canal != message.channel:
            embed = discord.Embed(
                title="🗑️ Mensagem Deletada",
                color=0xff6347,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Autor", value=message.author.mention, inline=True)
            embed.add_field(name="📍 Canal", value=message.channel.mention, inline=True)
            embed.add_field(name="💬 Conteúdo", value=message.content[:1000] or "Sem conteúdo texto", inline=False)
            
            if message.attachments:
                embed.add_field(name="📎 Anexos", value=f"{len(message.attachments)} arquivo(s)", inline=True)
            
            embed.set_thumbnail(url=message.author.display_avatar.url)
            await canal.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        
        canal = await self.get_log_channel(before.guild)
        if canal and canal != before.channel:
            embed = discord.Embed(
                title="✏️ Mensagem Editada",
                color=0xffa500,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Autor", value=before.author.mention, inline=True)
            embed.add_field(name="📍 Canal", value=before.channel.mention, inline=True)
            embed.add_field(name="📝 Antes", value=before.content[:500] or "Sem conteúdo", inline=False)
            embed.add_field(name="📝 Depois", value=after.content[:500] or "Sem conteúdo", inline=False)
            embed.add_field(name="🔗 Link", value=f"[Ir para mensagem]({after.jump_url})", inline=False)
            embed.set_thumbnail(url=before.author.display_avatar.url)
            await canal.send(embed=embed)
    
    # === EVENTOS DE CANAIS ===
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        canal = await self.get_log_channel(channel.guild)
        if canal:
            embed = discord.Embed(
                title="📢 Canal Criado",
                description=f"Canal **{channel.name}** foi criado",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="📍 Nome", value=channel.name, inline=True)
            embed.add_field(name="🆔 ID", value=channel.id, inline=True)
            embed.add_field(name="📂 Tipo", value=str(channel.type).replace('_', ' ').title(), inline=True)
            await canal.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        canal = await self.get_log_channel(channel.guild)
        if canal:
            embed = discord.Embed(
                title="🗑️ Canal Deletado",
                description=f"Canal **{channel.name}** foi deletado",
                color=0xff0000,
                timestamp=datetime.now()
            )
            embed.add_field(name="📍 Nome", value=channel.name, inline=True)
            embed.add_field(name="🆔 ID", value=channel.id, inline=True)
            embed.add_field(name="📂 Tipo", value=str(channel.type).replace('_', ' ').title(), inline=True)
            await canal.send(embed=embed)
    
    # === EVENTOS DE VOICE ===
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        canal = await self.get_log_channel(member.guild)
        if not canal:
            return
        
        # Entrou em canal de voz
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(
                title="🔊 Entrou no Voice",
                description=f"**{member.mention}** entrou em **{after.channel.name}**",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await canal.send(embed=embed)
        
        # Saiu do canal de voz
        elif before.channel is not None and after.channel is None:
            embed = discord.Embed(
                title="🔇 Saiu do Voice",
                description=f"**{member.mention}** saiu de **{before.channel.name}**",
                color=0xff0000,
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await canal.send(embed=embed)
        
        # Mudou de canal
        elif before.channel != after.channel and before.channel is not None and after.channel is not None:
            embed = discord.Embed(
                title="🔄 Mudou de Voice",
                description=f"**{member.mention}** mudou de canal",
                color=0xffa500,
                timestamp=datetime.now()
            )
            embed.add_field(name="📤 Saiu de", value=before.channel.name, inline=True)
            embed.add_field(name="📥 Entrou em", value=after.channel.name, inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)
            await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))