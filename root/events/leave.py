from root.main import nextcord, bot as root, gateway_channel_id
# Вышел участник
@root.event
async def on_member_remove(member):
    # Уведомление о выходе участника в консоли
    print(f'Участник покинул нас! {member.display_name}')
    channel = root.get_channel(gateway_channel_id)
    if member.bot:
        return
    # Уведомление о выходе участника в прихожей
    elif channel is not None:
        # EMBED 1
        embed_1 = nextcord.Embed(
            description=f"⠀\n👋🏻⠀⠀**До скорых встреч!**",
            color=0xA7A7D7
        )
        # ФИЛЛЕР
        embed_1.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
        await channel.send(embed=embed_1)
        # EMBED 2
        embed_2 = nextcord.Embed(
            description=f"⠀\n**Надеемся, что мы встретимся снова!**\n⠀\n**Пользователя пригласил:**\n⠀\n> ПРИГЛАСИЛ: пока нет",
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
    else:
        print(f"Не удалось найти канал для отправки сообщения.")
