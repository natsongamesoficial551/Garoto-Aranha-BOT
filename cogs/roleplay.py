import random
import asyncio
from discord.ext import commands

class Roleplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Sistema de HP para batalhas
        self.players_hp = {}
        self.max_hp = 100
        
        # Itens coletáveis
        self.player_inventories = {}
        
        # Lista de itens possíveis
        self.items = [
            "⚔️ Espada Lendária", "🛡️ Escudo de Aço", "💎 Gema Mágica", "🏹 Arco Élfico",
            "🧪 Poção de Cura", "📜 Pergaminho Antigo", "🗝️ Chave Dourada", "💰 Moedas de Ouro",
            "🔮 Orbe Misterioso", "⚡ Raio Engarrafado", "🌟 Estrela Cadente", "🍄 Cogumelo Mágico"
        ]

    def get_hp(self, user_id):
        """Obtém o HP atual do usuário"""
        if user_id not in self.players_hp:
            self.players_hp[user_id] = self.max_hp
        return self.players_hp[user_id]

    def damage_player(self, user_id, damage):
        """Aplica dano ao jogador"""
        current_hp = self.get_hp(user_id)
        new_hp = max(0, current_hp - damage)
        self.players_hp[user_id] = new_hp
        return new_hp

    def heal_player(self, user_id, heal_amount):
        """Cura o jogador"""
        current_hp = self.get_hp(user_id)
        new_hp = min(self.max_hp, current_hp + heal_amount)
        self.players_hp[user_id] = new_hp
        return new_hp

    def get_inventory(self, user_id):
        """Obtém o inventário do usuário"""
        if user_id not in self.player_inventories:
            self.player_inventories[user_id] = []
        return self.player_inventories[user_id]

    def add_item(self, user_id, item):
        """Adiciona item ao inventário"""
        inventory = self.get_inventory(user_id)
        inventory.append(item)
        return len(inventory)

    @commands.command()
    async def teia(self, ctx):
        """Lança teias como o Homem-Aranha"""
        respostas = [
            f"{ctx.author.mention} lançou uma teia e prendeu um vilão! 🕸️",
            f"{ctx.author.mention} balançou entre os prédios com sua teia! 🏙️",
            f"{ctx.author.mention} errou a teia e caiu no chão! 😅",
            f"{ctx.author.mention} criou uma rede de teias para proteger civis! 🕷️",
            f"{ctx.author.mention} usou a teia para desarmar um bandido! ⚡"
        ]
        await ctx.send(random.choice(respostas))

    @commands.command()
    async def atacar(self, ctx, *, alvo=None):
        """Ataca um inimigo ou outro jogador"""
        if not alvo:
            # Ataque a inimigo genérico
            ataques = [
                f"⚔️ {ctx.author.mention} desferiu um golpe poderoso no orc! Dano: {random.randint(15, 25)}",
                f"🏹 {ctx.author.mention} acertou uma flecha certeira no dragão! Dano: {random.randint(20, 30)}",
                f"⚡ {ctx.author.mention} lançou um raio mágico no goblin! Dano: {random.randint(10, 20)}",
                f"🔥 {ctx.author.mention} conjurou uma bola de fogo! Dano: {random.randint(18, 28)}",
                f"❄️ {ctx.author.mention} congelou o inimigo com magia de gelo! Dano: {random.randint(12, 22)}"
            ]
            await ctx.send(random.choice(ataques))
        else:
            # Ataque a outro usuário (se mencionado)
            if ctx.message.mentions:
                target = ctx.message.mentions[0]
                damage = random.randint(10, 25)
                new_hp = self.damage_player(target.id, damage)
                
                if new_hp <= 0:
                    await ctx.send(f"💀 {target.mention} foi derrotado por {ctx.author.mention}! Dano: {damage}")
                    self.players_hp[target.id] = self.max_hp  # Reset HP
                else:
                    await ctx.send(f"⚔️ {ctx.author.mention} atacou {target.mention}! Dano: {damage} | HP restante: {new_hp}")
            else:
                await ctx.send(f"⚔️ {ctx.author.mention} atacou {alvo} selvagemente! Dano: {random.randint(15, 25)}")

    @commands.command()
    async def defender(self, ctx):
        """Assume posição defensiva"""
        defesas = [
            f"🛡️ {ctx.author.mention} ergueu seu escudo e bloqueou o ataque!",
            f"⚡ {ctx.author.mention} esquivou com agilidade ninja!",
            f"🔮 {ctx.author.mention} criou uma barreira mágica protetora!",
            f"🏰 {ctx.author.mention} se escondeu atrás de uma rocha!",
            f"💨 {ctx.author.mention} desapareceu em uma nuvem de fumaça!"
        ]
        heal_amount = random.randint(5, 15)
        new_hp = self.heal_player(ctx.author.id, heal_amount)
        
        defesa = random.choice(defesas)
        await ctx.send(f"{defesa}\n💚 Recuperou {heal_amount} HP! HP atual: {new_hp}")

    @commands.command()
    async def explorar(self, ctx):
        """Explora uma área e pode encontrar itens"""
        locais = [
            "🏰 ruínas de um castelo antigo",
            "🌲 floresta sombria",
            "⛰️ caverna misteriosa",
            "🏖️ praia deserta",
            "🏜️ deserto árido",
            "🌋 vulcão adormecido",
            "❄️ tundra gelada",
            "🏛️ templo abandonado"
        ]
        
        local = random.choice(locais)
        chance = random.randint(1, 100)
        
        if chance <= 40:  # 40% chance de encontrar item
            item = random.choice(self.items)
            item_count = self.add_item(ctx.author.id, item)
            await ctx.send(f"🗺️ {ctx.author.mention} explorou {local} e encontrou: **{item}**!\n📦 Itens no inventário: {item_count}")
        elif chance <= 70:  # 30% chance de encontrar perigo
            damage = random.randint(5, 20)
            new_hp = self.damage_player(ctx.author.id, damage)
            if new_hp <= 0:
                await ctx.send(f"💀 {ctx.author.mention} explorou {local} mas foi derrotado por um monstro! Dano: {damage}")
                self.players_hp[ctx.author.id] = self.max_hp
            else:
                await ctx.send(f"⚠️ {ctx.author.mention} explorou {local} mas encontrou perigo! Dano: {damage} | HP: {new_hp}")
        else:  # 30% chance de não encontrar nada
            await ctx.send(f"🚶‍♂️ {ctx.author.mention} explorou {local} mas não encontrou nada interessante...")

    @commands.command()
    async def inventario(self, ctx):
        """Mostra o inventário do jogador"""
        inventory = self.get_inventory(ctx.author.id)
        hp = self.get_hp(ctx.author.id)
        
        if not inventory:
            await ctx.send(f"📦 {ctx.author.mention}, seu inventário está vazio!\n❤️ HP: {hp}/{self.max_hp}")
        else:
            items_text = "\n".join([f"• {item}" for item in inventory])
            await ctx.send(f"📦 **Inventário de {ctx.author.display_name}:**\n{items_text}\n\n❤️ HP: {hp}/{self.max_hp}")

    @commands.command()
    async def curar(self, ctx):
        """Usa uma poção de cura se disponível"""
        inventory = self.get_inventory(ctx.author.id)
        pocao_encontrada = False
        
        for i, item in enumerate(inventory):
            if "Poção" in item:
                heal_amount = random.randint(20, 40)
                new_hp = self.heal_player(ctx.author.id, heal_amount)
                inventory.pop(i)  # Remove a poção do inventário
                pocao_encontrada = True
                await ctx.send(f"🧪 {ctx.author.mention} usou uma {item} e recuperou {heal_amount} HP!\n❤️ HP atual: {new_hp}/{self.max_hp}")
                break
        
        if not pocao_encontrada:
            await ctx.send(f"❌ {ctx.author.mention}, você não possui poções de cura no inventário!")

    @commands.command()
    async def voar(self, ctx):
        """Voa pelos céus"""
        voos = [
            f"🦅 {ctx.author.mention} alçou voo majestosamente pelos céus!",
            f"✈️ {ctx.author.mention} voou sobre as nuvens como um super-herói!",
            f"🚁 {ctx.author.mention} fez manobras aéreas incríveis!",
            f"🛸 {ctx.author.mention} voou tão rápido que quebrou a barreira do som!",
            f"🌪️ {ctx.author.mention} criou um tornado com sua velocidade de voo!"
        ]
        await ctx.send(random.choice(voos))

    @commands.command()
    async def magica(self, ctx, *, tipo=None):
        """Lança diferentes tipos de magia"""
        if not tipo:
            magias = [
                f"✨ {ctx.author.mention} lançou uma magia misteriosa que brilhou intensamente!",
                f"🔮 {ctx.author.mention} conjurou um feitiço poderoso!",
                f"⚡ {ctx.author.mention} invocou raios do céu!",
                f"🔥 {ctx.author.mention} criou uma tempestade de fogo!",
                f"❄️ {ctx.author.mention} congelou tudo ao redor!"
            ]
        else:
            if "fogo" in tipo.lower():
                magias = [f"🔥 {ctx.author.mention} lançou uma bola de fogo devastadora!"]
            elif "gelo" in tipo.lower():
                magias = [f"❄️ {ctx.author.mention} criou uma nevasca congelante!"]
            elif "raio" in tipo.lower():
                magias = [f"⚡ {ctx.author.mention} invocou raios poderosos!"]
            elif "cura" in tipo.lower():
                heal_amount = random.randint(15, 30)
                new_hp = self.heal_player(ctx.author.id, heal_amount)
                await ctx.send(f"💚 {ctx.author.mention} lançou magia de cura e recuperou {heal_amount} HP!\n❤️ HP atual: {new_hp}/{self.max_hp}")
                return
            else:
                magias = [f"✨ {ctx.author.mention} lançou uma magia de {tipo}!"]
        
        await ctx.send(random.choice(magias))

    @commands.command()
    async def transformar(self, ctx, *, forma=None):
        """Se transforma em diferentes formas"""
        if not forma:
            formas = [
                f"🐺 {ctx.author.mention} se transformou em um lobo feroz!",
                f"🦅 {ctx.author.mention} virou uma águia majestosa!",
                f"🐉 {ctx.author.mention} se tornou um dragão poderoso!",
                f"🦈 {ctx.author.mention} virou um tubarão selvagem!",
                f"🐅 {ctx.author.mention} se transformou em um tigre feroz!"
            ]
        else:
            formas = [f"✨ {ctx.author.mention} se transformou em {forma}!"]
        
        await ctx.send(random.choice(formas))

    @commands.command()
    async def dancar(self, ctx):
        """Dança de forma épica"""
        dancas = [
            f"💃 {ctx.author.mention} começou a dançar e todos pararam para assistir!",
            f"🕺 {ctx.author.mention} fez uma dança tão incrível que ganhou aplausos!",
            f"🎭 {ctx.author.mention} dançou como se ninguém estivesse olhando!",
            f"🌟 {ctx.author.mention} brilhou na pista de dança!",
            f"🎪 {ctx.author.mention} fez uma apresentação circense incrível!"
        ]
        await ctx.send(random.choice(dancas))

    @commands.command()
    async def status(self, ctx):
        """Mostra o status completo do jogador"""
        hp = self.get_hp(ctx.author.id)
        inventory = self.get_inventory(ctx.author.id)
        item_count = len(inventory)
        
        # Determina o nível baseado nos itens
        if item_count >= 15:
            nivel = "🏆 Lendário"
        elif item_count >= 10:
            nivel = "⭐ Heroico"
        elif item_count >= 5:
            nivel = "🛡️ Aventureiro"
        else:
            nivel = "🌱 Novato"
        
        # Calcula barra de HP
        hp_percentage = (hp / self.max_hp) * 10
        hp_bar = "█" * int(hp_percentage) + "░" * (10 - int(hp_percentage))
        
        status_msg = f"""
**📊 STATUS DE {ctx.author.display_name.upper()}**

❤️ **HP:** {hp}/{self.max_hp}
`{hp_bar}`

🎯 **Nível:** {nivel}
📦 **Itens:** {item_count}
🏅 **Rank:** #{random.randint(1, 100)}

*Use !inventario para ver seus itens*
        """
        await ctx.send(status_msg)

    @commands.command()
    async def desafiar(self, ctx, *, oponente=None):
        """Desafia outro jogador para uma batalha épica"""
        if not oponente or not ctx.message.mentions:
            await ctx.send("❌ Você precisa mencionar alguém para desafiar!\nExemplo: `!desafiar @usuario`")
            return
        
        target = ctx.message.mentions[0]
        if target.id == ctx.author.id:
            await ctx.send("❌ Você não pode desafiar a si mesmo!")
            return
        
        # Batalha automática
        player1_damage = random.randint(20, 40)
        player2_damage = random.randint(20, 40)
        
        await ctx.send(f"🥊 **BATALHA ÉPICA INICIADA!**\n{ctx.author.mention} vs {target.mention}")
        await asyncio.sleep(2)
        
        await ctx.send(f"⚔️ {ctx.author.mention} atacou com força {player1_damage}!")
        await asyncio.sleep(1)
        
        await ctx.send(f"🛡️ {target.mention} revidou com poder {player2_damage}!")
        await asyncio.sleep(1)
        
        if player1_damage > player2_damage:
            winner = ctx.author
            loser = target
        elif player2_damage > player1_damage:
            winner = target
            loser = ctx.author
        else:
            await ctx.send("🤝 **EMPATE ÉPICO!** Ambos são guerreiros dignos!")
            return
        
        # Adiciona item ao vencedor
        prize = random.choice(self.items)
        self.add_item(winner.id, prize)
        
        await ctx.send(f"🏆 **{winner.mention} VENCEU A BATALHA!**\n🎁 Ganhou: {prize}")

    @commands.command()
    async def roleplay_help(self, ctx):
        """Mostra todos os comandos de roleplay"""
        help_text = """
**🎭 COMANDOS DE ROLEPLAY 🎭**

⚔️ **COMBATE:**
• `!atacar [alvo]` - Ataca inimigos ou jogadores
• `!defender` - Defende e recupera HP
• `!desafiar @usuario` - Desafia outro jogador

🔮 **AÇÕES MÁGICAS:**
• `!teia` - Lança teias como Homem-Aranha
• `!magica [tipo]` - Lança magias (fogo, gelo, raio, cura)
• `!voar` - Voa pelos céus
• `!transformar [forma]` - Se transforma

🗺️ **EXPLORAÇÃO:**
• `!explorar` - Explora áreas e encontra itens
• `!inventario` - Mostra seus itens
• `!curar` - Usa poção de cura
• `!status` - Mostra status completo

🎪 **DIVERSÃO:**
• `!dancar` - Dança de forma épica

*Divirta-se explorando e batalhando! ⚔️*
        """
        await ctx.send(help_text)

async def setup(bot):
    await bot.add_cog(Roleplay(bot))