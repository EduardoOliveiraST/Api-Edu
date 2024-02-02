import sqlite3
from ext.config import TABLE_AUDIENCES, TABLE_USERS, TABLE_SESSIONS

def create_table_audiences(DATABASE):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_AUDIENCES} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_user_insert INTEGER,
                    id_user_session TEXT,
                    db_name TEXT,
                    table_name TEXT,
                    audience_name TEXT,
                    parceiro TEXT,
                    advertiser_name TEXT,
                    FOREIGN KEY (id_user_insert) REFERENCES {TABLE_USERS}(id)
                )
            ''')
            return True
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)

def create_table_login(DATABASE):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT,
                    password TEXT
                )
            ''')
            return True
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)

def create_table_sessions(DATABASE):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {TABLE_SESSIONS} (
                    id_user INTEGER,
                    id_user_session TEXT,
                    FOREIGN KEY (id_user) REFERENCES {TABLE_USERS}(id)
                )
            ''')
            return True
    
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)