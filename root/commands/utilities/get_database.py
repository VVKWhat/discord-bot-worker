import events.sqlite as sqlite
import nextcord
from main import bot as root
import io

# Бан участника
@root.slash_command(name="get_database", description="Выдать бан участнику")
async def get_database(ctx: nextcord.Interaction):
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
        mutes = sqlite.cursor.execute('SELECT * FROM bot_mutes;').fetchall()
        sqlite.sql.commit()

        await ctx.response.send_message('База данных отправлена в личные сообщения', ephemeral=True)
        
        # Создание временного файла для пользователей
        users_content = '\n'.join([str(user) for user in users])
        users_file = io.StringIO(users_content)
        users_file.seek(0)

        # Отправка файлов пользователю
        await ctx.user.send("Варны:", file=nextcord.File(io.StringIO('\n'.join([str(warn) for warn in warns])), filename="warns.txt"))
        await ctx.user.send("Баны:", file=nextcord.File(io.StringIO('\n'.join([str(ban) for ban in bans])), filename="bans.txt"))
        await ctx.user.send("Муты:", file=nextcord.File(io.StringIO('\n'.join([str(mute) for mute in mutes])), filename="mute.txt"))
        await ctx.user.send("Пользователи:", file=nextcord.File(users_file, filename="users.txt"))
        
        return
    except Exception as e:
        if not ctx.response.is_done():
            await ctx.response.send_message(f"Произошла ошибка: {str(e)}")
        else:
            await ctx.followup.send(f"Произошла ошибка: {str(e)}")
        return
