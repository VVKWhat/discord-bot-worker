import sqlite3
import datetime
import json
from typing import Any, Union, List
# Подключение к базе данных
def adapt_datetime(ts):
    return ts.strftime('%Y-%m-%d %H:%M:%S')
sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sql = sqlite3.connect("./assets/db/database.db", detect_types=sqlite3.PARSE_DECLTYPES)
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
    # id_ticket = channel id тикета 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_ticket INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot_tickets_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_ticket INTEGER NOT NULL, 
        user_id INTEGER NOT NULL,
        closed_admin_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        reason_close TEXT,
        history JSON NOT NULL,
        is_closed BOOLEAN,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        close_date TIMESTAMP NULL,
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
        is_bot BOOLEAN NOT NULL,
        UNIQUE(user_id, id)
    );
    """)
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_user_id ON bot_users(user_id);
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot_mutes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        admin_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expired TIMESTAMP,
        UNIQUE(user_id, id)
    );
    """)
    cursor.execute("""
    DELETE FROM bot_users
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM bot_users
        GROUP BY user_id
    );
    """)
    sql.commit()

async def add_user_to_database(user_id: int, is_bot: bool):
    cursor.execute("""
    INSERT OR IGNORE INTO bot_users (user_id, date, is_bot)
    VALUES (?, ?, ?)
    """, (user_id, datetime.datetime.now(), is_bot))
    sql.commit()

async def format_to_json(data: Union[dict, list, Any]) -> str:
    """
    Convert a Python object (dict, list, etc.) to a JSON string suitable for SQLite.

    Parameters:
    data (Union[dict, list, Any]): The data to convert to JSON format.

    Returns:
    str: JSON formatted string.
    """
    try:
        json_form = json.dumps(data)
        return json_form
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid data for JSON conversion: {e}")
    
def fetch_json(table: str, column: str) -> List[Any]:
    """
    Fetch JSON data from a specified column in a specified table.

    Parameters:
    table (str): The name of the table.
    column (str): The name of the column containing JSON data.

    Returns:
    List[Any]: A list of parsed JSON data.
    """
    try:
        query = f'SELECT {column} FROM {table}'
        cursor.execute(query)
        rows = cursor.fetchall()
        return [json.loads(row[0]) for row in rows]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return []