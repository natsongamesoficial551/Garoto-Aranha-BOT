from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="📜 Lista de Comandos do Bot",
            description="Aqui estão todos os comandos organizados por categoria:",
            color=discord.Color.blue()
        )

        # 🛡️ Moderação
        embed.add_field(
            name="🛡️ Moderação",
            value=(
                "`!limpar <quantidade>` - Limpa mensagens\n"
                "`!ban <@membro> <motivo>` - Banir membro\n"
                "`!kick <@membro> <motivo>` - Expulsar membro\n"
                "`!mute <@membro> <tempo>` - Mutar membro\n"
                "`!unmute <@membro>` - Desmutar membro\n"
                "`!castigo <@membro>` - Castigar quem mandar link\n"
                "`(Auto)` Anti-link: Castiga quem mandar links ou convites\n"
                "`(Auto)` Anti-palavrões: Bloqueia palavras proibidas"
            ),
            inline=False
        )

        # ⚠️ Avisos / Warns
        embed.add_field(
            name="⚠️ Avisos (Warns)",
            value=(
                "`!warn <@usuário> <motivo>` - Adiciona um warn\n"
                "`!warns [@usuário]` - Mostra os warns de um usuário\n"
                "`!removewarn <warn_id>` - Remove um warn específico pelo ID\n"
                "`!clearwarns <@usuário>` - Remove todos os warns de um usuário\n"
                "`!warnconfig` - Mostra a configuração de punições por warns"
            ),
            inline=False
        )

        # 🎉 Diversão
        embed.add_field(
            name="🎉 Diversão",
            value=(
                "`!piada` - Conta uma piada aleatória\n"
                "`!fato` - Compartilha um fato curioso\n"
                "`!charada` - Apresenta uma charada\n"
                "`!resposta <resposta>` - Responde uma charada\n"
                "`!desistir` - Desiste da charada\n"
                "`!dados [quantidade] [lados]` - Rola dados\n"
                "`!moeda` - Cara ou coroa\n"
                "`!roleta <opções>` - Escolhe uma opção aleatória\n"
                "`!pergunta <pergunta>` - Pergunta sim ou não\n"
                "`!meme` - Envia um meme em texto\n"
                "`!countdown <segundos>` - Faz contagem regressiva (1-10s)"
            ),
            inline=False
        )

        # 🎭 Roleplay / RPG
        embed.add_field(
            name="🎭 Roleplay / RPG",
            value=(
                "**🗡️ Combate:**\n"
                "`!atacar [alvo]` - Ataca inimigos ou outros jogadores\n"
                "`!defender` - Defende e recupera HP\n"
                "`!desafiar @usuário` - Batalha PvP\n\n"

                "**🔮 Magia / Ações:**\n"
                "`!teia` - Lançar teias como o Homem-Aranha\n"
                "`!magica [tipo]` - Magia de fogo, gelo, raio ou cura\n"
                "`!voar` - Voar pelos céus\n"
                "`!transformar [forma]` - Transformar-se em algo\n"
                "`!dancar` - Dançar de forma épica\n\n"

                "**🗺️ Exploração / Inventário:**\n"
                "`!explorar` - Explorar áreas e encontrar itens\n"
                "`!inventario` - Ver seus itens\n"
                "`!curar` - Usar poção de cura\n"
                "`!status` - Mostrar HP, nível e inventário"
            ),
            inline=False
        )

        # 🦸 Modo Herói
        embed.add_field(
            name="🦸 Modo Herói",
            value=(
                "`!missao` - Jogar sua missão atual de herói\n"
                "`!aceitar` - Aceitar a missão\n"
                "`!desistir_missao` - Desistir da missão atual\n"
                "`!respeito` - Ver seu total de Respeito de Herói\n"
                "`!rankheroi` - Ver o Top 5 Heróis com mais respeito"
            ),
            inline=False
        )

        # 💰 Economia / XP / Coins
        embed.add_field(
            name="💰 Economia / XP",
            value=(
                "`!balance` - Ver saldo\n"
                "`!daily` - Recompensa diária\n"
                "`!work` - Trabalhar\n"
                "`!rob` - Tentar roubar alguém\n"
                "`!deposit <quantia>` - Depositar\n"
                "`!withdraw <quantia>` - Sacar\n"
                "`!transfer <@membro> <quantia>` - Transferir\n"
                "`!leaderboard` - Ranking de coins\n"
                "`!coinflip <quantia> <cara/coroa>` - Apostar cara ou coroa\n"
                "`!inventory` - Ver inventário\n"
                "`!shop` - Loja de itens\n"
                "`!buy <item>` - Comprar item\n"
                "`!topxp` - Ranking de XP\n"
                "`(Auto)` XP: Ganha XP ao enviar mensagens"
            ),
            inline=False
        )

        # 💡 Sugestões
        embed.add_field(
            name="💡 Sugestões",
            value="`!sugerir <mensagem>` - Envie uma sugestão para o servidor",
            inline=False
        )

        # 🛡️ Logs / Proteções
        embed.add_field(
            name="🛡️ Proteções / Logs",
            value=(
                "`(Auto)` Sistema de boas-vindas\n"
                "`(Auto)` Sistema de saída\n"
                "`(Auto)` Anti-link / Anti-invite\n"
                "`(Auto)` Anti-palavrões\n"
                "`(Auto)` Sistema de XP\n"
                "`(Auto)` Slowmode e anti-flood (em breve se quiser)"
            ),
            inline=False
        )

        embed.set_footer(text="Use os comandos com o prefixo '!'\nExemplo: !daily")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
    print("✅ Cog Help carregado com sucesso!")
