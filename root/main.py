import disnake
from disnake.ext import commands
import os

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(name='ping', description='Ping me!')
async def ping(ctx):
    embed = disnake.Embed(title='Pong!', description=f'Bot response time: {round(bot.latency * 1000)}ms')
    await ctx.send(embed=embed)

with open('token', 'r') as f:
    token = f.read()

bot.run(token)