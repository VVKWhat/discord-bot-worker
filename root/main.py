import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
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


@bot.slash_command(name="ban", description="Забанить пользователя")
async def ban(
    ctx: nextcord.application_command,
    member: nextcord.Member,
    ban_type: Option(str, "Тип бана", choices=["вечный", "без апелляции", "с доступом к апелляциям"], option_type=nextcord.ApplicationCommandOptionType.string),
    hours: Option(int, "Количество часов", required=True, default=0, option_type=nextcord.ApplicationCommandOptionType.integer),
    reason: Option(str, "Причина", required=True, option_type=nextcord.ApplicationCommandOptionType.string)
):
    role_ids = {
        'вечный': 1242234003428212837,
        'без апелляции': 1242232941422051358,
        'с доступом к апелляциям': 1242234027742859294
    }
    
    role_id = role_ids.get(ban_type.lower())
    if role_id is None:
        await ctx.respond('Неверно указан тип бана.', ephemeral=True)
        return
    
    role = ctx.guild.get_role(role_id)
    if role is None:
        await ctx.respond('Роль не найдена.', ephemeral=True)
        return
    
    if ban_type.lower() in ['вечный', 'без апелляции']:
        duration = None
    else:
        duration = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
    
    await member.add_roles(role)
    if duration:
        end_date = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
        await ctx.respond(f'{member.mention} был забанен типом {ban_type} на {hours} часов по причине: {reason}.', ephemeral=True)
        # Отправка уведомления в канал
        await send_notification(ctx.guild, member, ban_type, hours, reason, ctx.user, end_date)
        # Здесь вы можете сохранить информацию о бане в базе данных или файле
    else:
        await ctx.respond(f'{member.mention} был забанен на вечное время по причине: {reason}.', ephemeral=True)
        # Отправка уведомления в канал
        await send_notification(ctx.guild, member, ban_type, None, reason, ctx.user, None)
        # Здесь вы также можете сохранить информацию о вечном бане

async def send_notification(guild, member, ban_type, duration, reason, moderator, end_date=None):
    channel = guild.get_channel(notification_channel_id)
    if channel is None:
        print("Канал уведомлений не найден.")
        return
    
    embeds = []
    
    # Embed 1: Уведомление о бане
    embed1 = Embed(description=f"⠀\n‼️⠀⠀**{member.display_name}, вы были забанены за нарушение правил сервера!**\n⠀\n❓⠀⠀Канал с частыми вопросами: <#1242236181505376366>", color=2829617)
    embed1.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
    embeds.append(embed1)
    
    # Embed 2: Информация о бане
    duration_text = f"{duration} часов" if duration else "Навсегда"
    appeal_text = "У вас есть возможность подачи апелляции!\n> В канале <#1242236306571001876>" if ban_type.lower() == 'с доступом к апелляциям' else ""
    embed2 = Embed(
        description=f"""⠀
- Срок вашего наказания:
> {duration_text}
⠀
- Причина выдачи наказания:
> {reason}
⠀
- Наказание выдал(-а):
> {moderator.mention}
⠀
- Дата окончания наказания:
> {end_date.strftime('%d %B %Y, %H:%M') if end_date else 'Навсегда'}

- Дополнительно:
> {appeal_text}
        """, 
        color=16711680
    )
    embed2.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
    embeds.append(embed2)
    
    for embed in embeds:
        await channel.send(content=member.mention, embed=embed)

bot.run(TOKEN)