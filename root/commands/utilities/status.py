import events.sqlite as sqlite
import nextcord
from main import bot as root
import psutil
import threading
# Статистика бота
@root.slash_command(name="status", description="Статус бота и сервера")
async def status(ctx: nextcord.Interaction):
    try:
        # Если участник не имеет админ-ролей
        if ctx.user.top_role.id not in [1242265397735067698, 1242267372052545576, 1242266974713544825]:
            await ctx.response.send_message("У вас нет прав для использования этой команды.")
            return

        warns = len(sqlite.cursor.execute('SELECT * FROM bot_warns;').fetchall())
        users = len(sqlite.cursor.execute('SELECT * FROM bot_users;').fetchall())
        bans = len(sqlite.cursor.execute('SELECT * FROM bot_bans;').fetchall())
        mutes = len(sqlite.cursor.execute('SELECT * FROM bot_mutes;').fetchall())
        sqlite.sql.commit()
        
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        embed = nextcord.Embed(
            title="Статистика базы данных",
            description=f"Записей в таблице варнов: `{warns}`\nЗаписей в таблице пользователей: `{users}`\nЗаписей в таблице банов: `{bans}`\nЗаписей в таблице мутов: `{mutes}`\nВсего записей: `{warns+users+bans+mutes}`\n*подробно получить БД с помощью команды /get_database*",
            color=0xA7A7D7
        )
        net_io = psutil.net_io_counters(pernic=True)  # Получаем статистику для каждого сетевого интерфейса
        # Выбираем интерфейс с наибольшей скоростью передачи данных
        max_speed_interface = max(net_io, key=lambda x: net_io[x].bytes_sent + net_io[x].bytes_recv)

        # Получаем скорость передачи и приема данных для выбранного интерфейса
        speed_sent = net_io[max_speed_interface].bytes_sent
        speed_recv = net_io[max_speed_interface].bytes_recv

        embed.add_field(name="Статистика хоста бота", value=f"Использовано ОЗУ: `{int(memory.used/1024/1024)}/{int(memory.total/1024/1024)}МБ`\nДоступно: `{int(memory.available/1024/1024)}МБ`\n")
        embed.add_field(name="- процессор", value=f"Нагрузка на процессор: `{cpu_percent}%`\nАктивные потоки: `{threading.active_count()}`")
        embed.add_field(name="- сеть", value=f"Отправлено: `{int(speed_sent / (1024 * 1024))}МБ`\nПринято: `{int(speed_recv / (1024 * 1024))}МБ`\n")
        embed.set_image(url="https://i.ibb.co/M7DtSqd/banner.png")
        await ctx.response.send_message(embed=embed)
        return
    except Exception as e:
        if not ctx.response.is_done():
            await ctx.response.send_message(f"Произошла ошибка: {str(e)}")
        else:
            await ctx.followup.send(f"Произошла ошибка: {str(e)}")
        return
