import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
import datetime
import json
import os
import events.sqlite as sqlite
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

notification_channel_id = 1242246527712235582
gateway_channel_id = 1242216834237992990
guild_id = 1242213449405304864
guild: nextcord.Guild = bot.get_guild(guild_id)
# Импортируем все модули из команд
get_modules_from_directory('commands/moderation')
get_modules_from_directory('commands/utilities')
get_modules_from_directory('events')
scheduler = AsyncIOScheduler()
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
    
    scheduler.start()

async def hourly_task():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = await sqlite.cursor.execute("SELECT `user_id` FROM `bot_bans` WHERE datetime(`date`, '+' || `expired` || 'hours') <= ?", (now))
    expired_bans = await data.fetchall()
    channel = bot.get_channel(1242246527712235582)
    for ban in expired_bans:
        user_id = ban[0]
        if guild:
            user = await guild.fetch_member(user_id)
            if user:
                await sqlite.cursor.execute('DELETE FROM `bot_bans` WHERE `bot_bans`.`user_id` = ?',(user_id))
                embed1 = nextcord.Embed(
                    description=" \n**С вас было снято наказание.**",
                    color=0xA7A7D7,
                    url="https://i.ibb.co/26ySjnr/filler.png"
                )
                embed2 = nextcord.Embed(
                    description=f"### **Причина**\n⠀\n> \"Срок бана истёк\"\n⠀\н### **Модератор**\n⠀\н> <@1235625733431234681>",
                    color=0xA7A7D7,
                    url="https://i.ibb.co/26ySjnr/filler.png"
                )
                embed3 = nextcord.Embed(
                    description="",
                    color=0xA7A7D7
                )
                embed1.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
                embed2.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
                embed3.set_image(url="https://i.ibb.co/M7DtSqd/banner.png")
                await channel.send(embed=embed1)
                await channel.send(embed=embed2)
                await channel.send(embed=embed3)
                try:
                    await user.send(embed=embed1)
                    await user.send(embed=embed2)
                    await user.send(embed=embed3)
                except nextcord.Forbidden:
                    pass
                print(f"Разбан пользователя с ID: {user_id}")
    sqlite.sql.commit()
    data = sqlite.cursor.execute("SELECT `user_id` FROM `bot_mutes` WHERE datetime(`date`, '+' || `expired` || 'hours') <= ?", (now))
    expired_mutes = await data.fetchall()
    for mute in expired_mutes:
        user_id = mute[0]
        if guild:
            user = await guild.fetch_member(user_id)
            if user:
                await sqlite.cursor.execute('DELETE FROM `bot_mutes` WHERE `bot_mutes`.`user_id` = ?',(user_id))
                embed1 = nextcord.Embed(
                    description="⠀\n**С вас был снят мьют.**",
                    color=0xA7A7D7,
                    url="https://i.ibb.co/26ySjnr/filler.png"
                )
                embed2 = nextcord.Embed(
                    description=f"### **Причина**\n⠀\n> \"Срок мута истёк\"\n⠀\н### **Модератор**\n⠀\н> <@1235625733431234681>",
                    color=0xA7A7D7,
                    url="https://i.ibb.co/26ySjnr/filler.png"
                )
                embed3 = nextcord.Embed(
                    description="",
                    color=0xA7A7D7
                )
                embed1.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
                embed2.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
                embed3.set_image(url="https://i.ibb.co/M7DtSqd/banner.png")
                await channel.send(embed=embed1)
                await channel.send(embed=embed2)
                await channel.send(embed=embed3)
                try:
                    await user.send(embed=embed1)
                    await user.send(embed=embed2)
                    await user.send(embed=embed3)
                except nextcord.Forbidden:
                    pass
                print(f"Размьючен пользователя с ID: {user_id}")
    sqlite.sql.commit()
scheduler.add_job(hourly_task, 'interval', hours=1)


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