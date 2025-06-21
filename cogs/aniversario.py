import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime

CAMINHO_JSON = 'C:\\Users\\Admin\\GarotoAranhaBot\\cogs\\aniversarios.json'
CANAL_ANIVERSARIOS = 1382522505603842110  # Troque pelo ID do canal de aniversário

def carregar_aniversarios():
    if os.path.exists(CAMINHO_JSON):
        try:
            with open(CAMINHO_JSON, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Arquivo vazio ou inválido
            return {}
    else:
        return {}

def salvar_aniversarios(aniversarios):
    with open(CAMINHO_JSON, 'w') as f:
        json.dump(aniversarios, f, indent=4, ensure_ascii=False)

class Aniversario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verificar_aniversarios.start()

    def cog_unload(self):
        self.verificar_aniversarios.cancel()

    @commands.command(name='setaniversario')
    async def set_aniversario(self, ctx, *, data):
        """
        Salva a data de aniversário do usuário no formato DD/MM.
        Exemplo: !setaniversario 20/06
        """
        aniversarios = carregar_aniversarios()
        user_id = str(ctx.author.id)
        aniversarios[user_id] = data
        salvar_aniversarios(aniversarios)
        await ctx.send(f"✅ {ctx.author.name}, seu aniversário foi salvo como: {data}")

    @commands.command(name='meuaniversario')
    async def meu_aniversario(self, ctx):
        """
        Mostra a data de aniversário do usuário.
        """
        aniversarios = carregar_aniversarios()
        user_id = str(ctx.author.id)
        if user_id in aniversarios:
            await ctx.send(f"🎉 {ctx.author.name}, seu aniversário é: {aniversarios[user_id]}")
        else:
            await ctx.send(f"❌ {ctx.author.name}, você ainda não cadastrou seu aniversário. Use `!setaniversario <data>`.")

    @commands.command(name='aniversarios')
    async def listar_aniversarios(self, ctx):
        """
        Mostra todos os aniversários cadastrados no bot.
        """
        aniversarios = carregar_aniversarios()
        if not aniversarios:
            await ctx.send("❌ Nenhum aniversário cadastrado ainda.")
            return
        
        linhas = []
        for user_id, data in aniversarios.items():
            user = self.bot.get_user(int(user_id))
            nome = user.name if user else f"Usuário ID {user_id}"
            linhas.append(f"**{nome}**: {data}")
        
        # Monta a mensagem dividindo em blocos para não passar do limite do Discord (2000 chars)
        mensagem = "🎂 **Aniversários cadastrados:**\n" + "\n".join(linhas)
        if len(mensagem) > 2000:
            # Se passar do limite, envia em partes menores
            partes = []
            parte_atual = "🎂 **Aniversários cadastrados:**\n"
            for linha in linhas:
                if len(parte_atual) + len(linha) + 1 > 2000:
                    partes.append(parte_atual)
                    parte_atual = ""
                parte_atual += linha + "\n"
            partes.append(parte_atual)
            for parte in partes:
                await ctx.send(parte)
        else:
            await ctx.send(mensagem)

    @tasks.loop(hours=24)
    async def verificar_aniversarios(self):
        await self.bot.wait_until_ready()
        hoje = datetime.now().strftime('%d/%m')
        aniversarios = carregar_aniversarios()
        canal = self.bot.get_channel(CANAL_ANIVERSARIOS)

        if canal:
            for user_id, data in aniversarios.items():
                if data == hoje:
                    try:
                        user = await self.bot.fetch_user(int(user_id))
                        await canal.send(f"🎉 Hoje é aniversário de {user.mention}! Parabéns! 🎂🎈")
                    except:
                        print(f"❌ Não consegui encontrar o usuário com ID {user_id}")

    @verificar_aniversarios.before_loop
    async def before_verificar(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Aniversario(bot))
