import sqlite3
from ext.database_operations import TABLE_AUDIENCES
from collections import namedtuple

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
            
def list_item_existing_audiences(**kwargs):
    from ext.database_operations import DATABASE
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(f"SELECT * FROM {TABLE_AUDIENCES} WHERE id = ?", (kwargs['id_audience'],))
            list_tuple_audiences = cursor.fetchall()
            MinhaClasse = namedtuple('Audiences', ['id','id_user_insert', 'id_user_session', 'db_name', 'table_name', 'audience_name', 'fornec'])
            audiences = [MinhaClasse(*tupla) for tupla in list_tuple_audiences]
            return audiences
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)
            
