import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime

CAMINHO_JSON = 'C:\Users\Admin\GarotoAranhaBot\cogs\aniversarios.json'
CANAL_ANIVERSARIOS = 1382522505603842110  # ✅ Troque pelo ID do canal onde as mensagens vão ser enviadas

def carregar_aniversarios():
    if os.path.exists(CAMINHO_JSON):
        with open(CAMINHO_JSON, 'r') as f:
            return json.load(f)
    else:
        return {}

def salvar_aniversarios(aniversarios):
    with open(CAMINHO_JSON, 'w') as f:
        json.dump(aniversarios, f, indent=4)

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
