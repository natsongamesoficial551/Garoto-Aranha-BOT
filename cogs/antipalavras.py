from discord.ext import commands
import discord

class AntiPalavras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Lista de palavras proibidas (você pode adicionar ou remover à vontade)
        self.palavras_proibidas = [
            "caralho", "porra", "merda", "puta", "fdp", "filho da puta", "desgraça",
            "vtnc", "vai se fuder", "bosta", "cacete", "inferno", "maldito", "arrombado",
            "corno", "viado", "piranha", "escroto", "otario", "pau no cu", "babaca",
            "cuzão", "lixo", "imbecil", "idiota", "retardado", "foda-se", "foda se",
            "fodase", "pau no seu cu", "vai tomar no cu", "vai te fuder", "corna",
            "seu merda", "seu lixo", "mongol", "aleijado", "aleijada", "burro", "burra",
            "macaco", "preto imundo", "branquelo", "racista", "nazista", "viado do caralho",
            "gorda", "gordo", "gorda nojenta", "gordo nojento", "retardada", "cuzinha", "bichinha"
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        conteudo = message.content.lower()
        for palavra in self.palavras_proibidas:
            if palavra in conteudo:
                try:
                    await message.delete()
                    await message.channel.send(f"🚫 {message.author.mention}, sua mensagem foi apagada por conter palavras ofensivas! Por favor, respeite as regras do servidor.")
                except:
                    pass
                break

async def setup(bot):
    await bot.add_cog(AntiPalavras(bot))
