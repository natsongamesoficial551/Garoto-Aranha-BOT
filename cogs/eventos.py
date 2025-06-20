from discord.ext import commands
import discord
from datetime import datetime
import random

class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Lista de mensagens de boas-vindas variadas
    mensagens_boas_vindas = [
        "🎉 Que alegria ter você aqui!",
        "🌟 Bem-vindo(a) à nossa comunidade!",
        "🚀 Prepare-se para uma experiência incrível!",
        "✨ Sua presença ilumina nosso servidor!",
        "🎊 Mais um membro incrível se juntou a nós!",
        "🔥 Chegou com tudo por aqui!",
        "💫 Bem-vindo(a) ao nosso cantinho especial!"
    ]
    
    # Lista de mensagens de despedida variadas
    mensagens_despedida = [
        "😢 Nossa, que pena que você está indo...",
        "🚪 As portas sempre estarão abertas para seu retorno!",
        "💔 O servidor fica mais vazio sem você...",
        "🌅 Desejamos boa sorte em sua nova jornada!",
        "👋 Até logo, esperamos te ver novamente!",
        "🕊️ Que sua caminhada seja repleta de sucesso!",
        "⭐ Você sempre será lembrado(a) aqui!"
    ]
    
    # Evento: Membro entrou
    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = discord.utils.get(member.guild.text_channels, name="💬・chat-geral")
        if canal:
            # Escolhe uma mensagem aleatória
            intro_aleatoria = random.choice(self.mensagens_boas_vindas)
            
            # Criar embed de boas-vindas
            embed = discord.Embed(
                title=f"{intro_aleatoria}",
                description=f"Olá {member.mention}! 👋",
                color=0x00ff88,
                timestamp=datetime.now()
            )
            
            # Avatar do membro
            embed.set_thumbnail(url=member.display_avatar.url)
            
            # Informações do servidor
            embed.add_field(
                name="🏠 Bem-vindo(a) ao", 
                value=f"**{member.guild.name}**", 
                inline=False
            )
            
            # Guia rápido
            embed.add_field(
                name="📋 Guia Rápido",
                value=(
                    "💬 **Chat Geral:** Converse com a galera aqui mesmo!\n"
                    "📜 **Regras:** Confira em <#📜・regras> para uma boa convivência\n"
                    "🎮 **Diversão:** Explore nossos canais temáticos\n"
                    "🆘 **Ajuda:** Chame a staff sempre que precisar!"
                ),
                inline=False
            )
            
            # Estatísticas
            embed.add_field(
                name="📊 Você é o membro",
                value=f"**#{member.guild.member_count}**",
                inline=True
            )
            
            embed.add_field(
                name="📅 Conta criada",
                value=member.created_at.strftime("%d/%m/%Y"),
                inline=True
            )
            
            # Mensagem motivacional
            embed.add_field(
                name="💖 Lembre-se",
                value="Respeito e diversão andam juntos! Seja você mesmo(a) e faça novos amigos! 🌟",
                inline=False
            )
            
            # Footer
            embed.set_footer(
                text=f"Divirta-se em {member.guild.name}! ❤️",
                icon_url=member.guild.icon.url if member.guild.icon else None
            )
            
            # Enviar embed
            await canal.send(embed=embed)
            
            # Reação opcional na mensagem
            try:
                message = await canal.fetch_message(canal.last_message_id)
                await message.add_reaction("👋")
                await message.add_reaction("❤️")
            except:
                pass
    
    # Evento: Membro saiu
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = discord.utils.get(member.guild.text_channels, name="💬・chat-geral")
        if canal:
            # Escolhe uma mensagem aleatória
            despedida_aleatoria = random.choice(self.mensagens_despedida)
            
            # Criar embed de despedida
            embed = discord.Embed(
                title=f"{despedida_aleatoria}",
                description=f"**{member.name}#{member.discriminator}** acabou de sair... 😔",
                color=0xff6b6b,
                timestamp=datetime.now()
            )
            
            # Avatar do membro
            embed.set_thumbnail(url=member.display_avatar.url)
            
            # Informações da permanência
            if member.joined_at:
                dias_no_servidor = (datetime.now(member.joined_at.tzinfo) - member.joined_at).days
                embed.add_field(
                    name="⏰ Tempo no servidor",
                    value=f"{dias_no_servidor} dias",
                    inline=True
                )
            
            embed.add_field(
                name="👥 Membros agora",
                value=f"{member.guild.member_count}",
                inline=True
            )
            
            # Mensagem de esperança
            frases_retorno = [
                "As portas sempre estarão abertas! 🚪",
                "Esperamos que volte em breve! 🌟",
                "Sua jornada continua em outro lugar! 🛤️",
                "Que encontre o que procura! 🎯",
                "Boa sorte em seus próximos passos! 🍀"
            ]
            
            embed.add_field(
                name="🌈 Mensagem final",
                value=random.choice(frases_retorno),
                inline=False
            )
            
            # Footer
            embed.set_footer(
                text="Você sempre será bem-vindo(a) de volta! 💙",
                icon_url=member.guild.icon.url if member.guild.icon else None
            )
            
            # Enviar embed
            await canal.send(embed=embed)
            
            # Reação opcional
            try:
                message = await canal.fetch_message(canal.last_message_id)
                await message.add_reaction("😢")
                await message.add_reaction("👋")
            except:
                pass

async def setup(bot):
    await bot.add_cog(Eventos(bot))