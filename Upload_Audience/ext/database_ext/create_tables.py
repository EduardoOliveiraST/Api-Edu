import sqlite3
from ext.config import TABLE_AUDIENCES, TABLE_USERS, TABLE_SALES_FORCE

def create_table_audiences(DATABASE):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_AUDIENCES} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_user_insert INTEGER,
                    db_name TEXT,
                    table_name TEXT,
                    audience_name TEXT,
                    parceiro TEXT,
                    advertiser_name TEXT,
                    created_by TEXT,
                    audience_processed INTEGER CHECK (audience_processed IN (0, 1)),
                    FOREIGN KEY (id_user_insert) REFERENCES {TABLE_USERS}(id)
                )
            ''')
            return True
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)

def create_table_salesforce(DATABASE):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {TABLE_SALES_FORCE} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_user_insert INTEGER,
                    db_name TEXT,
                    table_name TEXT,
                    file_name TEXT,
                    parceiro TEXT,
                    sftp_path TEXT,
                    created_by TEXT,
                    audience_processed INTEGER CHECK (audience_processed IN (0, 1)),
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