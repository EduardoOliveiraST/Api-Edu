import sqlite3
from flask import render_template,jsonify
from werkzeug.security import generate_password_hash
from ext.config import TABLE_AUDIENCES, TABLE_SESSIONS, TABLE_USERS, DATABASE
from ext.database_ext.create_tables import *
import os

create_table_audiences(DATABASE)
create_table_sessions(DATABASE)
create_table_login(DATABASE)

def table_and_database_exists(cursor_principal, **kwargs):

    """
    Operação central para verificar se o banco de dados e tabela inseridos pelo usuário no cadastro de audiências são existentes no lake (atualmente SQLITE3)
    Aqui é possível barrar esse erro de inserção por parte do usuário.

    Audiências que passam por esse endpoint, foram verificadas pela função insert_audience() e por javaScript no template form_post, garantindo que a requisição de audiência só seja criada se o banco e tabela existirem.

    """
    
    databases_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "databases/").replace("\\", "/") if os.name == "posix" else os.path.join(os.path.dirname(os.path.realpath(__file__)), "databases\\")
    try:
        database_dir = databases_dir + kwargs["db_name"] + '.db'
        if os.path.exists(database_dir): # Se database existe
            with sqlite3.connect(database_dir) as conn:
                cursor = conn.cursor()
                query = f"SELECT * FROM {kwargs['table_name']}"
                cursor.execute(query)
                existing_entry = bool(cursor.fetchone())

            if existing_entry: # Se tabela existe
                try:
                    cursor_principal.execute("BEGIN")
                    query = f'INSERT INTO {TABLE_AUDIENCES} (id_user_insert, id_user_session, db_name, table_name, audience_name, fornec)VALUES (?, ?, ?, ?, ?, ?)'
                    cursor_principal.execute(query,(kwargs['id_user_insert'], kwargs['id_user_session'], kwargs['db_name'], kwargs['table_name'], kwargs['audience_name'], kwargs['fornec'],))
                    cursor_principal.execute("COMMIT")

                    success_message = 'Audiência criada com êxito.'
                    return render_template('form_post.html', audience_form=kwargs['audience_form'], success_message=success_message)
                except sqlite3.Error as e:
                    cursor_principal.rollback()
                    print("Erro:", e)
    

        else:
            return render_template('form_post.html', audience_form=kwargs['audience_form'], error_message=f'[ERROR] O banco de dados {kwargs["db_name"]} não existente.')

    except Exception as e:
            if 'no such table' in e.args[0]:
                return render_template('form_post.html', audience_form=kwargs['audience_form'], error_message=f'[ERROR] A tabela {kwargs["table_name"]} não existe.')
            
            
def verify_session(**kwargs):

    """
    Todo endpoint passa por aqui, antes de qualquer chamada em qualquer endpoit essa função é chamada, para garantir que o usuário já realizou o login, e está manipulando os endpoints a partir desse login 
    
    """


    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            query = f'SELECT * FROM {TABLE_SESSIONS} WHERE id_user = ? or id_user_session = ?'
            cursor.execute(query, (kwargs['user_id'],kwargs['session_id'],))
        
        existing_entry = cursor.fetchall()

        if existing_entry:
            return True
        else:
            return False
        
    except sqlite3.Error as e:
        conn.rollback()
        print("Erro:", e)

def execute(func, **kwargs):
    
    def remove_session(**kwargs):
        try:
            query = f'SELECT * FROM {TABLE_SESSIONS} WHERE id_user_session = ?'
            cursor.execute(query, (kwargs['session']["session_id"],))

            existing_entry = cursor.fetchall()

            if existing_entry:
                cursor.execute("BEGIN")
                query = f'DELETE FROM {TABLE_SESSIONS} WHERE id_user_session = ?'
                cursor.execute("COMMIT")
                cursor.execute(query, (kwargs['session']["session_id"],))
                return True
            
            return False
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)        
    
    def insert_user(**kwargs): 
        try:
            query = f'SELECT * FROM {TABLE_USERS} WHERE user = ?'
            cursor.execute(query, (kwargs['username'],))    
            existing_entry = cursor.fetchone()  

            if existing_entry:
                return render_template('existing_users.html', user=kwargs['username'])
            
            cursor.execute("BEGIN")
            query = f'INSERT INTO {TABLE_USERS} (user, password) VALUES (?, ?)'
            cursor.execute(query, (kwargs['username'], generate_password_hash(kwargs['password']),)) 
            cursor.execute("COMMIT")

            return render_template('informacoes_created_user.html', user=kwargs['username'])
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)    
    
    def delete_audience(**kwargs):
        try:
            cursor.execute("BEGIN")
            query = f'DELETE FROM {TABLE_AUDIENCES} WHERE id = ?'
            cursor.execute(query, (kwargs['audience_id'],))
            cursor.execute("COMMIT")
            return jsonify({'success': True, 'message': 'Audiência excluída com sucesso'})
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Erro ao excluir a audiência: {str(e)}'})

    def insert_audience(**kwargs):
        query = f'SELECT * FROM {TABLE_AUDIENCES} WHERE audience_name = ?  AND fornec = ?'
        cursor.execute(query, (kwargs['audience_name'], kwargs['fornec'],))

        exists = bool(cursor.fetchone())
        if exists:
            return render_template('form_post.html', audience_form=kwargs['audience_form'], error_message=f'[ERROR] Audiência {kwargs["audience_name"]} já é existente.')
        
        return table_and_database_exists(cursor, **kwargs)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        return locals()[func](**kwargs)