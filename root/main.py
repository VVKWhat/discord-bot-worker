import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
import datetime
import json
import os
import events.sqlite as sqlite
 

import importlib

def get_modules_from_directory(directory):
    # Получаем абсолютный путь к директории
    directory_path = os.path.abspath(directory)
    print(f'modules directory: {directory_path}')
    for filename in os.listdir(directory_path):
        if filename.endswith('.py') and filename != '__init__.py':
            module_path = os.path.join(directory_path, filename)
            with open(module_path, "r", encoding="utf-8") as file:
                code = file.read()
                compiled_code = compile(code, module_path, 'exec')
                exec(compiled_code, globals())


current_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(current_dir, "token")
# import locale
# locale.setlocale(locale.LC_ALL, ('C', 'UTF-8')) # Вместо C установить ru_RU, при этом убедиться что есть языковой пакет ru_RU.UTF-8 через команду locale -a
# print(locale.getlocale())   
with open(token_file, "r") as f:
    TOKEN = f.read().strip()

intents = nextcord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

notification_channel_id = 1242246527712235582
gateway_channel_id = 1242216834237992990
guild_id = 1242213449405304864
# Импортируем все модули из команд
get_modules_from_directory('commands/moderation')
get_modules_from_directory('commands/utilities')
get_modules_from_directory('events')

print("Все модули импортированы")

# Старт бота
@bot.event
async def on_ready():
    await sqlite.create_database()
    print(f'\nБот {bot.user.name} успешно запущен.\n')

    for guild in bot.guilds:
        if guild.id != guild_id:
            await leave_guild(guild)
        else:
            for member in guild.members:
                await sqlite.add_user_to_database(member.id, member.bot)

async def leave_guild(guild: nextcord.Guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("[Бот доступен только на одном сервере.](https://discord.gg/ffTPqp8GjT)")
            break
    await guild.leave()

@bot.event
async def on_guild_join(guild: nextcord.Guild):
    if guild.id != guild_id:
        await leave_guild(guild)

# Пинг бота
@bot.slash_command()
async def ping(ctx):
    latency = bot.latency * 1000
    embed = nextcord.Embed(
        title="Pong!",
        description=f"Задержка: {latency:.2f} мс",
        color=0xA7A7D7
    )
    await ctx.send(embed=embed)
bot.run(TOKEN)