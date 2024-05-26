import events.sqlite as sqlite
from main import nextcord, datetime, SlashOption, bot as root
@root.slash_command(name="user_status", description="Получить информацию о пользователя")
async def user_status(
    ctx: nextcord.Interaction, 
    member: nextcord.Member = SlashOption(
        name="member",
        description= "Пользователь",
        required=True
    ), ):
    guild = ctx.guild

    if not guild:
        await ctx.response.send_message("Эта команда может быть использована только на сервере.")
        return
    all_warns = sqlite.cursor.execute(f'SELECT * FROM `bot_warns` WHERE `bot_warns`.`user_id` = {member.id}').fetchall()
    mute = sqlite.cursor.execute(f'SELECT * FROM `bot_mutes` WHERE `bot_mutes`.`user_id` = {member.id}').fetchall()
    ban = sqlite.cursor.execute(f'SELECT * FROM `bot_bans` WHERE `bot_bans`.`user_id` = {member.id}').fetchall()
    user = sqlite.cursor.execute(f'SELECT * FROM `bot_users` WHERE `bot_users`.`user_id` = {member.id}').fetchall()
    is_warned = False if len(all_warns) <= 0 else True
    is_muted = False if len(mute) <= 0 else True
    is_banned = False if len(ban) <= 0 else True
    warns = ''
    if is_warned:
        for warn in all_warns:
            date= warn[4]
            if date == -2:
                date = 'навсегда'
            timestamp: datetime.datetime = warn[3].strftime('%H:%M %d.%m.%Y')
            warns = warns+f'`id {warn[0]}`:\n- Причина: `{warn[2]}`\n- Дата выдачи: `{timestamp}`\n- Время: `{date} д.`\n'
    bans = ''
    if is_banned:
        timestamp: datetime.datetime = ban[0][4].strftime('%H:%M %d.%m.%Y')
        date: datetime.datetime = ban[0][5].strftime('%H:%M %d.%m.%Y')
        bans = f"`id {ban[0][0]}`:\n- Причина: {ban[0][3]}\n- Выдал: <@{ban[0][2]}>\n- Дата выдачи: {timestamp}\n- Время: {date}\n- Апелляция: {"с апелляцией" if bool(ban[0][6]) else "без апелляции"}"
    if is_muted:
        date: datetime.datetime = ban[0][5].strftime('%H:%M %d.%m.%Y')
        timestamp: datetime.datetime = mute[0][4].strftime('%H:%M %d.%m.%Y')
        mutes = f"`id {mute[0][0]}`:\n- Причина: {mute[0][3]}\n- Выдал: <@{mute[0][2]}>\n- Дата выдачи: {timestamp}\n- Время: {date}"
    emebed = nextcord.Embed(
        title=f"Информация о {member.display_name}",
        description= f"Discord-ID: `{member.id}`\nID: `{user[0][0]}`\nВ бане? - {f"`Да`\n{bans}\n" if is_banned else "`Нет`"}\nВ муте? {f"`Да`\n{mutes}\n" if is_muted else "`Нет`"}\nПредупреждения: {f"`Имеется`\n{warns}\n" if is_warned else "`Не имеется`"}",
        color=0xA7A7D7
    )
    await ctx.response.send_message(embed=emebed) 
    
    #await ctx.response.send_message(f"Все предупреждения пользователя {member.mention}\n{warns}") 
    sqlite.sql.commit()