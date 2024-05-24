import events.sqlite as sqlite
from main import nextcord, SlashOption, bot as root
@root.slash_command(name="unwarn", description="Снять  предупреждение пользователю")
async def unwarn(
    ctx: nextcord.Interaction, 
    id: int = SlashOption(
        name="id",
        required=True
    ),
    reason: str = SlashOption(
        name="reason",
        required=True
    )):
    
    guild = ctx.guild

    if not guild:
        await ctx.response.send_message("Эта команда может быть использована только на сервере.")
        return
    
    if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
        await ctx.response.send_message("У вас нет прав для использования этой команды.")
        return

    select_value = sqlite.cursor.execute(f'SELECT * FROM `bot_warns` WHERE `bot_warns`.`id` = {id}').fetchall()
    print(select_value)
    
    if len(select_value) <=0:
        await ctx.send(f'Нету такого айди (id: {id})')
        return
    member = root.get_user(select_value[0][1])
    if ctx.user.mention == member.mention:
            print(f"{ctx.user.display_name} долбоёб - пытался снять с себя предупреждение =-=")
            await ctx.response.send_message("Вы не имеете полномочий для того, чтобы снять предупреждений с самого себя.")
            return
    sqlite.cursor.execute(f'DELETE FROM `bot_warns` WHERE `bot_warns`.`id` = {id}')
    await ctx.response.send_message(f"Снято предупреждение {member.mention}, причина: {reason}\nID предупреждения: {id}\nПричина прошлого предупреждения: {select_value[0][2]}") 
    await member.send(f'У вас снял предупреждение {ctx.user.mention}\nПричина снятия: {reason}\n\nПричина прошлого предупреждение: {select_value[0][2]}')
    sqlite.sql.commit()