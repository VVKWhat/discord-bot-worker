from main import nextcord, commands, json, bot as root

# Проверка прав доступа пользователя: должен иметь одну из двух указанных ролей
@root.slash_command(description="Отправляет JSON в выбранный канал.")
@commands.has_any_role(1242265397735067698, 1242267372052545576)
async def send_json(ctx: nextcord.Interaction, attachment: nextcord.Attachment, channel: nextcord.TextChannel):
    await ctx.response.defer()  # Отложенный ответ на взаимодействие пользователя

    # Проверка
    if not attachment.filename.endswith('.json'):
        await ctx.followup.send("Пожалуйста, прикрепите JSON.")
        return

    try:
        # Чтение содержимого прикрепленного файла
        file_content = await attachment.read()
        # Расшифровка JSON данных
        data = json.loads(file_content)
    except json.JSONDecodeError:
        await ctx.followup.send("Не удалось прочесть JSON.")
        return

    try:
        # Отправка в канал встраиваемых сообщений из данных JSON
        for item in data['embeds']:
            embed = nextcord.Embed.from_dict(item)
            await channel.send(embed=embed)
        await ctx.followup.send("Сообщение было отправлено.")
    except Exception as e:
        # Обработка ошибки и отправка сообщения об ошибке
        await ctx.followup.send(f"Ошибка: {str(e)}")