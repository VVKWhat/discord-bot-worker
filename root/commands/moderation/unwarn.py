import events.sqlite as sqlite
from main import nextcord, SlashOption, bot as root
@root.slash_command(name="unwarn", description="Снять  предупреждение пользователю")
async def warn(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    reason: str = SlashOption(
        name="reason",
        required=True
    )):

    if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
        await ctx.response.send_message("У вас нет прав для использования этой команды.")
        return
    select_value = sqlite.cursor.execute(f'SELECT * FROM `bot_warns` WHERE `bot_warns`.`user_id` = {member.id}')
    print(select_value)
    
    await ctx.response.send_message(f"Снято предупреждение {member.mention}, причина: {reason}\nпричина прошлого предупреждения: {select_value[2][0]}") 
    await member.send(f'Вы получили варн по причине {reason}\nПолучили варн от администратора: {ctx.user.mention}\nСрок выдачи варна: ----- дней.')
    sqlite.sql.commit()