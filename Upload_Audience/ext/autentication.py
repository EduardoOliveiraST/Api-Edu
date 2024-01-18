import sqlite3
from secrets import token_urlsafe
from flask import redirect, url_for, render_template
from werkzeug.security import check_password_hash
from ext.database_operations import execute, TABLE_USERS, TABLE_SESSIONS



def valid_user_login(**kwargs):
    from ext.database_operations import DATABASE
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        """Função que verifica no banco de dados se o usuário e senha existem e se estão corretos.
        Se existir, obtém o ID do banco, usuário, senha criptografada do banco

        1 - A senha do banco de dados será utilizada para a validação do usuário
        2 - O ID é utilizado junto a um token hexadecimal que está definido como sesion_id, para conseguirmos mensurar o fluxo de operações dentro de uma ou várias sessões na WEB, então conseguimos verificar quantas operações o usuário fez em uma única sessão aberta.
        """

        form = kwargs['form']
        password = kwargs['password']
        session = kwargs['session']
        user = kwargs['user']

        cursor.execute(f'''
            SELECT * FROM {TABLE_USERS}
            WHERE user = ?
        ''', (user,))

        existing_entry = cursor.fetchone() # Verifica se existe o nome do usuário no banco.

        if existing_entry:
            session_id = token_urlsafe(16)
            user_id, password_encrypted_database = existing_entry[0], existing_entry[2]
            in_session = execute('verify_session',user_id=user_id, session_id=session_id)

            if not in_session:

                if check_password_hash(password_encrypted_database, password):
                    # Armazenar o token na sessão
                    session['session_id'] = session_id
                    session['user_id'] = user_id

                    cursor.execute(f'''
                        INSERT INTO {TABLE_SESSIONS} (id_user, id_user_session)
                        VALUES (?, ?)
                        ''', (user_id, session_id,))

                    return redirect(url_for('form_post'))
                else:
                    return render_template('login.html', form=form, error_message='Usuário ou senha incorretos. Revise os parâmetros!')
                
            else:
                return render_template('login.html', form=form, error_message='O usuário está logado!')
            
        return render_template('login.html', form=form, error_message='Usuário inexistente.')