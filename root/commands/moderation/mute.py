import events.sqlite as sqlite
from main import  nextcord, SlashOption, datetime, bot as root
# Бан участника
@root.slash_command(name="mute", description="Выдать мут участнику")
async def mute(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    duration: int = SlashOption(
        name="duration",
        description= "Время в часах",
        required=True
    ), 
    reason: str = SlashOption(
        name="reason",
        description= "Причина выдачи",
        required=True
    )
):
    try:
        guild = ctx.guild
        # Если команда вызывается не на сервере
        if not guild:
            await ctx.response.send_message("Эта команда может быть использована только на сервере.")
            return

        # ID бан-ролей
        mute_role = guild.get_role(1242266843499200684)

        # Если участник не имеет админ-ролей
        if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
            await ctx.response.send_message("У вас нет прав для использования этой команды.")
            return
        
        # Если участник уже в бане
        if member.get_role(1242266843499200684) is not None:
            await ctx.response.send_message("Данный пользователь уже в муте.")
            return 
        
        # Если модератор пытается забанить себя
        if ctx.user.mention == member.mention:
            print(f"{ctx.user.display_name} долбоёб - пытался себя замутить =-=") # Ай-яй-яй Foxanto
            await ctx.response.send_message("Вы не можете замутить себя.")
            return
        
        await member.add_roles(mute_role)

        unban_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=duration)
        
        # Ответ на бан модератору
        await ctx.response.send_message(f"{member.mention} был замучен на {duration}ч. по причине: \"{reason}\".")

        channel = root.get_channel(1242246527712235582)
        ## ADD NEW DATA IN DATABASE ##

        unban_time_sql = sqlite.adapt_datetime(unban_time)
        sqlite.sql.execute('INSERT INTO bot_mutes (user_id, admin_id, reason, expired) VALUES (?, ?, ?, ?)', (member.id, ctx.user.id, reason, unban_time_sql))
        sqlite.sql.commit()
        ## END ADD NEW DATA IN DATABASE ##
        if not channel:
            await ctx.response.send_message("Не удалось найти канал для отправки сообщения.")
            return
        # Упоминание забаненного участника
        await channel.send(f'<@{member.id}>')
        # EMBED 1
        embed_1 = nextcord.Embed(
            description=" ⠀\nВы были замьючены за нарушения правил сервера.",
            color=0xA7A7D7,
            url= "https://i.ibb.co/26ySjnr/filler.png"
            
        )
        embed_2 =nextcord.Embed(
            description=f"### **Причина**\n⠀\n> \"{reason}\"\n⠀\n###  **Длительность**\n⠀\n> **{duration}**ч.\n⠀\n### **Дата истечения**\n⠀\n> {unban_time.strftime('%d %B %Y, %H:%M')} (UTC)\n⠀\n### **Модератор**\n⠀\n> <@{ctx.user.id}>",
            color=0xA7A7D7,
            url='https://i.ibb.co/26ySjnr/filler.png'
        )
        embed_3 = nextcord.Embed(
            description="",
            color=0xA7A7D7
        )
        embed_1.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
        embed_2.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
        embed_3.set_image(url="https://i.ibb.co/M7DtSqd/banner.png")
        await channel.send(embed=embed_1)
        try:
            await member.send(embed=embed_1)
            await member.send(embed=embed_2)
            await member.send(embed=embed_3)
        except nextcord.Forbidden:
            await ctx.followup.send("Не удалось отправить личное сообщение пользователю.", ephemeral=True)
        
        await channel.send(embed=embed_2)
        await channel.send(embed=embed_3)
    except Exception as e:
        await ctx.response.send_message(f"Произошла ошибка: {str(e)}")