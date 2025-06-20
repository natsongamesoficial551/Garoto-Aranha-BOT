import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import asyncio
from datetime import datetime, timedelta
from typing import Optional
import json

class WarnSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_database()
        
        # Configurações de punição (você pode ajustar esses valores)
        self.punishments = {
            3: {"type": "timeout", "duration": 3600, "reason": "3 warns - Timeout de 1 hora"},
            5: {"type": "timeout", "duration": 86400, "reason": "5 warns - Timeout de 24 horas"},
            7: {"type": "kick", "reason": "7 warns - Kick do servidor"},
            10: {"type": "ban", "reason": "10 warns - Ban permanente"}
        }
    
    def init_database(self):
        """Inicializa o banco de dados SQLite"""
        self.conn = sqlite3.connect('warns.db')
        self.cursor = self.conn.cursor()
        
        # Tabela de warns
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS warns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                moderator_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de configurações do servidor
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS guild_config (
                guild_id INTEGER PRIMARY KEY,
                warn_channel_id INTEGER,
                mod_role_id INTEGER,
                punishments TEXT
            )
        ''')
        
        self.conn.commit()
    
    async def get_warn_count(self, user_id: int, guild_id: int) -> int:
        """Retorna o número de warns de um usuário"""
        self.cursor.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id = ? AND guild_id = ?",
            (user_id, guild_id)
        )
        return self.cursor.fetchone()[0]
    
    async def add_warn(self, user_id: int, guild_id: int, moderator_id: int, reason: str):
        """Adiciona um warn ao usuário"""
        self.cursor.execute(
            "INSERT INTO warns (user_id, guild_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
            (user_id, guild_id, moderator_id, reason)
        )
        self.conn.commit()
    
    async def remove_warn(self, warn_id: int, guild_id: int) -> bool:
        """Remove um warn específico"""
        self.cursor.execute(
            "DELETE FROM warns WHERE id = ? AND guild_id = ?",
            (warn_id, guild_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    async def get_user_warns(self, user_id: int, guild_id: int):
        """Retorna todos os warns de um usuário"""
        self.cursor.execute(
            "SELECT id, moderator_id, reason, timestamp FROM warns WHERE user_id = ? AND guild_id = ?",
            (user_id, guild_id)
        )
        return self.cursor.fetchall()
    
    async def apply_punishment(self, member: discord.Member, warn_count: int):
        """Aplica punição baseada no número de warns"""
        if warn_count in self.punishments:
            punishment = self.punishments[warn_count]
            
            try:
                if punishment["type"] == "timeout":
                    until = discord.utils.utcnow() + timedelta(seconds=punishment["duration"])
                    await member.timeout(until, reason=punishment["reason"])
                    return f"**Timeout aplicado:** {punishment['duration']} segundos"
                
                elif punishment["type"] == "kick":
                    await member.kick(reason=punishment["reason"])
                    return f"**Usuário expulso** do servidor"
                
                elif punishment["type"] == "ban":
                    await member.ban(reason=punishment["reason"])
                    return f"**Usuário banido** permanentemente"
                    
            except discord.Forbidden:
                return "❌ Não tenho permissão para aplicar esta punição"
            except discord.HTTPException:
                return "❌ Erro ao aplicar punição"
        
        return None
    
    @commands.command(name="warn", help="Adiciona um warn a um usuário")
    async def warn_command(self, ctx, user: discord.Member, *, reason: str):
        # Verificar permissões
        if not ctx.author.guild_permissions.moderate_members:
            await ctx.send("❌ Você não tem permissão para usar este comando!")
            return
        
        # Verificar se não está tentando dar warn em si mesmo
        if ctx.author.id == user.id:
            await ctx.send("❌ Você não pode dar warn em si mesmo!")
            return
        
        # Verificar se não está tentando dar warn no bot
        if user.bot:
            await ctx.send("❌ Você não pode dar warn em bots!")
            return
        
        # Adicionar warn
        await self.add_warn(user.id, ctx.guild.id, ctx.author.id, reason)
        warn_count = await self.get_warn_count(user.id, ctx.guild.id)
        
        # Criar embed
        embed = discord.Embed(
            title="⚠️ Warn Aplicado",
            color=discord.Color.yellow(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Usuário", value=user.mention, inline=True)
        embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
        embed.add_field(name="Total de Warns", value=f"{warn_count}", inline=True)
        embed.add_field(name="Motivo", value=reason, inline=False)
        
        # Aplicar punição se necessário
        punishment_msg = await self.apply_punishment(user, warn_count)
        if punishment_msg:
            embed.add_field(name="Punição Aplicada", value=punishment_msg, inline=False)
        
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"ID do usuário: {user.id}")
        
        await ctx.send(embed=embed)
        
        # Enviar DM para o usuário (opcional)
        try:
            dm_embed = discord.Embed(
                title=f"⚠️ Você recebeu um warn em {ctx.guild.name}",
                color=discord.Color.yellow(),
                timestamp=datetime.utcnow()
            )
            dm_embed.add_field(name="Motivo", value=reason, inline=False)
            dm_embed.add_field(name="Total de Warns", value=f"{warn_count}", inline=True)
            
            if punishment_msg:
                dm_embed.add_field(name="Punição", value=punishment_msg, inline=False)
            
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            pass  # Usuário tem DMs desabilitadas
    
    @commands.command(name="warns", help="Mostra os warns de um usuário")
    async def warns_command(self, ctx, user: discord.Member = None):
        target_user = user or ctx.author
        warns = await self.get_user_warns(target_user.id, ctx.guild.id)
        
        if not warns:
            embed = discord.Embed(
                title="📋 Warns do Usuário",
                description=f"{target_user.mention} não possui warns!",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="📋 Warns do Usuário",
                description=f"**{target_user.mention}** possui **{len(warns)}** warn(s)",
                color=discord.Color.orange()
            )
            
            for i, (warn_id, mod_id, reason, timestamp) in enumerate(warns, 1):
                moderator = self.bot.get_user(mod_id) or "Moderador Desconhecido"
                embed.add_field(
                    name=f"Warn #{i} (ID: {warn_id})",
                    value=f"**Moderador:** {moderator}\n**Motivo:** {reason}\n**Data:** <t:{int(datetime.fromisoformat(timestamp.replace('Z', '+00:00')).timestamp())}:f>",
                    inline=False
                )
        
        embed.set_thumbnail(url=target_user.display_avatar.url)
        embed.set_footer(text=f"ID do usuário: {target_user.id}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="removewarn", help="Remove um warn específico")
    async def remove_warn_command(self, ctx, warn_id: int):
        # Verificar permissões
        if not ctx.author.guild_permissions.moderate_members:
            await ctx.send("❌ Você não tem permissão para usar este comando!")
            return
        
        success = await self.remove_warn(warn_id, ctx.guild.id)
        
        if success:
            embed = discord.Embed(
                title="✅ Warn Removido",
                description=f"O warn com ID `{warn_id}` foi removido com sucesso!",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=f"Removido por: {ctx.author}")
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Não foi encontrado nenhum warn com ID `{warn_id}` neste servidor.",
                color=discord.Color.red()
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="clearwarns", help="Remove todos os warns de um usuário")
    async def clear_warns_command(self, ctx, user: discord.Member):
        # Verificar permissões
        if not ctx.author.guild_permissions.moderate_members:
            await ctx.send("❌ Você não tem permissão para usar este comando!")
            return
        
        # Contar warns antes de remover
        warn_count = await self.get_warn_count(user.id, ctx.guild.id)
        
        if warn_count == 0:
            await ctx.send(f"❌ {user.mention} não possui warns para remover!")
            return
        
        # Remover todos os warns
        self.cursor.execute(
            "DELETE FROM warns WHERE user_id = ? AND guild_id = ?",
            (user.id, ctx.guild.id)
        )
        self.conn.commit()
        
        embed = discord.Embed(
            title="🗑️ Warns Limpos",
            description=f"Todos os **{warn_count}** warn(s) de {user.mention} foram removidos!",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"Limpo por: {ctx.author}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="warnconfig", help="Mostra as configurações de punição do sistema de warns")
    async def warn_config_command(self, ctx):
        embed = discord.Embed(
            title="⚙️ Configurações do Sistema de Warns",
            description="Punições automáticas baseadas no número de warns:",
            color=discord.Color.blue()
        )
        
        for warn_count, punishment in self.punishments.items():
            punishment_text = ""
            if punishment["type"] == "timeout":
                hours = punishment["duration"] // 3600
                minutes = (punishment["duration"] % 3600) // 60
                if hours > 0:
                    punishment_text = f"Timeout de {hours}h"
                    if minutes > 0:
                        punishment_text += f" e {minutes}min"
                else:
                    punishment_text = f"Timeout de {minutes} minutos"
            elif punishment["type"] == "kick":
                punishment_text = "Expulsão do servidor"
            elif punishment["type"] == "ban":
                punishment_text = "Banimento permanente"
            
            embed.add_field(
                name=f"{warn_count} Warns",
                value=punishment_text,
                inline=True
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WarnSystem(bot))

# Exemplo de como usar no bot principal (main.py):
"""
import discord
from discord.ext import commands

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Criar bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} conectado!')
    # Não precisa mais sincronizar comandos slash

# Carregar o cog
async def main():
    await bot.load_extension('warn_system')  # Nome do arquivo sem .py
    await bot.start('SEU_TOKEN_AQUI')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
"""