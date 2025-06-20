import random
import asyncio
from discord.ext import commands

class Heroi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.missoes = self.lista_missoes()
        self.progresso = {}  # user_id: {"missao": int, "respeito": int}

    def lista_missoes(self):
        """Lista fixa com 100 missões completas"""
        return [
            "Salvar um gato em uma árvore",
            "Ajudar uma criança perdida no parque",
            "Prender um ladrão de bolsa",
            "Apagar um incêndio pequeno em uma lixeira",
            "Resgatar um filhote em um bueiro",
            "Impedir um ciclista de ser atropelado",
            "Encontrar um cachorro desaparecido",
            "Ajudar uma senhora a atravessar a rua",
            "Controlar um vazamento de gás",
            "Socorrer alguém preso em um elevador",
            "Detonar uma pequena bomba relógio",
            "Desarmar um bandido armado",
            "Impedir um assalto a uma loja",
            "Salvar pessoas de um prédio em chamas",
            "Prender um hacker invadindo sistemas",
            "Impedir uma fuga de criminosos",
            "Derrotar um supervilão local",
            "Resgatar vítimas de um deslizamento de terra",
            "Desativar explosivos em um estádio",
            "Enfrentar uma gangue armada",
            "Impedir um acidente de trem",
            "Combater um incêndio florestal",
            "Proteger um comboio de ajuda humanitária",
            "Salvar reféns em um banco",
            "Interceptar um carregamento ilegal",
            "Resgatar um avião em queda",
            "Derrotar um robô gigante fora de controle",
            "Impedir a queda de um prédio antigo",
            "Salvar civis de uma enchente repentina",
            "Conter uma rebelião de prisioneiros",
            "Enfrentar um monstro subterrâneo",
            "Resgatar pessoas em um navio afundando",
            "Desativar um vírus de computador global",
            "Parar um trem desgovernado",
            "Evitar a queda de um satélite na Terra",
            "Salvar uma cidade de um furacão",
            "Capturar um vilão fugitivo internacional",
            "Impedir um ataque químico",
            "Desativar uma ogiva nuclear",
            "Proteger um político de um atentado",
            "Detonar uma bomba no metrô",
            "Salvar um comboio militar emboscado",
            "Lutar contra uma criatura mutante",
            "Conter um vazamento radioativo",
            "Resgatar astronautas perdidos no espaço",
            "Conter um tsunami iminente",
            "Salvar um ônibus escolar pendurado na ponte",
            "Detonar uma bomba em uma represa",
            "Evitar o colapso de uma usina elétrica",
            "Resgatar vítimas de um terremoto",
            "Lutar contra um exército de drones",
            "Proteger um laboratório com vírus perigosos",
            "Parar uma epidemia de zumbis",
            "Derrotar um dragão que surgiu misteriosamente",
            "Resgatar um comboio médico em zona de guerra",
            "Neutralizar um ataque biológico",
            "Conter um vazamento tóxico em um rio",
            "Evitar o colapso de uma barragem",
            "Lutar contra um ataque de alienígenas",
            "Desativar um campo de minas",
            "Salvar uma cidade de um meteoro",
            "Impedir a queda de um avião comercial",
            "Lutar contra um golem de pedra",
            "Proteger um comboio diplomático",
            "Evitar um ataque cibernético mundial",
            "Salvar um submarino encalhado",
            "Resgatar uma vila em chamas",
            "Derrotar um exército de robôs rebeldes",
            "Conter uma tempestade de areia gigante",
            "Impedir o rompimento de um gasoduto",
            "Resgatar mergulhadores presos",
            "Desativar uma bomba em um hospital",
            "Salvar um trem bala de um descarrilamento",
            "Lutar contra um exército de sombras",
            "Proteger uma cidade de uma nevasca extrema",
            "Resgatar cientistas de um vulcão em erupção",
            "Conter um surto de criaturas mutantes",
            "Desativar uma arma de destruição em massa",
            "Impedir um ataque hacker ao governo",
            "Salvar uma estação espacial de colisão",
            "Proteger um comboio de refugiados",
            "Enfrentar um supervilão interdimensional",
            "Evitar o colapso de um planeta",
            "Derrotar um titã gigante",
            "Conter uma anomalia temporal",
            "Salvar o mundo de um buraco negro",
            "Impedir uma invasão de robôs alienígenas",
            "Resgatar civis de um tornado de energia",
            "Desativar uma bomba de antimatéria",
            "Lutar contra um dragão de fogo",
            "Salvar a lua de ser destruída",
            "Conter uma explosão de matéria escura",
            "Evitar o fim do mundo por um cometa",
            "Resgatar um multiverso em colapso",
            "Derrotar o vilão final: O Devastador de Realidades",
            "Reconstruir a cidade destruída",
            "Salvar os sobreviventes da última batalha",
            "Restaurar a paz mundial",
            "Impedir o surgimento de novos vilões",
            "Ser homenageado como Herói Supremo",
            "Virar lenda e inspiração para novas gerações",
            "Continuar protegendo o mundo para sempre"
        ]

    def get_status(self, user_id):
        if user_id not in self.progresso:
            self.progresso[user_id] = {"missao": 1, "respeito": 0}
        return self.progresso[user_id]

    @commands.command()
    async def missao(self, ctx):
        """Joga a missão atual"""
        user_id = ctx.author.id
        status = self.get_status(user_id)

        if status["missao"] > 100:
            await ctx.send(f"🏅 {ctx.author.mention}, você já completou todas as 100 missões! 👑")
            return

        missao_texto = self.missoes[status["missao"] - 1]
        await ctx.send(f"🦸 **Missão {status['missao']}**: {missao_texto}\n\nDigite `!aceitar` para começar ou `!desistir_missao` para pular.")

        def check(m):
            return m.author.id == user_id and m.channel == ctx.channel and m.content.lower() in ["!aceitar", "!desistir_missao"]

        try:
            resposta = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f"⏳ Tempo esgotado, {ctx.author.mention}. Missão cancelada!")
            return

        if resposta.content.lower() == "!desistir_missao":
            await ctx.send(f"😔 {ctx.author.mention} desistiu da missão...")
            return

        dificuldade = status["missao"]
        chance_base = 70 - (dificuldade // 2)
        chance_base = max(15, chance_base)

        if random.randint(1, 100) <= chance_base:
            ganho = random.randint(5, 20) + dificuldade
            status["respeito"] += ganho
            status["missao"] += 1
            await ctx.send(f"✅ {ctx.author.mention} concluiu a missão e ganhou **{ganho} de Respeito de Herói!** ⭐ Total: **{status['respeito']}**")
        else:
            await ctx.send(f"❌ {ctx.author.mention} falhou na missão... Tente novamente!")

    @commands.command()
    async def respeito(self, ctx):
        """Mostra seu Respeito de Herói"""
        status = self.get_status(ctx.author.id)
        await ctx.send(f"🌟 {ctx.author.mention}, você tem **{status['respeito']} de Respeito de Herói** e está na **Missão {status['missao']} / 100**!")

    @commands.command()
    async def rankheroi(self, ctx):
        """Mostra o top 5 jogadores com mais respeito"""
        if not self.progresso:
            await ctx.send("🏅 Ninguém começou ainda o caminho do herói!")
            return

        ranking = sorted(self.progresso.items(), key=lambda x: x[1]["respeito"], reverse=True)[:5]
        rank_texto = "\n".join([
            f"**#{i+1}** <@{user_id}> - {dados['respeito']} Respeito"
            for i, (user_id, dados) in enumerate(ranking)
        ])

        await ctx.send(f"🏆 **Top 5 Heróis com Mais Respeito:**\n\n{rank_texto}")

async def setup(bot):
    await bot.add_cog(Heroi(bot))
    print("✅ Cog Heroi carregado com sucesso!")
