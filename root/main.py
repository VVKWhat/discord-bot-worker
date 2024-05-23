import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
import datetime
import json
import os
import events.sqlite as sqlite
 

import importlib

def import_all_modules_from_directory(directory):
    # Получаем абсолютный путь к директории
    directory_path = os.path.abspath(directory)
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Убираем ".py" из имени файла
            module_path = directory.replace(os.path.sep, '.') + '.' + module_name
            importlib.import_module(module_path)


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
# Импортируем все модули из команд
import_all_modules_from_directory('commands/moderation')
import_all_modules_from_directory('commands/utilities')
import_all_modules_from_directory('events')

# Ваш основной код
if __name__ == "__main__":
    print("Все модули импортированы")
# Старт бота
@bot.event
async def on_ready():
    await sqlite.create_database()
    print(f'\nБот {bot.user.name} успешно запущен.\n')
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