import sqlite3
from ext.config import TABLE_AUDIENCES, TABLE_SALES_FORCE, DATABASE
from collections import namedtuple

def list_existing_audiences():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(f'''SELECT * FROM {TABLE_AUDIENCES}''')
            list_tuple_audiences = cursor.fetchall()
            MinhaClasse = namedtuple('Audiences', ['id','id_user_insert', 'db_name', 'table_name', 'audience_name', 'parceiro', 'advertiser_name'])
            audiences = [MinhaClasse(*tupla) for tupla in list_tuple_audiences]
            return audiences
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)

def list_existing_audiences_salesforce():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(f'''SELECT * FROM {TABLE_SALES_FORCE}''')
            list_tuple_audiences = cursor.fetchall()
            MinhaClasse = namedtuple('Audiences', ['id','id_user_insert', 'db_name_sf', 'table_name_sf', 'file_name', 'parceiro', 'sftp_path'])
            audiences = [MinhaClasse(*tupla) for tupla in list_tuple_audiences]
            return audiences
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)
            
def list_item_existing_audiences(**kwargs):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(f"SELECT * FROM {TABLE_AUDIENCES} WHERE id = ?", (kwargs['id_audience'],))
            list_tuple_audiences = cursor.fetchall()
            MinhaClasse = namedtuple('Audiences', ['id','id_user_insert', 'id_user_session', 'db_name', 'table_name', 'audience_name', 'parceiro', 'advertiser_name'])
            audiences = [MinhaClasse(*tupla) for tupla in list_tuple_audiences]
            return audiences
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)
            
