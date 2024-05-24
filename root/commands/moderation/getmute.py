import events.sqlite as sqlite
from main import nextcord, datetime, SlashOption, bot as root
@root.slash_command(name="getmute", description="Получить варны у пользователя")
async def getmute(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, ):
    guild = ctx.guild

    if not guild:
        await ctx.response.send_message("Эта команда может быть использована только на сервере.")
        return
    
    if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
        await ctx.response.send_message("У вас нет прав для использования этой команды.")
        return
    all_warns = sqlite.cursor.execute(f'SELECT * FROM `bot_mutes` WHERE `bot_mutes`.`user_id` = {member.id}').fetchall()
    print(all_warns)
    warns = ''
    for warn in all_warns:
        date = warn[5]
        timestamp: datetime.datetime = warn[4].strftime('%H:%M %d.%m.%Y')
        warns = warns+f'`id: {warn[0]}, причина: {warn[3]}, дата выдачи: {timestamp}, время: {date} часов`\n'
    await ctx.response.send_message(f"Все предупреждения пользователя {member.mention}\n{warns}") 
    sqlite.sql.commit()