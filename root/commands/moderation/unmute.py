import events.sqlite as sqlite
from main import nextcord, SlashOption, bot as root
@root.slash_command(name="unmute", description="Снять предупреждение пользователю")
async def unmute(
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

    select_value = sqlite.cursor.execute(f'SELECT * FROM `bot_mutes` WHERE `bot_mutes`.`id` = {id}').fetchall()
    print(select_value)
    channel = root.get_channel(1242246527712235582)
    if len(select_value) <=0:
        await ctx.send(f'Нету такого айди (id: {id})')
        return
    member = root.get_user(select_value[0][1])
    if ctx.user.mention == member.mention:
            print(f"{ctx.user.display_name} долбоёб - пытался снять с себя мут =-=")
            await ctx.response.send_message("Вы не имеете полномочий для того, чтобы снять мут с самого себя.")
            return
    sqlite.cursor.execute(f'DELETE FROM `bot_mutes` WHERE `bot_mutes`.`id` = {id}')
    embed1 = nextcord.Embed(
         description='⠀\n**С вас был снят мьют.**',
         color=0xA7A7D7
    )
    embed2 = nextcord.Embed(
         description=f"### **Причина**\n⠀\n> \"{reason}\"\n⠀\n### **Модератор**\n⠀\n> <@{ctx.user.id}>",
         color=0xA7A7D7
    )
    embed3 = nextcord.Embed(
         description='',
         color=0xA7A7D7
    )
    embed1.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
    embed2.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
    embed3.set_image('https://i.ibb.co/M7DtSqd/banner.png"')
    await channel.send(member.mention)
    await channel.send(embed=embed1)
    await channel.send(embed=embed2)
    await channel.send(embed=embed3)
    await ctx.response.send_message(f"Снят мут пользователю {member.mention}, причина: {reason}\nID предупреждения: {id}\nПричина прошлого предупреждения: {select_value[0][3]}") 
    await member.send(embed=embed1)
    await member.send(embed=embed2)
    await member.send(embed=embed3)
    sqlite.sql.commit()