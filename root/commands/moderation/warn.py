import events.sqlite as sqlite
from main import nextcord, SlashOption, bot as root
@root.slash_command(name="warn", description="Выдать предупреждение пользователю")
async def warn(
    ctx: nextcord.Interaction, 
    member: nextcord.Member, 
    duration: int = SlashOption(
        name="duration",
        choices={
            "Навсегда": 0, 
            "30 дней": 30, 
            "Пользовательский": -1
        },
        required=True
    ), 
    reason: str = SlashOption(
        name="reason",
        required=True
    )):
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
                sqlite.cursor.execute('INSERT `bot_warns` INTO `bot_warns`.`users_id`, `bot_warns`.`reason`, `bot_warns`.`expired_days` VALUES (?.?,?)', member.id, reason, custom_duration_value)
                sqlite.sql.commit()
                await interaction.response.send_message(f"Выдано предупреждение пользователю {member.mention} на срок {custom_duration_value}, причина: {reason}") 
                await member.send(f'Вы получили варн по причине {reason}\nПолучили варн от администратора: {interaction.user.mention}\nСрок выдачи варна: {custom_duration_value} дней.')
            except:
                await interaction.response.send_message(f'Вы неправильно выдали варн пользователю: {member.mention}!\nВы неправильно указали время в днях: {custom_duration_value}\nПричина варна: {reason}')
            await interaction.response.send_message(f'Пользовательский срок установлен на {custom_duration_value} дней.')
        modal.callback = modal_callback
        await ctx.response.send_modal(modal)

    else:
        await member.send(f'Вы получили варн по причине {reason}\nПолучили варн от администратора: {ctx.user.mention}\nСрок выдачи варна: {duration}')
        await ctx.response.send_message(f"Выдано предупреждение пользователю {member.mention} на срок {duration}, причина: {reason}")
    