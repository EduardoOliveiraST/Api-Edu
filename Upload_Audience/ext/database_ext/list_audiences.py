import sqlite3
from ext.config import TABLE_AUDIENCES, TABLE_SALES_FORCE, DATABASE
from collections import namedtuple

def list_existing_audiences(audienceid=False, processed_audiences = False):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        try:
            query = f'''SELECT * FROM {TABLE_AUDIENCES} WHERE audience_processed = 0''' if not audienceid else f'''SELECT * FROM {TABLE_AUDIENCES} WHERE id = ? and audience_processed = 0'''
            query = query.replace('=', '<>') if processed_audiences else query
            cursor.execute(query) if not audienceid else cursor.execute(query,(audienceid,))
            list_tuple_audiences = cursor.fetchall()
            MinhaClasse = namedtuple('Audiences', ['id','id_user_insert', 'db_name', 'table_name', 'audience_name', 'parceiro', 'advertiser_name', 'created_by', 'audience_processed'])
            audiences = [MinhaClasse(*tupla) for tupla in list_tuple_audiences]
            return audiences
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)

def list_existing_audiences_salesforce(audienceid=False, processed_audiences = False):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        try:
            query = f'''SELECT * FROM {TABLE_SALES_FORCE} WHERE audience_processed = 0''' if not audienceid else f'''SELECT * FROM {TABLE_SALES_FORCE} WHERE id = ? AND audience_processed = 0'''
            query = query.replace('=', '<>') if processed_audiences else query
            cursor.execute(query) if not audienceid else cursor.execute(query,(audienceid,))
            list_tuple_audiences = cursor.fetchall()
            MinhaClasse = namedtuple('Audiences', ['id','id_user_insert', 'db_name_sf', 'table_name_sf', 'file_name', 'parceiro', 'sftp_path', 'created_by', 'audience_processed'])
            audiences = [MinhaClasse(*tupla) for tupla in list_tuple_audiences]
            return audiences
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)   
