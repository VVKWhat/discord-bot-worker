from main import nextcord, commands, json, bot as root

@root.slash_command(name="clear", description="Очищает указанное количество сообщений")
@commands.has_any_role(1242265397735067698, 1242267372052545576, 1242266974713544825, 1242266949250056304)
async def clear(ctx: nextcord.Interaction, amount: int):
    if amount > 100:
        await ctx.response.send_message("Максимальное количество сообщений, которое можно очистить - 100!")
        return
    if amount < 1:
        await ctx.response.send_message("Минимальное количество сообщений, которое можно очистить - 1!")
        return

    deleted = await ctx.channel.purge(limit=amount)

    embed_1 = nextcord.Embed(
        description=f"⠀\n**Успешно очищено {len(deleted)} сообщений!**",
        color=0xA7A7D7
    )
    embed_1.set_image(url="https://i.ibb.co/ZWBrwLk/filler.png")
    await ctx.response.send_message(embed=embed_1)

    embed_2 = nextcord.Embed(
        description="",
        color=0xA7A7D7
    )
    embed_2.set_image(url="https://i.ibb.co/M7DtSqd/banner.png")
    await ctx.channel.send(embed=embed_2)