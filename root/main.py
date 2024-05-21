import nextcord
from nextcord.ext import commands
import datetime
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(current_dir, "token")

with open(token_file, "r") as f:
    TOKEN = f.read().strip()

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

notification_channel_id = 1242246527712235582

@bot.event
async def on_ready():
    print()
    print(f'Бот {bot.user.name} успешно запущен.')


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


@bot.event
async def on_member_ban(guild, user):
    channel = bot.get_channel(1242246527712235582)
    await channel.send(f'<@{user.id}>')
    embed = nextcord.Embed(
        description="⠀\n‼️⠀⠀**Вы были забанены за нарушение правил сервера!**\n⠀\n❓⠀⠀Канал с частыми вопросами: <#1242236181505376366>",
        color=nextcord.Color.red()
    )
    embed.add_field(name="- Срок вашего наказания:", value="> Placeholder (заменить на срок бана)")
    embed.add_field(name="- Причина выдачи наказания:", value="> Placeholder (заменить на причину бана)")
    embed.add_field(name="- Наказание выдал(-а):", value=f"> <@{bot.user.id}>")
    embed.add_field(name="- Дата окончания наказания:", value="> Placeholder (заменить на дату окончания бана)")
    embed.add_field(name="- Дополнительно:", value="> У вас есть возможность подачи апелляции!\n> В канале <#1242236306571001876>")
    await channel.send(embed=embed)

@bot.slash_command (name="ban",
    description="Выдать бан с возможностью апелляции.",
    options=[
        nextcord.option.Option("пользователь", "Пользователь для бана.", nextcord.option.OptionType.USER, True),
        nextcord.option.Option("срок", "Срок бана в часах.", nextcord.option.OptionType.INTEGER, True),
        nextcord.option.Option("причина", "Причина бана.", nextcord.option.OptionType.STRING, True)
    ])
async def ban(ctx: nextcord.Interaction, пользователь: nextcord.Member, срок: int, причина: str):
    guild = ctx.guild
    ban_role = guild.get_role(1242234027742859294)
    if ctx.author.top_role.id in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
        await пользователь.add_roles(ban_role)
        unban_time = datetime.datetime.now() + datetime.timedelta(hours=срок)
        await ctx.send(f"{пользователь.mention} был забанен на {срок} часов. Причина: {причина}.")
        channel = bot.get_channel(1242246527712235582)
        await channel.send(f'<@{пользователь.id}>')
        embed = nextcord.Embed(
            description="⠀\n‼️⠀⠀**Вы были забанены за нарушение правил сервера!**\n⠀\n❓⠀⠀Канал с частыми вопросами: <#1242236181505376366>",
            color=nextcord.Color.red()
        )
        embed.add_field(name="- Срок вашего наказания:", value=f"> {срок} часов")
        embed.add_field(name="- Причина выдачи наказания:", value=f"> {причина}")
        embed.add_field(name="- Наказание выдал(-а):", value=f"> <@{ctx.author.id}>")
        embed.add_field(name="- Дата окончания наказания:", value=f"> {unban_time.strftime('%d %B %Y, %H:%M')}")
        embed.add_field(name="- Дополнительно:", value="> У вас есть возможность подачи апелляции!\n> В канале <#1242236306571001876>")
        await channel.send(embed=embed)
    else:
        await ctx.send("У вас нет прав для использования этой команды.")

bot.run(TOKEN)