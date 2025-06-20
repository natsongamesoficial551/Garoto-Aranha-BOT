from discord.ext import commands
import discord
import json
import os

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = 'xp.json'
        self.load_xp_data()

    def load_xp_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.xp_data = json.load(f)
        else:
            self.xp_data = {}

    def save_xp_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.xp_data, f, ensure_ascii=False, indent=4)

    def add_xp(self, user_id, amount):
        user_id = str(user_id)
        if user_id not in self.xp_data:
            self.xp_data[user_id] = {"xp": 0, "level": 1}
        
        self.xp_data[user_id]["xp"] += amount
        xp = self.xp_data[user_id]["xp"]
        level = self.xp_data[user_id]["level"]

        next_level_xp = level * 100

        # Level Up
        if xp >= next_level_xp:
            self.xp_data[user_id]["level"] += 1
            self.xp_data[user_id]["xp"] = xp - next_level_xp
            self.save_xp_data()
            return True, self.xp_data[user_id]["level"]
        else:
            self.save_xp_data()
            return False, level

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Ganha 10 XP por mensagem
        level_up, new_level = self.add_xp(message.author.id, 10)

        if level_up:
            embed = discord.Embed(
                title="🎉 Level Up!",
                description=f"{message.author.mention}, você subiu para o **Level {new_level}!** 🚀",
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)

    @commands.command(name="meuxp", aliases=["mylevel"])
    async def meuxp(self, ctx):
        """Mostra o seu XP e Level"""
        user_id = str(ctx.author.id)
        data = self.xp_data.get(user_id, {"xp": 0, "level": 1})

        embed = discord.Embed(
            title=f"📊 XP de {ctx.author.display_name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Level", value=data["level"])
        embed.add_field(name="XP Atual", value=data["xp"])

        await ctx.send(embed=embed)

    @commands.command(name="topxp", aliases=["xpleaderboard", "rankingxp"])
    async def topxp(self, ctx):
        """Mostra o Top XP (Ranking)"""
        if not self.xp_data:
            await ctx.send("❌ Não há dados de XP ainda!")
            return

        sorted_users = sorted(
            self.xp_data.items(),
            key=lambda x: (x[1]["level"], x[1]["xp"]),
            reverse=True
        )

        embed = discord.Embed(
            title="🏆 Ranking de XP",
            color=discord.Color.gold()
        )

        medals = ["🥇", "🥈", "🥉"]

        for idx, (user_id, data) in enumerate(sorted_users[:10]):
            user = self.bot.get_user(int(user_id))
            if not user:
                continue
            medal = medals[idx] if idx < 3 else f"{idx+1}."
            embed.add_field(
                name=f"{medal} {user.display_name}",
                value=f"Level {data['level']} | XP: {data['xp']}",
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(XP(bot))
    print("✅ Cog XP carregado com sucesso!")
