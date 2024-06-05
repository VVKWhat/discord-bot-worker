import events.sqlite as sql
from nextcord.ext.commands.bot import Bot
from nextcord import Interaction
from main import guild
from nextcord import Embed
async def create_ticket_channel(user_id: int, reason: str, ctx: Interaction, bot: Bot):
    """
    Создаёт канал с тикетом
    Возвращает ticket_id (Channel id тикета)
    """
    _guild = guild
    embed = Embed(
        title="⠀\n**Ваш Тикет / Ваша Апелляция.**",
        description="### **Приветствуем!**\n⠀\n> Ваш тикет был открыт, а агенты поддержки упомянуты об этом.\n⠀\n> Не нужно пинговать их, они ответят сразу, как только смогут.",
        color= 0xA7A7D7
    )
    user = bot.get_user(user_id).mention
    channel_id = await guild.create_text_channel(name=f"{user}-Тикет")
    sql.cursor.execute('INSERT INTO `bot_tickets` (`id_ticket`,`user_id`,`reason`) VALUES (?,?,?)', (channel_id,user_id,reason))
    await ctx.send(embed=embed)

    sql.sql.commit()

async def handler_save_history(ticket_id: int):
    """
    Обработчик сохранения истории тикета в БД 
    Забавный факт что функция будет вызываться ивентов on_message
    """
    _len = sql.cursor.execute('SELECT * FROM `bot_tickets` WHERE `bot_tickets`.`id_ticket` = ?', (ticket_id))
    if len(_len) <= 0:
        return None

    sql.sql.commit()