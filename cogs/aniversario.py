import discord
from discord.ext import commands, tasks
import json
from datetime import datetime

ID_CANAL_PARABENS = 1382522505603842110  # Mude para o ID do canal certo

def carregar_aniversarios():
    try:
        with open('aniversarios.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_aniversarios(aniversarios):
    with open('aniversarios.json', 'w') as f:
        json.dump(aniversarios, f, indent=4)

class Aniversario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aniversarios = carregar_aniversarios()
        self.checar_aniversarios.start()

    @commands.command()
    async def setaniversario(self, ctx, data):
        """
        Salva o aniversário do usuário no formato DD-MM (Ex: 20-06)
        """
        try:
            datetime.strptime(data, '%d-%m')
            self.aniversarios[str(ctx.author.id)] = data
            salvar_aniversarios(self.aniversarios)
            await ctx.send(f'🎉 {ctx.author.mention}, seu aniversário foi salvo como **{data}**!')
        except ValueError:
            await ctx.send('❌ Formato inválido! Use o formato **DD-MM**, exemplo: `!setaniversario 20-06`')

    @tasks.loop(hours=24)
    async def checar_aniversarios(self):
        hoje = datetime.now().strftime('%d-%m')
        canal = self.bot.get_channel(ID_CANAL_PARABENS)
        if not canal:
            print(f"❌ Canal com ID {ID_CANAL_PARABENS} não encontrado!")
            return

        for user_id, data in self.aniversarios.items():
            if data == hoje:
                user = await self.bot.fetch_user(int(user_id))
                if user:
                    await canal.send(f'🎂 Feliz aniversário, {user.mention}! 🎉🎈')
                    print(f'Parabéns enviados para {user.name}')

    @checar_aniversarios.before_loop
    async def before_checar(self):
        await self.bot.wait_until_ready()
        print("🔄 Sistema de aniversário iniciado...")

async def setup(bot):
    await bot.add_cog(Aniversario(bot))
