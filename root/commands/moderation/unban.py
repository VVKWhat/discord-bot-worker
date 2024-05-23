import events.sqlite as sqlite
from main import nextcord, bot as root
# Снять бан участника
@root.slash_command(name="unban", description="Убрать существующий бан пользователю")
async def unban(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    reason: str, 
):
    try:
        guild = ctx.guild
        # Если команда вызывается не на сервере
        if not guild:
            await ctx.response.send_message("Эта команда может быть использована только на сервере.")
            return

        ban_appeal = guild.get_role(1242234027742859294)
        ban_no_appeal = guild.get_role(1242232941422051358)

        # Если пользователь не имеет ролей
        if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
            await ctx.response.send_message("У вас нет прав для использования этой команды.")
            return
        # Если пользователь пытается разбанить себя
        if ctx.user.mention == member.mention:
            print(f"{ctx.user.display_name} долбоёб - пытался себя разбанить =-=") # Ай-яй-яй Foxanto X2
            await ctx.response.send_message("Вы не имеете полномочий для того, чтобы разбанить самого себя.")
            return
        # Если пользователь не забанен
        if member.get_role(1242234027742859294) is not None and member.get_role(1242232941422051358) is not None:
            await ctx.response.send_message("Данный пользователь не забанен!")
            return
        if ban_appeal in member.roles or ban_no_appeal in member.roles:
            


            if ban_appeal in member.roles:
                await member.remove_roles(ban_appeal)
                await ctx.response.send_message(f'⠀\nПользователь {member.mention} был разбанен администратором {ctx.user.mention}\n⠀\nПричина снятия бана: **{reason}**\n⠀\nУ данного пользователя был бан с аппеляцией.')
                await member.send(f'Вы были разбанены администратором {ctx.user.mention}\n**Начинайте наслаждаться моментом!**')
                
            if ban_no_appeal in member.roles:
                await member.remove_roles(ban_no_appeal)
                await ctx.response.send_message(f'⠀\nПользователь {member.mention} был разбанен администратором {ctx.user.mention}\n⠀\nПричина снятия бана: **{reason}**\n⠀\nУ данного пользователя был бан без возможности аппеляции.')
                await member.send(f'Вы были разбанены администратором {ctx.user.mention}\n**Начинайте наслаждаться моментом!**')

        else:
            await ctx.response.send_message("Данный пользователь не забанен!")
            
        channel = root.get_channel(1242246527712235582)
        if not channel:
            await ctx.response.send_message("Не удалось найти канал для отправки сообщения.")
            return
        embed = nextcord.Embed(
            description=f"⠀\n-Разбанен пользователь:\n> {member.mention}\n⠀\n- Причина:\n> {reason}\n⠀\n- Наказание снял(-а):\n> <@{ctx.user.id}>\n",
            color=0xA7A7D7
        )
        embed.set_image(url="https://i.ibb.co/b21F1Mf/ban.png")
        await channel.send(embed=
                           embed)
        
    except Exception as e:
        await ctx.response.send_message(f"Произошла ошибка: {str(e)}")

