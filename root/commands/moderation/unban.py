import events.sqlite as sqlite
from main import nextcord, SlashOption, bot as root

# Снять бан участника
@root.slash_command(name="unban", description="Убрать существующий бан пользователю")
async def unban(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    reason: str = SlashOption(
        name="reason",
        description="Причина выдачи",
        required=True
    )
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
            print(f"{ctx.user.display_name} пытался себя разбанить.")
            await ctx.response.send_message("Вы не имеете полномочий для того, чтобы разбанить самого себя.")
            return
        # Если пользователь не забанен
        if member.get_role(1242234027742859294) is None and member.get_role(1242232941422051358) is None:
            await ctx.response.send_message("Данный пользователь не забанен!")
            return

        sqlite.cursor.execute(f'DELETE FROM `bot_bans` WHERE `bot_bans`.`user_id` = {member.id}')

        if ban_appeal in member.roles:
            await member.remove_roles(ban_appeal)
            response_message = f'⠀\nПользователь {member.mention} был разбанен администратором {ctx.user.mention}\n⠀\nПричина снятия бана: **{reason}**\n⠀\nУ данного пользователя был бан с аппеляцией.'
        elif ban_no_appeal in member.roles:
            await member.remove_roles(ban_no_appeal)
            response_message = f'⠀\nПользователь {member.mention} был разбанен администратором {ctx.user.mention}\n⠀\nПричина снятия бана: **{reason}**\n⠀\нУ данного пользователя был бан без возможности аппеляции.'
        else:
            await ctx.response.send_message("Данный пользователь не забанен!")
            return

        sqlite.sql.commit()
        await ctx.response.send_message(response_message)

        try:
            await member.send(f'Вы были разбанены администратором {ctx.user.mention}\n**Начинайте наслаждаться моментом!**')
        except nextcord.Forbidden:
            await ctx.followup.send(f"Не удалось отправить ЛС пользователю {member.mention}. Возможно, он отключил ЛС или заблокировал бота.", ephemeral=True)

        channel = root.get_channel(1242246527712235582)
        if not channel:
            await ctx.followup.send("Не удалось найти канал для отправки сообщения.", ephemeral=True)
            return

        embed1 = nextcord.Embed(
            description="\n**С вас было снято наказание.**",
            color=0xA7A7D7,
            url="https://i.ibb.co/26ySjnr/filler.png"
        )
        embed2 = nextcord.Embed(
            description=f"### **Причина**\n⠀\n> \"{reason}\"\n⠀\н### **Модератор**\n⠀\н> <@{ctx.user.id}>",
            color=0xA7A7D7,
            url="https://i.ibb.co/26ySjnr/filler.png"
        )
        embed3 = nextcord.Embed(
            description="",
            color=0xA7A7D7
        )
        embed1.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
        embed2.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
        embed3.set_image(url="https://i.ibb.co/M7DtSqd/banner.png")

        await channel.send(embed=embed1)
        await channel.send(embed=embed2)
        await channel.send(embed=embed3)
        try:
            await member.send(embed=embed1)
            await member.send(embed=embed2)
            await member.send(embed=embed3)
        except nextcord.Forbidden:
            await ctx.followup.send(f"Не удалось отправить ЛС пользователю {member.mention}. Возможно, он отключил ЛС или заблокировал бота.", ephemeral=True)
        
    except Exception as e:
        if not ctx.response.is_done():
            await ctx.response.send_message(f"Произошла ошибка: {str(e)}")
        else:
            await ctx.followup.send(f"Произошла ошибка: {str(e)}")
