import random
import asyncio
from discord.ext import commands

class Diversao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Lista de piadas
        self.piadas = [
            "Por que o computador foi ao médico? Porque ele estava com um vírus! 😂",
            "O que o pato disse para a pata? Vem quá! 🦆",
            "Por que os pássaros voam para o sul no inverno? Porque é longe demais para ir andando! 🐦",
            "O que é que a impressora falou para a outra impressora? Essa folha é sua ou é impressão minha? 🖨️",
            "Por que o livro de matemática estava triste? Porque tinha muitos problemas! 📚",
            "O que o JavaScript disse para o HTML? Você é muito estático! 💻",
            "Por que o programador foi preso? Porque ele matou o processo! 👮‍♂️",
            "O que é um terremoto? É quando a terra fica nervosa! 🌍",
            "Por que a galinha atravessou a rua? Para mostrar aos gambás que era possível! 🐔",
            "O que é que fica no canto e faz quá-quá? Um pato de castigo! 🦆"
        ]
        
        # Lista de fatos curiosos
        self.fatos_curiosos = [
            "🐙 Os polvos têm 3 corações e sangue azul!",
            "🦆 Os patos não conseguem voar durante a troca de penas!",
            "🐨 Os coalas dormem até 22 horas por dia!",
            "🦒 As girafas só precisam dormir 2 horas por dia!",
            "🐝 As abelhas podem reconhecer rostos humanos!",
            "🐧 Os pinguins podem pular até 3 metros de altura!",
            "🦋 As borboletas provam com os pés!",
            "🐘 Os elefantes são os únicos animais que não conseguem pular!",
            "🦈 Os tubarões existem há mais tempo que as árvores!",
            "🐢 Algumas tartarugas podem viver mais de 150 anos!"
        ]
        
        # Lista de charadas
        self.charadas = [
            {"pergunta": "O que é que tem coroa mas não é rei, tem espinhos mas não é rosa?", "resposta": "abacaxi"},
            {"pergunta": "O que é que quanto mais se tira, maior fica?", "resposta": "buraco"},
            {"pergunta": "O que é que está sempre no meio do começo e no final do fim?", "resposta": "letra m"},
            {"pergunta": "O que é que tem dentes mas não morde?", "resposta": "pente"},
            {"pergunta": "O que é que sobe quando a chuva desce?", "resposta": "guarda-chuva"},
        ]
        
        # Armazenar charadas ativas por canal
        self.charadas_ativas = {}

    @commands.command()
    async def piada(self, ctx):
        """Conta uma piada aleatória"""
        piada = random.choice(self.piadas)
        await ctx.send(piada)

    @commands.command()
    async def fato(self, ctx):
        """Compartilha um fato curioso"""
        fato = random.choice(self.fatos_curiosos)
        await ctx.send(f"**Fato Curioso:** {fato}")

    @commands.command()
    async def charada(self, ctx):
        """Apresenta uma charada para resolver"""
        if ctx.channel.id in self.charadas_ativas:
            await ctx.send("❌ Já existe uma charada ativa neste canal! Use `!resposta <sua_resposta>` para responder.")
            return
            
        charada_escolhida = random.choice(self.charadas)
        self.charadas_ativas[ctx.channel.id] = charada_escolhida
        
        await ctx.send(f"🧩 **CHARADA:** {charada_escolhida['pergunta']}\n\n*Use: `!resposta <sua_resposta>` para responder!*")

    @commands.command()
    async def resposta(self, ctx, *, resposta=None):
        """Responde uma charada ativa"""
        if ctx.channel.id not in self.charadas_ativas:
            await ctx.send("❌ Não há charada ativa neste canal! Use `!charada` para começar uma.")
            return
            
        if not resposta:
            await ctx.send("❌ Você precisa fornecer uma resposta! Exemplo: `!resposta pente`")
            return
            
        charada_ativa = self.charadas_ativas[ctx.channel.id]
        
        if resposta.lower().strip() == charada_ativa['resposta'].lower():
            await ctx.send(f"🎉 **PARABÉNS {ctx.author.mention}!** Você acertou! A resposta era: **{charada_ativa['resposta']}**")
            del self.charadas_ativas[ctx.channel.id]
        else:
            await ctx.send(f"❌ Ops! Não foi dessa vez. Tente novamente!")

    @commands.command()
    async def desistir(self, ctx):
        """Desiste da charada atual"""
        if ctx.channel.id not in self.charadas_ativas:
            await ctx.send("❌ Não há charada ativa neste canal!")
            return
            
        charada_ativa = self.charadas_ativas[ctx.channel.id]
        await ctx.send(f"😔 Que pena! A resposta era: **{charada_ativa['resposta']}**")
        del self.charadas_ativas[ctx.channel.id]

    @commands.command()
    async def roleta(self, ctx, *opcoes):
        """Escolhe uma opção aleatória entre as fornecidas"""
        if len(opcoes) < 2:
            await ctx.send("❌ Você precisa fornecer pelo menos 2 opções!\nExemplo: `!roleta pizza hambúrguer sushi`")
            return
            
        escolha = random.choice(opcoes)
        await ctx.send(f"🎲 **A roleta escolheu:** {escolha}")

    @commands.command()
    async def dados(self, ctx, quantidade: int = 1, lados: int = 6):
        """Rola dados (padrão: 1 dado de 6 lados)"""
        if quantidade < 1 or quantidade > 10:
            await ctx.send("❌ Quantidade deve ser entre 1 e 10!")
            return
            
        if lados < 2 or lados > 100:
            await ctx.send("❌ Lados deve ser entre 2 e 100!")
            return
            
        resultados = [random.randint(1, lados) for _ in range(quantidade)]
        total = sum(resultados)
        
        if quantidade == 1:
            await ctx.send(f"🎲 Você rolou: **{resultados[0]}**")
        else:
            await ctx.send(f"🎲 Você rolou: {resultados}\n**Total:** {total}")

    @commands.command()
    async def moeda(self, ctx):
        """Joga uma moeda"""
        resultado = random.choice(["Cara", "Coroa"])
        emoji = "🪙" if resultado == "Cara" else "👑"
        await ctx.send(f"{emoji} **{resultado}!**")

    @commands.command()
    async def pergunta(self, ctx, *, pergunta=None):
        """Responde sim ou não para uma pergunta"""
        if not pergunta:
            await ctx.send("❌ Você precisa fazer uma pergunta!\nExemplo: `!pergunta Devo estudar hoje?`")
            return
            
        respostas = [
            "Sim! 👍", "Não! 👎", "Talvez... 🤔", "Definitivamente sim! ✅",
            "Definitivamente não! ❌", "Provavelmente sim 😊", "Provavelmente não 😐",
            "Não sei, pergunte novamente 🤷‍♂️", "Certamente! 💪", "Nem pensar! 🙄"
        ]
        
        resposta = random.choice(respostas)
        await ctx.send(f"🎱 **Pergunta:** {pergunta}\n**Resposta:** {resposta}")

    @commands.command()
    async def meme(self, ctx):
        """Compartilha um meme em texto"""
        memes = [
            "```\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⠖⠚⢉⣩⣭⡭⠛⠓⠲⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⢋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀\n     Stonks 📈\n```",
            "```\n  ∩───∩\n  │   │\n  │ ◉ ◉ │  <- Você quando vê uma notificação\n  │   ○   │      do Discord\n  │  ___  │\n  └──┬──┘\n     │\n```",
            "```\n    ¯\\_(ツ)_/¯\n   Quando perguntam\n  se você entendeu\n    a explicação\n```",
            "```\n     /\\_/\\\n    (  o.o  )\n     > ^ <\n\n  Gato digitando...\n  Por favor aguarde\n```"
        ]
        
        meme = random.choice(memes)
        await ctx.send(meme)

    @commands.command()
    async def countdown(self, ctx, segundos: int = 5):
        """Faz uma contagem regressiva"""
        if segundos < 1 or segundos > 10:
            await ctx.send("❌ A contagem deve ser entre 1 e 10 segundos!")
            return
            
        msg = await ctx.send(f"⏰ Contagem regressiva: **{segundos}**")
        
        for i in range(segundos - 1, 0, -1):
            await asyncio.sleep(1)
            await msg.edit(content=f"⏰ Contagem regressiva: **{i}**")
            
        await asyncio.sleep(1)
        await msg.edit(content="🎉 **TEMPO ESGOTADO!** 🎉")

    @commands.command()
    async def diversao_help(self, ctx):
        """Mostra todos os comandos de diversão"""
        embed_content = """
**🎭 COMANDOS DE DIVERSÃO 🎭**

🤣 **!piada** - Conta uma piada aleatória
🤔 **!fato** - Compartilha um fato curioso
🧩 **!charada** - Apresenta uma charada para resolver
💡 **!resposta <resposta>** - Responde uma charada ativa
😔 **!desistir** - Desiste da charada atual

🎲 **!dados [quantidade] [lados]** - Rola dados (padrão: 1d6)
🪙 **!moeda** - Joga uma moeda
🎯 **!roleta <opção1> <opção2> ...** - Escolhe uma opção aleatória
🎱 **!pergunta <sua pergunta>** - Responde sim/não para perguntas

😂 **!meme** - Compartilha um meme em texto
⏰ **!countdown [segundos]** - Faz contagem regressiva (1-10s)

*Divirta-se! 🎉*
        """
        await ctx.send(embed_content)

async def setup(bot):
    await bot.add_cog(Diversao(bot))