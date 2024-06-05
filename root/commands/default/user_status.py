import events.sqlite as sqlite
from main import nextcord, datetime, SlashOption, bot as root

@root.slash_command(name="user_status", description="Получить информацию о пользователя")
async def user_status(
    ctx: nextcord.Interaction, 
    member: nextcord.Member = SlashOption(
        name="member",
        description="Пользователь",
        required=True
    ),
):
    guild = ctx.guild

    if not guild:
        await ctx.response.send_message("Эта команда может быть использована только на сервере.")
        return

    all_warns = sqlite.cursor.execute('SELECT * FROM `bot_warns` WHERE `bot_warns`.`user_id` = ?', (member.id,)).fetchall()
    mute = sqlite.cursor.execute('SELECT * FROM `bot_mutes` WHERE `bot_mutes`.`user_id` = ?', (member.id,)).fetchall()
    ban = sqlite.cursor.execute('SELECT * FROM `bot_bans` WHERE `bot_bans`.`user_id` = ?', (member.id,)).fetchall()
    user = sqlite.cursor.execute('SELECT * FROM `bot_users` WHERE `bot_users`.`user_id` = ?', (member.id,)).fetchall()

    is_warned = False if len(all_warns) <= 0 else True
    is_muted = False if len(mute) <= 0 else True
    is_banned = False if len(ban) <= 0 else True

    warns = ''
    if is_warned:
        for warn in all_warns:
            date = warn[4]
            if date == -2:
                date = 'навсегда'
            timestamp = warn[3].strftime('%H:%M %d.%m.%Y')
            warns += (
                '`id {}`:\n- Причина: `{}`\n- Дата выдачи: `{}`\n- Время: `{}` д.\n'.format(
                    warn[0], warn[2], timestamp, date
                )
            )

    bans = ''
    if is_banned:
        timestamp = ban[0][4].strftime('%H:%M %d.%m.%Y')
        date = ban[0][5].strftime('%H:%M %d.%m.%Y')
        bans = (
            '`id {}`:\n- Причина: {}\n- Выдал: <@{}>\n- Дата выдачи: {}\n- Время: {}\n- Апелляция: {}'.format(
                ban[0][0], ban[0][3], ban[0][2], timestamp, date, "с апелляцией" if bool(ban[0][6]) else "без апелляции"
            )
        )

    mutes = ''
    if is_muted:
        date = mute[0][5].strftime('%H:%M %d.%m.%Y')
        timestamp = mute[0][4].strftime('%H:%М %d.%m.%Y')
        mutes = (
            '`id {}`:\n- Причина: {}\n- Выдал: <@{}>\n- Дата выдачи: {}\n- Время: {}'.format(
                mute[0][0], mute[0][3], mute[0][2], timestamp, date
            )
        )

    embed_description = (
        'Discord-ID: `{}`\nID: `{}`\nВ бане? - {}\nВ муте? {}\nПредупреждения: {}'.format(
            member.id, user[0][0],
            "`Да`\n" + bans + "\n" if is_banned else "`Нет`",
            "`Да`\n" + mutes + "\n" if is_muted else "`Нет`",
            "`Имеется`\n" + warns + "\n" if is_warned else "`Не имеется`"
        )
    )

    embed = nextcord.Embed(
        title="Информация о {}".format(member.display_name),
        description=embed_description,
        color=0xA7A7D7
    )
    await ctx.response.send_message(embed=embed)

    sqlite.sql.commit()
