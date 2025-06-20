from discord.ext import commands
import discord
import json
import os
import random
import asyncio
from datetime import datetime, timedelta

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'economia.json'
        self.daily_cooldown = {}
        self.work_cooldown = {}
        self.crime_cooldown = {}
        self.load_data()
    
    def load_data(self):
        """Carrega os dados de economia do arquivo JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.economy_data = json.load(f)
            except:
                self.economy_data = {}
        else:
            self.economy_data = {}
    
    def save_data(self):
        """Salva os dados de economia no arquivo JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.economy_data, f, ensure_ascii=False, indent=2)
    
    def get_user_data(self, user_id):
        """Pega os dados do usuário ou cria novos"""
        user_id = str(user_id)
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {
                'coins': 100,  # Coins iniciais
                'bank': 0,
                'xp': 0,
                'level': 1,
                'daily_streak': 0,
                'last_daily': None,
                'inventory': {},
                'achievements': []
            }
            self.save_data()
        return self.economy_data[user_id]
    
    def add_coins(self, user_id, amount):
        """Adiciona coins ao usuário"""
        data = self.get_user_data(user_id)
        data['coins'] += amount
        self.save_data()
        return data['coins']
    
    def remove_coins(self, user_id, amount):
        """Remove coins do usuário"""
        data = self.get_user_data(user_id)
        if data['coins'] >= amount:
            data['coins'] -= amount
            self.save_data()
            return True
        return False
    
    def add_xp(self, user_id, xp_amount):
        """Adiciona XP e verifica level up"""
        data = self.get_user_data(user_id)
        data['xp'] += xp_amount
        
        # Calcular novo level
        new_level = int((data['xp'] / 100) ** 0.5) + 1
        
        if new_level > data['level']:
            data['level'] = new_level
            bonus_coins = new_level * 50
            data['coins'] += bonus_coins
            self.save_data()
            return new_level, bonus_coins
        
        self.save_data()
        return None, 0
    
    @commands.command(aliases=['saldo', 'bal'])
    async def balance(self, ctx, user: discord.Member = None):
        """Mostra o saldo de coins do usuário"""
        if user is None:
            user = ctx.author
        
        data = self.get_user_data(user.id)
        total = data['coins'] + data['bank']
        
        embed = discord.Embed(
            title=f"💰 Economia - {user.display_name}",
            color=discord.Color.gold()
        )
        embed.add_field(name="🪙 Carteira", value=f"{data['coins']:,} coins", inline=True)
        embed.add_field(name="🏦 Banco", value=f"{data['bank']:,} coins", inline=True)
        embed.add_field(name="💎 Total", value=f"{total:,} coins", inline=True)
        embed.add_field(name="📊 Level", value=f"{data['level']}", inline=True)
        embed.add_field(name="⭐ XP", value=f"{data['xp']:,}", inline=True)
        embed.add_field(name="🔥 Streak Diário", value=f"{data['daily_streak']} dias", inline=True)
        
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def daily(self, ctx):
        """Recompensa diária"""
        user_id = ctx.author.id
        
        # Verificar cooldown
        if user_id in self.daily_cooldown:
            time_left = self.daily_cooldown[user_id] - datetime.now()
            if time_left.total_seconds() > 0:
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                await ctx.send(f"⏰ Você já coletou sua recompensa diária! Volte em {hours}h {minutes}m")
                return
        
        data = self.get_user_data(user_id)
        
        # Verificar streak
        now = datetime.now()
        last_daily = datetime.fromisoformat(data['last_daily']) if data['last_daily'] else None
        
        if last_daily and (now - last_daily).days == 1:
            data['daily_streak'] += 1
        elif last_daily and (now - last_daily).days > 1:
            data['daily_streak'] = 1
        else:
            data['daily_streak'] = 1
        
        # Calcular recompensa baseada no streak
        base_reward = 500
        streak_bonus = min(data['daily_streak'] * 50, 1000)
        level_bonus = data['level'] * 25
        total_reward = base_reward + streak_bonus + level_bonus
        
        self.add_coins(user_id, total_reward)
        self.add_xp(user_id, 25)
        data['last_daily'] = now.isoformat()
        
        # Definir próximo cooldown (24 horas)
        self.daily_cooldown[user_id] = now + timedelta(hours=24)
        
        embed = discord.Embed(
            title="🎁 Recompensa Diária Coletada!",
            description=f"Você ganhou **{total_reward:,} coins**!",
            color=discord.Color.green()
        )
        embed.add_field(name="💰 Recompensa Base", value=f"{base_reward:,} coins", inline=True)
        embed.add_field(name="🔥 Bônus Streak", value=f"{streak_bonus:,} coins", inline=True)
        embed.add_field(name="📊 Bônus Level", value=f"{level_bonus:,} coins", inline=True)
        embed.add_field(name="🔥 Streak Atual", value=f"{data['daily_streak']} dias", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['trabalhar'])
    async def work(self, ctx):
        """Trabalhar para ganhar coins"""
        user_id = ctx.author.id
        
        # Verificar cooldown (1 hora)
        if user_id in self.work_cooldown:
            time_left = self.work_cooldown[user_id] - datetime.now()
            if time_left.total_seconds() > 0:
                minutes = int(time_left.total_seconds() // 60)
                await ctx.send(f"⏰ Você está cansado! Descanse por mais {minutes} minutos.")
                return
        
        jobs = [
            ("🕷️ Combateu criminosos como Garoto-Aranha", 200, 300),
            ("📰 Trabalhou como fotógrafo", 150, 250),
            ("🧪 Ajudou no laboratório", 180, 280),
            ("🏫 Deu aulas de ciências", 160, 240),
            ("🦸‍♂️ Salvou gatos de árvores", 120, 200),
            ("📸 Vendeu fotos do Garoto-Aranha", 250, 350),
            ("🔬 Fez pesquisa científica", 300, 400)
        ]
        
        job_desc, min_reward, max_reward = random.choice(jobs)
        reward = random.randint(min_reward, max_reward)
        
        data = self.get_user_data(user_id)
        level_bonus = data['level'] * 10
        total_reward = reward + level_bonus
        
        self.add_coins(user_id, total_reward)
        level_up, bonus_coins = self.add_xp(user_id, 15)
        
        # Definir cooldown (1 hora)
        self.work_cooldown[user_id] = datetime.now() + timedelta(hours=1)
        
        embed = discord.Embed(
            title="💼 Trabalho Concluído!",
            description=job_desc,
            color=discord.Color.blue()
        )
        embed.add_field(name="💰 Ganhou", value=f"{total_reward:,} coins", inline=True)
        embed.add_field(name="⭐ XP", value="+15 XP", inline=True)
        
        if level_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {level_up}! +{bonus_coins:,} coins bônus!", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['crime', 'roubar'])
    async def rob(self, ctx):
        """Tentar um crime (arriscado)"""
        user_id = ctx.author.id
        
        # Verificar cooldown (2 horas)
        if user_id in self.crime_cooldown:
            time_left = self.crime_cooldown[user_id] - datetime.now()
            if time_left.total_seconds() > 0:
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                await ctx.send(f"⏰ A polícia ainda está te procurando! Espere {hours}h {minutes}m")
                return
        
        data = self.get_user_data(user_id)
        
        if data['coins'] < 100:
            await ctx.send("❌ Você precisa de pelo menos 100 coins para tentar um crime!")
            return
        
        # 60% chance de sucesso
        success = random.random() < 0.6
        
        if success:
            reward = random.randint(300, 800)
            self.add_coins(user_id, reward)
            self.add_xp(user_id, 10)
            
            crimes = [
                f"🦹‍♂️ Você derrotou um vilão e encontrou {reward:,} coins!",
                f"💎 Você encontrou um tesouro escondido: {reward:,} coins!",
                f"🕸️ Você impediu um roubo e ganhou recompensa: {reward:,} coins!",
                f"🏆 Você completou uma missão secreta: {reward:,} coins!"
            ]
            
            embed = discord.Embed(
                title="✅ Crime Bem Sucedido!",
                description=random.choice(crimes),
                color=discord.Color.green()
            )
        else:
            penalty = random.randint(100, 300)
            penalty = min(penalty, data['coins'])  # Não pode ficar negativo
            self.remove_coins(user_id, penalty)
            
            fails = [
                f"🚔 A polícia te pegou! Multa de {penalty:,} coins!",
                f"😵 Você foi nocauteado por um vilão! Perdeu {penalty:,} coins!",
                f"🕷️ O Garoto-Aranha te impediu! Perdeu {penalty:,} coins!",
                f"⚡ Você tropeçou tentando fugir! Perdeu {penalty:,} coins!"
            ]
            
            embed = discord.Embed(
                title="❌ Crime Falhou!",
                description=random.choice(fails),
                color=discord.Color.red()
            )
        
        # Definir cooldown (2 horas)
        self.crime_cooldown[user_id] = datetime.now() + timedelta(hours=2)
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['dep', 'depositar'])
    async def deposit(self, ctx, amount=None):
        """Depositar coins no banco"""
        if amount is None:
            await ctx.send("❌ Use: `!deposit <quantidade>` ou `!deposit all`")
            return
        
        data = self.get_user_data(ctx.author.id)
        
        if amount.lower() == 'all':
            amount = data['coins']
        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.send("❌ Quantidade inválida!")
                return
        
        if amount <= 0:
            await ctx.send("❌ Quantidade deve ser maior que 0!")
            return
        
        if data['coins'] < amount:
            await ctx.send(f"❌ Você só tem {data['coins']:,} coins na carteira!")
            return
        
        data['coins'] -= amount
        data['bank'] += amount
        self.save_data()
        
        embed = discord.Embed(
            title="🏦 Depósito Realizado",
            description=f"Você depositou **{amount:,} coins** no banco!",
            color=discord.Color.green()
        )
        embed.add_field(name="💰 Carteira", value=f"{data['coins']:,} coins", inline=True)
        embed.add_field(name="🏦 Banco", value=f"{data['bank']:,} coins", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['with', 'sacar'])
    async def withdraw(self, ctx, amount=None):
        """Sacar coins do banco"""
        if amount is None:
            await ctx.send("❌ Use: `!withdraw <quantidade>` ou `!withdraw all`")
            return
        
        data = self.get_user_data(ctx.author.id)
        
        if amount.lower() == 'all':
            amount = data['bank']
        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.send("❌ Quantidade inválida!")
                return
        
        if amount <= 0:
            await ctx.send("❌ Quantidade deve ser maior que 0!")
            return
        
        if data['bank'] < amount:
            await ctx.send(f"❌ Você só tem {data['bank']:,} coins no banco!")
            return
        
        data['bank'] -= amount
        data['coins'] += amount
        self.save_data()
        
        embed = discord.Embed(
            title="🏦 Saque Realizado",
            description=f"Você sacou **{amount:,} coins** do banco!",
            color=discord.Color.blue()
        )
        embed.add_field(name="💰 Carteira", value=f"{data['coins']:,} coins", inline=True)
        embed.add_field(name="🏦 Banco", value=f"{data['bank']:,} coins", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['give', 'pay'])
    async def transfer(self, ctx, user: discord.Member, amount: int):
        """Transferir coins para outro usuário"""
        if user == ctx.author:
            await ctx.send("❌ Você não pode transferir coins para si mesmo!")
            return
        
        if user.bot:
            await ctx.send("❌ Você não pode transferir coins para bots!")
            return
        
        if amount <= 0:
            await ctx.send("❌ Quantidade deve ser maior que 0!")
            return
        
        sender_data = self.get_user_data(ctx.author.id)
        
        if sender_data['coins'] < amount:
            await ctx.send(f"❌ Você só tem {sender_data['coins']:,} coins!")
            return
        
        # Taxa de transferência (5%)
        tax = int(amount * 0.05)
        final_amount = amount - tax
        
        self.remove_coins(ctx.author.id, amount)
        self.add_coins(user.id, final_amount)
        
        embed = discord.Embed(
            title="💸 Transferência Realizada",
            description=f"{ctx.author.mention} transferiu **{final_amount:,} coins** para {user.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="💰 Valor", value=f"{amount:,} coins", inline=True)
        embed.add_field(name="💳 Taxa (5%)", value=f"{tax:,} coins", inline=True)
        embed.add_field(name="✅ Recebido", value=f"{final_amount:,} coins", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['rank', 'top'])
    async def leaderboard(self, ctx):
        """Ranking dos usuários mais ricos"""
        if not self.economy_data:
            await ctx.send("❌ Nenhum dado de economia encontrado!")
            return
        
        # Ordenar usuários por total de coins (carteira + banco)
        sorted_users = []
        for user_id, data in self.economy_data.items():
            try:
                user = self.bot.get_user(int(user_id))
                if user and not user.bot:
                    total = data['coins'] + data['bank']
                    sorted_users.append((user, total, data['level']))
            except:
                continue
        
        sorted_users.sort(key=lambda x: x[1], reverse=True)
        
        embed = discord.Embed(
            title="🏆 Ranking de Economia",
            color=discord.Color.gold()
        )
        
        medals = ["🥇", "🥈", "🥉"]
        
        for i, (user, total, level) in enumerate(sorted_users[:10]):
            medal = medals[i] if i < 3 else f"{i+1}."
            embed.add_field(
                name=f"{medal} {user.display_name}",
                value=f"💰 {total:,} coins • 📊 Level {level}",
                inline=False
            )
        
        embed.set_footer(text=f"Total de usuários: {len(sorted_users)}")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def coinflip(self, ctx, bet: int, choice: str):
        """Apostar coins no cara ou coroa"""
        if bet <= 0:
            await ctx.send("❌ Aposta deve ser maior que 0!")
            return
        
        if choice.lower() not in ['cara', 'coroa', 'heads', 'tails']:
            await ctx.send("❌ Escolha 'cara' ou 'coroa'!")
            return
        
        data = self.get_user_data(ctx.author.id)
        
        if data['coins'] < bet:
            await ctx.send(f"❌ Você só tem {data['coins']:,} coins!")
            return
        
        # Normalizar escolha
        user_choice = 'cara' if choice.lower() in ['cara', 'heads'] else 'coroa'
        result = random.choice(['cara', 'coroa'])
        
        if user_choice == result:
            # Ganhou - dobra a aposta
            winnings = bet
            self.add_coins(ctx.author.id, winnings)
            self.add_xp(ctx.author.id, 5)
            
            embed = discord.Embed(
                title="🎉 Você Ganhou!",
                description=f"🪙 **{result.title()}**!\n\nVocê ganhou **{winnings:,} coins**!",
                color=discord.Color.green()
            )
        else:
            # Perdeu
            self.remove_coins(ctx.author.id, bet)
            
            embed = discord.Embed(
                title="😔 Você Perdeu!",
                description=f"🪙 **{result.title()}**!\n\nVocê perdeu **{bet:,} coins**!",
                color=discord.Color.red()
            )
        
        embed.add_field(name="Sua Escolha", value=user_choice.title(), inline=True)
        embed.add_field(name="Resultado", value=result.title(), inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def shop(self, ctx):
        """Loja de itens"""
        embed = discord.Embed(
            title="🛒 Loja do Garoto-Aranha",
            description="Use `!buy <item>` para comprar!",
            color=discord.Color.blue()
        )
        
        items = {
            "teia": {"name": "🕸️ Cartucho de Teia", "price": 500, "description": "Aumenta XP de trabalho"},
            "camera": {"name": "📷 Câmera Profissional", "price": 2000, "description": "Aumenta ganhos de fotografia"},
            "suit": {"name": "🦸‍♂️ Traje do Garoto-Aranha", "price": 10000, "description": "Aumenta todos os ganhos"},
            "web_shooter": {"name": "🎯 Lançador de Teia", "price": 5000, "description": "Reduz cooldown de trabalho"},
            "spider_sense": {"name": "🕷️ Sentido Aranha", "price": 8000, "description": "Aumenta chance de sucesso em crimes"}
        }
        
        for item_id, item in items.items():
            embed.add_field(
                name=f"{item['name']} - {item['price']:,} coins",
                value=item['description'],
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def buy(self, ctx, item_name: str):
        """Comprar item da loja"""
        items = {
            "teia": {"name": "🕸️ Cartucho de Teia", "price": 500},
            "camera": {"name": "📷 Câmera Profissional", "price": 2000},
            "suit": {"name": "🦸‍♂️ Traje do Garoto-Aranha", "price": 10000},
            "web_shooter": {"name": "🎯 Lançador de Teia", "price": 5000},
            "spider_sense": {"name": "🕷️ Sentido Aranha", "price": 8000}
        }
        
        item_name = item_name.lower()
        
        if item_name not in items:
            await ctx.send("❌ Item não encontrado! Use `!shop` para ver os itens disponíveis.")
            return
        
        item = items[item_name]
        data = self.get_user_data(ctx.author.id)
        
        if data['coins'] < item['price']:
            await ctx.send(f"❌ Você precisa de {item['price']:,} coins para comprar {item['name']}!")
            return
        
        # Verificar se já possui o item
        if item_name in data['inventory'] and data['inventory'][item_name] > 0:
            await ctx.send(f"❌ Você já possui {item['name']}!")
            return
        
        # Comprar item
        self.remove_coins(ctx.author.id, item['price'])
        
        if 'inventory' not in data:
            data['inventory'] = {}
        
        data['inventory'][item_name] = data['inventory'].get(item_name, 0) + 1
        self.save_data()
        
        embed = discord.Embed(
            title="✅ Compra Realizada!",
            description=f"Você comprou **{item['name']}** por **{item['price']:,} coins**!",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['inv', 'mochila'])
    async def inventory(self, ctx, user: discord.Member = None):
        """Mostra o inventário do usuário"""
        if user is None:
            user = ctx.author
        
        data = self.get_user_data(user.id)
        inventory = data.get('inventory', {})
        
        if not inventory or all(count == 0 for count in inventory.values()):
            await ctx.send(f"📦 {user.display_name} não possui itens no inventário!")
            return
        
        items_names = {
            "teia": "🕸️ Cartucho de Teia",
            "camera": "📷 Câmera Profissional", 
            "suit": "🦸‍♂️ Traje do Garoto-Aranha",
            "web_shooter": "🎯 Lançador de Teia",
            "spider_sense": "🕷️ Sentido Aranha"
        }
        
        embed = discord.Embed(
            title=f"📦 Inventário - {user.display_name}",
            color=discord.Color.purple()
        )
        
        for item_id, count in inventory.items():
            if count > 0:
                item_name = items_names.get(item_id, item_id.title())
                embed.add_field(name=item_name, value=f"Quantidade: {count}", inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economia(bot))
    print("✅ Cog Economia carregado com sucesso!")