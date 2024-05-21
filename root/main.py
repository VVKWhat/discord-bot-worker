import nextcord
from nextcord.ext import commands
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

bot.run(TOKEN)