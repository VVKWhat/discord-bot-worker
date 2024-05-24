import events.sqlite as sqlite
from main import  nextcord, SlashOption, datetime, bot as root
# Бан участника
@root.slash_command(name="ban", description="Выдать бан участнику")
async def ban(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    duration: int, 
    reason: str, 
    appeal: str = SlashOption(
        name="appeal",
        choices={
            "С апелляцией": "appeal", 
            "Без апелляции": "noappeal"
        },
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
        ban_appeal = guild.get_role(1242234027742859294)
        ban_no_appeal = guild.get_role(1242232941422051358)

        # Если участник не имеет админ-ролей
        if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
            await ctx.response.send_message("У вас нет прав для использования этой команды.")
            return
        
        # Если участник уже в бане
        if member.get_role(1242234027742859294) is not None or member.get_role(1242232941422051358) is not None:
            await ctx.response.send_message("Данный пользователь уже в бане.")
            return 
        
        # Если модератор пытается забанить себя
        if ctx.user.mention == member.mention:
            print(f"{ctx.user.display_name} долбоёб - пытался себя забанить =-=") # Ай-яй-яй Foxanto
            await ctx.response.send_message("Вы не можете забанить себя.")
            return
        
        # Если модератор выдал возможность апелляции
        if appeal == "appeal":
            await member.add_roles(ban_appeal)
            appeal_text = '\n\n- Дополнительно:\n> У вас есть возможность подачи апелляции!\n> В канале <#1242228411280265388>'
        else:
            await member.add_roles(ban_no_appeal)
            appeal_text = ''

        unban_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=duration)
        
        # Ответ на бан модератору
        await ctx.response.send_message(f"{member.mention} был забанен на {duration}ч. по причине: \"{reason}\".")

        channel = root.get_channel(1242246527712235582)
        ## ADD NEW DATA IN DATABASE ##

        unban_time_sql = sqlite.adapt_datetime(unban_time)
        sqlite.sql.execute('INSERT INTO bot_bans (user_id, admin_id, reason, expired, appelation) VALUES (?, ?, ?, ?, ?)', (member.id, ctx.user.id, reason, unban_time_sql, ('appeal' in appeal)))
        sqlite.sql.commit()
        ## END ADD NEW DATA IN DATABASE ##
        if not channel:
            await ctx.response.send_message("Не удалось найти канал для отправки сообщения.")
            return
        # Упоминание забаненного участника
        await channel.send(f'<@{member.id}>')
        # EMBED 1
        embed_1 = nextcord.Embed(
            description="⠀\n‼️⠀⠀**Вы были забанены за нарушение правил сервера!**\n\n❓⠀⠀Канал с частыми вопросами: <#1242236181505376366>\n",
            color=0xA7A7D7
        )
        embed_2 =nextcord.Embed(
            description=f"⠀⠀\n- Срок вашего наказания:\n> {duration}ч.\n⠀\n- Причина выдачи наказания:\n> {reason}\n⠀\n- Наказание выдал(-а):\n> <@{ctx.user.id}>\n⠀\n- Дата окончания наказания:\n> {unban_time.strftime('%d %B %Y, %H:%M')} (UTC){appeal_text}",
            color=0xA7A7D7
        )
        embed_3 = nextcord.Embed(
            description="",
            color=0xA7A7D7
        )
        embed_3.set_image(url="https://i.ibb.co/b21F1Mf/ban.png")
        #embed_1.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed_1)
        await member.send(embed=embed_1)
        await channel.send(embed=embed_2)
        await member.send(embed=embed_2)
        await channel.send(embed=embed_3)
        await member.send(embed=embed_3)
    except Exception as e:
        await ctx.response.send_message(f"Произошла ошибка: {str(e)}")