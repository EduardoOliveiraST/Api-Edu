import sqlite3
from secrets import token_urlsafe
from flask import redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash
from ext.database_operations import execute
from ext.config import TABLE_USERS, TABLE_SESSIONS, DATABASE

def valid_user_login(**kwargs):
    form = kwargs['form']
    password = kwargs['password']
    session = kwargs['session']
    user = kwargs['user']

    with sqlite3.connect(DATABASE) as conn:
        try:
            cursor = conn.cursor()
            consulta = f'SELECT * FROM {TABLE_USERS} WHERE user = ?'

            cursor.execute(consulta, (user,))

            existing_entry = cursor.fetchone()

            if existing_entry:
                session_id = token_urlsafe(16)
                user_id, password_encrypted_database = existing_entry[0], existing_entry[2]
                in_session = execute('verify_session', user_id=user_id, session_id=session_id)

                if not in_session:
                    if check_password_hash(password_encrypted_database, password):
                        # Armazenar o token na sessão
                        session['session_id'] = session_id
                        session['user_id'] = user_id

                        try:
                            cursor.execute("BEGIN")
                            consulta = f'INSERT INTO {TABLE_SESSIONS} (id_user, id_user_session) VALUES (?, ?)'
                            cursor.execute(consulta, (user_id, session_id,))
                            cursor.execute("COMMIT")
                        except sqlite3.Error as e:
                            print(f"Erro durante a transação: {e}")
                            conn.rollback()

                        return redirect(url_for('form_post'))
                    else:
                        flash('Usuário ou senha incorretos. Revise os parâmetros!', 'error')
                        return render_template('login.html', form=form)
                else:
                    flash('O usuário está logado!', 'warning')
                    return render_template('login.html', form=form)
            else:
                flash('Usuário inexistente.', 'error')
                return render_template('login.html', form=form)
        except sqlite3.Error as e:
            print(f"Erro durante a transação: {e}")
            conn.rollback()
