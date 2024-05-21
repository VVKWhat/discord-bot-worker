import os
import nextcord
from nextcord.ext import commands

current_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(current_dir, "token")

with open(token_file, "r") as f:
    TOKEN = f.read().strip()

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print()
    print(f'Бот {bot.user.name} успешно запущен.')
    print()

@bot.slash_command()
async def ping(ctx):
    latency = bot.latency * 1000
    embed = nextcord.Embed(
        title="Pong!",
        description=f"Задержка: {latency:.2f} мс",
        color=0x2b2d31
    )
    await ctx.send(embed=embed)

bot.run(TOKEN)