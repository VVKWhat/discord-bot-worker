import sqlite3
import datetime
# Подключение к базе данных
def adapt_datetime(ts):
    return ts.strftime('%Y-%m-%d %H:%M:%S')
sqlite3.register_adapter(datetime.datetime, adapt_datetime)
file = open('./database.db','+a')
file.close()
sql = sqlite3.connect("./database.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = sql.cursor()
async def create_database():
    global sql,cursor
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot_warns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expired_days INT,
        UNIQUE(user_id, id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot_bans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        admin_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expired TIMESTAMP,
        appelation BOOLEAN,
        UNIQUE(user_id, id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot_invites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        invite_code TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expired TIMESTAMP,
        count BOOLEAN,
        UNIQUE(user_id, id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        invite_id INTEGER NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, id)
    );
    """)
    sql.commit()
