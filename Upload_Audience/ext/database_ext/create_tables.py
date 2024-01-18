import sqlite3
from collections import namedtuple
from ext.database_operations import TABLE_AUDIENCES, TABLE_USERS, TABLE_SESSIONS

def create_table_audiences():
    from ext.database_operations import DATABASE
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
                    fornec TEXT
                    usuario_id INTEGER,
                    FOREIGN KEY (id_user_insert) REFERENCES {TABLE_USERS}(id)
                )
            ''')
            return True
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)

def create_table_login():
    from ext.database_operations import DATABASE
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

def create_table_sessions():
    from ext.database_operations import DATABASE
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

def list_existing_audiences():
    from ext.database_operations import DATABASE
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(f'''SELECT * FROM {TABLE_AUDIENCES}''')
            list_tuple_audiences = cursor.fetchall()
            MinhaClasse = namedtuple('Audiences', ['id','id_user_insert', 'id_user_session', 'db_name', 'table_name', 'audience_name', 'fornec'])
            audiences = [MinhaClasse(*tupla) for tupla in list_tuple_audiences]
            return audiences
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)