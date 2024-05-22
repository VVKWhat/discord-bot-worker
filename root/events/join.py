from root.main import nextcord, bot as root, gateway_channel_id
import root.events.sqlite as sqlite
# Новый участник
@root.event
async def on_member_join(member):
    # Уведомление о присоединении участника в консоли
    print(f'Участник присоединился к нам! {member.display_name}')
    channel = root.get_channel(gateway_channel_id)
    if member.bot:
        return
    # Уведомление о присоединении участника в прихожей
    elif channel is not None:
        # Упоминание присоединившегося участника
        await channel.send(f'<@{member.id}>')
        # EMBED 1
        embed_1 = nextcord.Embed(
            description=f"⠀\n👋🏻⠀⠀**Приветствуем вас на нашем Discord сервере!**",
            color=0xA7A7D7
        )
        # ФИЛЛЕР
        embed_1.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed_1)
        # EMBED 2
        embed_2 = nextcord.Embed(
            description=f"⠀\n**Советуем ознакомиться с следующими каналами:**\n⠀\n> - <#1242213724262105190>\n> - <#1242221576611696811>\n> - <#1242229530861768856>\n⠀\n**Вас пригласил:**\n⠀\n> ПРИГЛАСИЛ: пока нету",
            color=0xA7A7D7
        )
        # ФИЛЛЕР
        embed_2.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed_2)
        # EMBED 3
        embed_3 = nextcord.Embed(
            description=""
        )
        # КАРТИНКА
        embed_3.set_image(url="https://i.ibb.co/jWQhTGH/gateway.png")
        await channel.send(embed=embed_3)
        print(root.user.id,'joined')
        ## USER IS BANNED ##
        answer = sqlite.cursor.execute(f'SELECT `appelation` FROM `bot_bans` WHERE `bot_bans`.`user_id` = {member.id}').fetchall()
        print(answer)
        if len(answer) >= 1:
            has_ban = bool(answer[0][0])
            role_id = 1242234027742859294 if has_ban else 1242232941422051358
            role = member.guild.get_role(role_id)
            await member.add_roles(role)
        sqlite.sql.commit()
        ## END USER IS BANNED ##
    else:
        print(f"Не удалось найти канал для отправки сообщения.")


