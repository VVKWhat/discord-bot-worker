import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
import datetime
import json
import os
import sqlite3

import sqlite3

# Подключение к базе данных
sql = sqlite3.connect("database.db")
cursor = sql.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bot_warns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expired_days INT,
    UNIQUE(user_id, reason)
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS bot_bans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expired TIMESTAMP,
    appilation BOOLEAN,
    UNIQUE(user_id, reason)
);
""")
sql.commit()


current_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(current_dir, "token")
import locale
#locale.setlocale(locale.LC_ALL, ('C', 'UTF-8')) # Вместо C установить ru_RU, при этом убедиться что есть языковой пакет ru_RU.UTF-8 через команду locale -a
#print(locale.getlocale())   
with open(token_file, "r") as f:
    TOKEN = f.read().strip()

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

notification_channel_id = 1242246527712235582
gateway_channel_id = 1242216834237992990

@bot.event
async def on_ready():
    print()
    print(f'Бот {bot.user.name} успешно запущен.')
    print()


@bot.event
async def on_member_join(member):
    print(f'новый участник! {member.display_name}')
    channel = nextcord.Interaction.get_channel(gateway_channel_id)
    if member.bot:
        return
    elif channel is not None:
        await channel.send(f'<@{member.id}>')
        embed_info = nextcord.Embed(
            description=f"⠀\n👋🏻⠀⠀**Приветствуем вас на нашем Discord сервере!**",
            color=0x2b2d31
        )
        embed_info.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed_info)
        embed_info = nextcord.Embed(
            description=f"⠀\n**Советуем ознакомиться с следующими каналами:**\n⠀\n> - <#1242213724262105190>\n> - <#1242221576611696811>\n> - <#1242229530861768856>\n⠀\n**Вас пригласил:**\n⠀\n> ПРИГЛАСИЛ: пока нету",
            color=0x2b2d31
        )
        embed_info.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed_info)
    else:
        print(f"Не удалось найти канал для отправки сообщения.")


@bot.event
async def on_member_remove(member):
    print(f'Участник покинул нас! {member.display_name}')
    channel = nextcord.Interaction.get_channel(gateway_channel_id)
    if member.bot:
        return
    elif channel is not None:
        await channel.send(f'<@{member.id}>')
        embed_info = nextcord.Embed(
            description=f"⠀\n👋🏻⠀⠀**До скорых встреч!**",
            color=0x2b2d31
        )
        embed_info.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed_info)
        embed = nextcord.Embed(
            description=f"⠀\n**Надеемся, что мы встретимся снова!**\n⠀\n**Пользователя пригласил:**\n⠀\n> ПРИГЛАСИЛ: пока нет",
            color=0x2b2d31
        )
        embed.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed)
    else:
        print(f"Не удалось найти канал для отправки сообщения.")


@bot.slash_command()
async def ping(ctx):
    latency = bot.latency * 1000
    embed = nextcord.Embed(
        title="Pong!",
        description=f"Задержка: {latency:.2f} мс",
        color=0x2b2d31
    )
    await ctx.send(embed=embed)


@bot.slash_command(description="Отправляет JSON в выбранный канал.")
@commands.has_any_role(1242265397735067698, 1242267372052545576)
async def send_json(ctx: nextcord.Interaction, attachment: nextcord.Attachment, channel: nextcord.TextChannel):
    await ctx.response.defer()

    if not attachment.filename.endswith('.json'):
        await ctx.followup.send("Пожалуйста, прикрепите JSON.")
        return

    try:
        file_content = await attachment.read()
        data = json.loads(file_content)
    except json.JSONDecodeError:
        await ctx.followup.send("Не удалось прочесть JSON.")
        return

    try:
        for item in data['embeds']:
            embed = nextcord.Embed.from_dict(item)
            await channel.send(embed=embed)
        await ctx.followup.send("Сообщение было отправлено.")
    except Exception as e:
        await ctx.followup.send(f"Ошибка: {str(e)}")

@send_json.error
async def send_json_error(ctx: nextcord.Interaction, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("У вас нет прав для использования этой команды.")
    else:
        await ctx.send(f"Произошла ошибка: {str(error)}")

@bot.slash_command(name="ban", description="Выдать бан пользователю")
async def ban(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    duration: int, 
    reason: str, 
    appeal: str = SlashOption(
        name="appeal",
        choices={
            "С апелляцией": "appeal", 
            "Без апелляции": "noappeal"
        },
        required=True
    )
):
    try:
        guild = ctx.guild
        if not guild:
            await ctx.response.send_message("Эта команда может быть использована только в сервере.")
            return

        ban_appeal = guild.get_role(1242234027742859294)
        ban_no_appeal = guild.get_role(1242232941422051358)
        if 1242232941422051358 in member.roles.id or 1242234027742859294 in member.roles.id:
            await ctx.response.send_message("Данный пользователь уже в бане.")
        if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
            await ctx.response.send_message("У вас нет прав для использования этой команды.")
            return
        if ctx.user.mention == member.mention:
            print(f"{ctx.user.display_name} долбоёб - пытался себя забанить =-=")
            await ctx.response.send_message("Вы не можете забанить себя! Всё с головой в порядке?")
            return
        if appeal == "appeal":
            await member.add_roles(ban_appeal)
            appeal_text = '\n\n- Дополнительно:\n> У вас есть возможность подачи апелляции!\n> В канале <#1242228411280265388>'
        else:
            await member.add_roles(ban_no_appeal)
            appeal_text = ''

        unban_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=duration)

        await ctx.response.send_message(f"{member.mention} был забанен на {duration}ч. по причине: \"{reason}\".")

        channel = bot.get_channel(1242246527712235582)
        if not channel:
            await ctx.response.send_message("Не удалось найти канал для отправки сообщения.")
            return

        await channel.send(f'<@{member.id}>')

        embed_info = nextcord.Embed(
            description="⠀\n‼️⠀⠀**Вы были забанены за нарушение правил сервера!**\n⠀\n❓⠀⠀Канал с частыми вопросами: <#1242236181505376366>",
            color=0x2b2d31
        )
        embed_info.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed_info)

        embed = nextcord.Embed(
            description=f"⠀\n- Срок вашего наказания:\n> {duration}ч.\n⠀\n- Причина выдачи наказания:\n> {reason}\n⠀\n- Наказание выдал(-а):\n> <@{ctx.user.id}>\n⠀\n- Дата окончания наказания:\n> {unban_time.strftime('%d %B %Y, %H:%M')} (UTC){appeal_text}",
            color=0xff0000
        )
        embed.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed)
        await member.send(embed=embed_info)
        await member.send(embed=embed)
    except Exception as e:
        await ctx.response.send_message(f"Произошла ошибка: {str(e)}")

@bot.slash_command(name="unban", description="Убрать существующий бан пользователю")
async def unban(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    reason: str, 
):
    try:
        guild = ctx.guild
        if not guild:
            await ctx.response.send_message("Эта команда может быть использована только в сервере.")
            return

        ban_appeal = guild.get_role(1242234027742859294)
        ban_no_appeal = guild.get_role(1242232941422051358)

        if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
            await ctx.response.send_message("У вас нет прав для использования этой команды.")
            return
        if ctx.user.mention == member.mention:
            print(f"{ctx.user.display_name} долбоёб - пытался себя разбанить =-=")
            await ctx.response.send_message("Вы не имеете полномочий для того, чтобы разбанить самого себя")
            return
        if member.get_role(1242234027742859294) is not None and member.get_role(1242232941422051358) is not None:
            await ctx.response.send_message("Данный пользователь не забанен!")
            return
        if ban_appeal in member.roles or ban_no_appeal in member.roles:
            if ban_appeal in member.roles:
                await member.remove_roles(ban_appeal)
                await ctx.response.send_message(f'Пользователь {member.mention} был разбанен администратором {ctx.user.mention}\nПричина снятия бана: **{reason}**\n\nУ данного пользователя был бан с аппеляцией.')
                await member.send(f'Вы были разбанены администратором {ctx.user.mention}\n**Начинайте наслаждаться моментом!**')
                
            if ban_no_appeal in member.roles:
                await member.remove_roles(ban_no_appeal)
                await ctx.response.send_message(f'Пользователь {member.mention} был разбанен администратором {ctx.user.mention}\nПричина снятия бана: **{reason}**\n\nУ данного пользователя был бан без возможности аппеляции.')
                await member.send(f'Вы были разбанены администратором {ctx.user.mention}\n**Начинайте наслаждаться моментом!**')
        else:
            await ctx.response.send_message("Данный пользователь не забанен!")
            
        channel = bot.get_channel(1242246527712235582)
        if not channel:
            await ctx.response.send_message("Не удалось найти канал для отправки сообщения.")
            return
        embed = nextcord.Embed(
            description=f"⠀\n-Разбанен пользователь:\n> {member.mention}\n⠀\n- Причина:\n> {reason}\n⠀\n- Наказание снял(-а):\n> <@{ctx.user.id}>\n",
            color=0xff0000
        )
        await channel.send(embed=
                           embed)
        
    except Exception as e:
        await ctx.response.send_message(f"Произошла ошибка: {str(e)}")


@bot.slash_command(name="warn", description="Выдать предупреждение пользователю")
async def warn(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    duration: int = SlashOption(
        name="duration",
        choices={
            "Навсегда": 0, 
            "30 дней": 30, 
            "Пользовательский": -1
        },
        required=True
    ), 
    reason: str = SlashOption(
        name="reason",
        required=True
    )):
    if duration == -1:
        modal = nextcord.ui.Modal(title="Введите пользовательский срок")
        
        custom_duration = nextcord.ui.TextInput(
            label="Срок в днях",
            placeholder="Введите количество дней",
            required=True
        )

        if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
            await ctx.response.send_message("У вас нет прав для использования этой команды.")
            return
        
        modal.add_item(custom_duration)
        
        async def modal_callback(interaction: nextcord.Interaction):
            custom_duration_value = custom_duration.value
            try:
                
                await interaction.response.send_message(f"Выдано предупреждение пользователю {member.mention} на срок {custom_duration_value}, причина: {reason}") 
                await member.send(f'Вы получили варн по причине {reason}\nПолучили варн от администратора: {interaction.user.mention}\nСрок выдачи варна: {custom_duration_value} дней.')
            except:
                await interaction.response.send_message(f'Вы неправильно выдали варн пользователю: {member.mention}!\nВы неправильно указали время в днях: {custom_duration_value}\nПричина варна: {reason}')
            await interaction.response.send_message(f'Пользовательский срок установлен на {custom_duration_value} дней.')
        modal.callback = modal_callback
        await ctx.response.send_modal(modal)
    else:
        await member.send(f'Вы получили варн по причине {reason}\nПолучили варн от администратора: {ctx.user.mention}\nСрок выдачи варна: {duration}')
        await ctx.response.send_message(f"Выдано предупреждение пользователю {member.mention} на срок {duration}, причина: {reason}")
    



bot.run(TOKEN)