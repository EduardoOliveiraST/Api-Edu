import sqlite3
from flask import render_template,jsonify
from werkzeug.security import generate_password_hash

DATABASE = ''
TABLE_AUDIENCES = 'tb_upload_audiences_ecs_marketing'
TABLE_USERS = 'tb_login'
TABLE_SESSIONS = 'tb_sessions'


def init_app(app):
    global DATABASE
    DATABASE = app.dynaconf.SQLALCHEMY_DATABASE_URI

def execute(func,**kwargs):
    
    def verify_session(**kwargs):
        try:
            cursor.execute(f'''
                SELECT * FROM {TABLE_SESSIONS}
                WHERE id_user = ? or id_user_session = ?''',
                (kwargs['user_id'],kwargs['session_id'],))

            existing_entry = cursor.fetchall()

            if existing_entry:
                return True
            else:
                return False
            
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)
    
    def remove_session(**kwargs):
        try:
            cursor.execute(f'''
                SELECT * FROM {TABLE_SESSIONS}
                WHERE id_user_session = ?
            ''', (kwargs['session']["session_id"],))

            existing_entry = cursor.fetchall()

            if existing_entry:
                cursor.execute(f'''
                    DELETE FROM {TABLE_SESSIONS}
                    WHERE id_user_session = ?
                    ''', (kwargs['session']["session_id"],))
                return True
            
            return False
        
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)        
    
    def insert_user(**kwargs): 
        cursor.execute(f'''SELECT * FROM {TABLE_USERS} WHERE user = ?''', (kwargs['username'],))    
        existing_entry = cursor.fetchone()  

        if existing_entry:
            return render_template('existing_users.html', user=kwargs['username'])

        cursor.execute(f'''
            INSERT INTO {TABLE_USERS} (user, password)
            VALUES (?, ?)
        ''', (kwargs['username'], generate_password_hash(kwargs['password']),)) 

        return render_template('informacoes_created_user.html', user=kwargs['username'])
    
    def delete_audience(**kwargs):
        try:
            cursor.execute(f"DELETE FROM {TABLE_AUDIENCES} WHERE id = ?", (kwargs['audience_id'],))
            return jsonify({'success': True, 'message': 'Audiência excluída com sucesso'})
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Erro ao excluir a audiência: {str(e)}'})

    def insert_audience(**kwargs):
        cursor.execute(f'''
            SELECT * FROM {TABLE_AUDIENCES}
            WHERE audience_name = ?  AND fornec = ?
        ''', (kwargs['audience_name'], kwargs['fornec'],))

        exists = bool(cursor.fetchone())
        if exists:
            return render_template('form_post.html', audience_form=kwargs['audience_form'], error_message=f'[ERROR] Audiência {kwargs["audience_name"]} já é existente.')

        cursor.execute(f'''
            INSERT INTO {TABLE_AUDIENCES} (id_user_insert, id_user_session, db_name, table_name, audience_name, fornec)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (kwargs['id_user_insert'], kwargs['id_user_session'], kwargs['db_name'], kwargs['table_name'], kwargs['audience_name'], kwargs['fornec'],))

        success_message = 'Audiência criada com êxito.'
        return render_template('form_post.html', audience_form=kwargs['audience_form'], success_message=success_message)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        return locals()[func](**kwargs)