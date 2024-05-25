import events.sqlite as sqlite
from main import nextcord, datetime, SlashOption, bot as root

@root.slash_command(name="warn", description="Выдать предупреждение пользователю")
async def warn(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    duration: int = SlashOption(
        name="duration",
        description="Время в днях",
        choices={
            "Навсегда": -2, 
            "30 дней": 30, 
            "Пользовательский": -1
        },
        required=True
    ), 
    reason: str = SlashOption(
        name="reason",
        description="Причина",
        required=True
    )
):
    guild = ctx.guild
    if not guild:
        await ctx.response.send_message("Эта команда может быть использована только на сервере.")
        return
    
    channel = root.get_channel(1242246527712235582)
    warn_member = sqlite.cursor.execute(f'SELECT * FROM `bot_warns` WHERE `bot_warns`.`user_id` = {member.id}').fetchall()
    warn_member_len = len(warn_member)
    embed1 = nextcord.Embed(
        description=f"  \n**Вы получили предупреждение на сервере.** ({warn_member_len+1}/4)",
        color=0xA7A7D7
    )
    embed2 = nextcord.Embed(
        description=f"### **Причина**\n⠀\n> \"{reason}\"\n⠀\n### **Модератор**\n⠀\n> <@{ctx.user.id}>",
        color=0xA7A7D7
    )
    embed3 = nextcord.Embed(
        description="",
        color=0xA7A7D7
    )
    embed1.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
    embed2.set_image(url="https://i.ibb.co/26ySjnr/filler.png")
    embed3.set_image(url="https://i.ibb.co/M7DtSqd/banner.png")
    
    if duration == -1:
        modal = nextcord.ui.Modal(title="Введите пользовательский срок")
        
        custom_duration = nextcord.ui.TextInput(
            label="Срок в днях",
            placeholder="Введите количество дней",
            required=True
        )

        if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
            await ctx.response.send_message("У вас нет прав для использования этой команды.")
            return
        
        modal.add_item(custom_duration)
        
        async def modal_callback(interaction: nextcord.Interaction):
            custom_duration_value = custom_duration.value
            try:
                sqlite.cursor.execute(
                    'INSERT INTO bot_warns (user_id, reason, expired_days) VALUES (?, ?, ?)',
                    (member.id, reason, custom_duration_value)
                )
                sqlite.sql.commit()
                await interaction.response.send_message(
                    f"Выдано предупреждение пользователю {member.mention} на срок {custom_duration_value} д.\nпричина: {reason}"
                )
            except Exception as e:
                await interaction.response.send_message(
                    f'Ошибка при выдаче варна пользователю {member.mention}!\nОшибка: {str(e)}'
                )
                return

        modal.callback = modal_callback
        await ctx.response.send_modal(modal)

    else:
        sqlite.cursor.execute(
            'INSERT INTO bot_warns (user_id, reason, expired_days) VALUES (?, ?, ?)',
            (member.id, reason, duration)
        )
        sqlite.sql.commit()
        
        if duration != -2:
            await ctx.response.send_message(f"Выдано предупреждение пользователю {member.mention} на срок {duration} д.\nпричина: {reason}")
        else:    
            await ctx.response.send_message(f"Выдано предупреждение пользователю {member.mention} на срок **навсегда**\nпричина: {reason}")
    
    if (warn_member_len + 1) >= 4:
        embed_1 = nextcord.Embed(
            description="⠀\n‼️⠀⠀**Вы были забанены за нарушение правил сервера!**\n\n❓⠀⠀Канал с частыми вопросами: <#1242236181505376366>\n",
            color=0xA7A7D7
        )
        unban_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=168)
        unban_time_sql = sqlite.adapt_datetime(unban_time)
        sqlite.sql.execute(
            'INSERT INTO bot_bans (user_id, admin_id, reason, expired, appelation) VALUES (?, ?, ?, ?, ?)', 
            (member.id, 1235625733431234681, "Получение больше 4-х предупреждений", unban_time_sql, False)
        )
        sqlite.sql.commit()
        
        embed_2 = nextcord.Embed(
            description=f"⠀⠀\n- Срок вашего наказания:\n> 168 ч. (7 дней)\n⠀\n- Причина выдачи наказания:\n> Получение больше 4-х предупреждений\n⠀\n- Наказание выдал(-а):\n> <@1235625733431234681>\n⠀\n- Дата окончания наказания:\n> {unban_time.strftime('%d %B %Y, %H:%M')} (UTC)",
            color=0xA7A7D7
        )
        embed_3 = nextcord.Embed(
            description="",
            color=0xA7A7D7
        )
        embed_3.set_image(url="https://i.ibb.co/b21F1Mf/ban.png")
        embed_2.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        embed_1.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        
        await member.add_roles(guild.get_role(1242232941422051358))
        await channel.send(embed=embed_1)
        await member.send(embed=embed_1)
        await channel.send(embed=embed_2)
        await member.send(embed=embed_2)
        await channel.send(embed=embed_3)
        await member.send(embed=embed_3)

    await channel.send(embed=embed1)
    await member.send(embed=embed1)
    await channel.send(embed=embed2)
    await member.send(embed=embed2)
    await channel.send(embed=embed3)
    await member.send(embed=embed3)
    return
