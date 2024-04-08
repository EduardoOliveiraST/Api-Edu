import sqlite3
from flask import render_template,jsonify
from werkzeug.security import generate_password_hash
from ext.config import TABLE_AUDIENCES, TABLE_USERS, TABLE_SALES_FORCE, DATABASE
from ext.database_ext.create_tables import *
import os
import pandas as pd

create_table_login(DATABASE)
create_table_audiences(DATABASE)
create_table_salesforce(DATABASE)


def table_and_database_exists(cursor_principal, **kwargs):

    def insert():
        try:
            if kwargs['parceiro'] == 'Tiktok':
                cursor_principal.execute("BEGIN")
                query = f'INSERT INTO {TABLE_AUDIENCES} (id_user_insert, db_name, table_name, audience_name, parceiro, advertiser_name) VALUES (?, ?, ?, ?, ?, ?)'
                cursor_principal.execute(query,(kwargs['id_user_insert'], kwargs['db_name'], kwargs['table_name'], kwargs['audience_name'], kwargs['parceiro'], kwargs['advertiser_name'],))
                cursor_principal.execute("COMMIT")


            elif kwargs['parceiro'] == 'Salesforce':
                cursor_principal.execute("BEGIN")
                query = f'INSERT INTO {TABLE_SALES_FORCE} (id_user_insert, db_name, table_name, file_name, parceiro, sftp_path) VALUES (?, ?, ?, ?, ?, ?)'
                cursor_principal.execute(query,(kwargs['id_user_insert'], kwargs['db_name'], kwargs['table_name'], kwargs['file_name'], kwargs['parceiro'], kwargs['sftp_path'],))
                cursor_principal.execute("COMMIT")
            
            success_message = f'Audiência para o {kwargs["parceiro"]} criada com êxito.'
            return render_template('form_post.html', user=kwargs['user'], audience_form=kwargs['audience_form'], salesforce_form=kwargs['salesforce_form'], success_message=success_message)
            
        except sqlite3.Error as e:
            cursor_principal.rollback()
            print("Erro:", e)
    """
    Operação central para verificar se o banco de dados e tabela inseridos pelo usuário no cadastro de audiências são existentes no lake (atualmente SQLITE3)
    Aqui é possível barrar esse erro de inserção por parte do usuário.

    Audiências que passam por esse endpoint, foram verificadas pela função insert_audience() e por javaScript no template form_post, garantindo que a requisição de audiência só seja criada se o banco e tabela existirem.

    """
    return insert()
    # file_name = 'list_existing_databases.csv' # Esse arquivo precisa existir e estar populado (Operação manual de inserção)
    # file_databases_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + f'/{file_name}' if os.name == "posix" else os.path.dirname(os.path.realpath(__file__)) + f'\\{file_name}'
    # df = pd.read_csv(file_databases_path, sep=';')
    # df['joined_column'] = df['database'].astype(str) +'.'+ df['table_name'].astype(str) # Esse campo não pode ser formatado com f-string, comportamento muda. Concatenação de valores foi utilizado, não formatação.

    # if kwargs["db_name"] in df['database'].values and kwargs["table_name"] in df['table_name'].values:
    #     if kwargs["db_name"] + '.' + kwargs["table_name"] in df['joined_column'].values:
    #         return insert()
    #     else:
    #         error_message = '[ERROR] Combinação entre banco de dados e tabela não existe.'
    
    # elif kwargs["db_name"] not in df['database'].values:
    #     error_message = '[ERROR] O banco de dados não existe.'
        
    # elif kwargs["table_name"] not in df['table_name'].values:
    #     error_message = '[ERROR] Tabela não existe.'

    # if error_message:
    #     return render_template('form_post.html', user=kwargs['user'], audience_form=kwargs['audience_form'], salesforce_form=kwargs['salesforce_form'], error_message=error_message)
            

def execute(func, **kwargs):    
    
    def insert_user(**kwargs): 
        try:
            query = f'SELECT * FROM {TABLE_USERS} WHERE user = ?'
            cursor.execute(query, (kwargs['username'],))    
            existing_entry = cursor.fetchone()  

            if existing_entry:
                return render_template('existing_users.html',user=kwargs['user'], username=kwargs['username'])
            
            cursor.execute("BEGIN")
            query = f'INSERT INTO {TABLE_USERS} (user, password) VALUES (?, ?)'
            cursor.execute(query, (kwargs['username'], generate_password_hash(kwargs['password']),)) 
            cursor.execute("COMMIT")

            return render_template('informacoes_created_user.html', user=kwargs['user'], username=kwargs['username'])
        except sqlite3.Error as e:
            conn.rollback()
            print("Erro:", e)    
    
    def delete_audience(**kwargs):
        try:
            if kwargs['parceiro'] == 'Tiktok':
                cursor.execute("BEGIN")
                query = f'DELETE FROM {TABLE_AUDIENCES} WHERE id = ?'
                cursor.execute(query, (kwargs['audience_id'],))
                cursor.execute("COMMIT")
                return jsonify({'success': True, 'message': 'Audiência excluída com sucesso'})
            
            elif kwargs['parceiro'] == 'Salesforce':
                cursor.execute("BEGIN")
                query = f'DELETE FROM {TABLE_SALES_FORCE} WHERE id = ?'
                cursor.execute(query, (kwargs['audience_id'],))
                cursor.execute("COMMIT")
                return jsonify({'success': True, 'message': 'Audiência excluída com sucesso'})
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Erro ao excluir a audiência: {str(e)}'})

    def insert_audience(**kwargs):
        if kwargs['parceiro'] == 'Tiktok':
            query = f'SELECT * FROM {TABLE_AUDIENCES} WHERE audience_name = ?  AND parceiro = ?'
            cursor.execute(query, (kwargs['audience_name'], kwargs['parceiro'],))

            exists = bool(cursor.fetchone())
            if exists:
                return render_template('form_post.html', user=kwargs['user'], audience_form=kwargs['audience_form'], salesforce_form=kwargs['salesforce_form'], error_message=f'[ERROR] Audiência {kwargs["audience_name"]} já é existente.')
        
        
        elif kwargs['parceiro'] == 'Salesforce':
            query = f'SELECT * FROM {TABLE_SALES_FORCE} WHERE file_name = ?  AND parceiro = ?'
            cursor.execute(query, (kwargs['file_name'], kwargs['parceiro'],))

            exists = bool(cursor.fetchone())
            if exists:
                return render_template('form_post.html', user=kwargs['user'], audience_form=kwargs['audience_form'], salesforce_form=kwargs['salesforce_form'], error_message=f'[ERROR] Audiência {kwargs["audience_name"]} já é existente.')
        
        return table_and_database_exists(cursor, **kwargs)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        return locals()[func](**kwargs)