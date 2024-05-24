import events.sqlite as sqlite
from main import  nextcord, SlashOption, datetime, bot as root
# Бан участника
@root.slash_command(name="get_database", description="Выдать бан участнику")
async def get_database(
    ctx: nextcord.Interaction, 
):
    try:
        guild = ctx.guild
        # Если команда вызывается не на сервере
        if not guild:
            await ctx.response.send_message("Эта команда может быть использована только на сервере.")
            return

        # Если участник не имеет админ-ролей
        if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
            await ctx.response.send_message("У вас нет прав для использования этой команды.")
            return

        warns = sqlite.cursor.execute('SELECT * FROM bot_warns;').fetchall()
        users = sqlite.cursor.execute('SELECT * FROM bot_users;').fetchall()
        bans = sqlite.cursor.execute('SELECT * FROM bot_bans;').fetchall()
        sqlite.sql.commit()
        await ctx.response.send_message('База данных отправлена в личные сообщения', ephemeral=True)
        await ctx.user.send(f'Варны: `{warns}`')
        await ctx.user.send(f'Баны: `{bans}`')
        await ctx.user.send(f'Пользователи: `{users}`')
        return
    except Exception as e:
        await ctx.response.send_message(f"Произошла ошибка: {str(e)}")
        return