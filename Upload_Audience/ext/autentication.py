import sqlite3
from secrets import token_urlsafe
from flask import redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash
from ext.config import TABLE_USERS, DATABASE

def valid_user_login(**kwargs):

    session = kwargs['session']
    user = kwargs['user']
    password = kwargs['password']

    with sqlite3.connect(DATABASE) as conn:
        try:
            cursor = conn.cursor()
            consulta = f'SELECT * FROM {TABLE_USERS} WHERE user = ?'
            cursor.execute(consulta, (user,))
            existing_entry = cursor.fetchone()
            # Se usuário existe
            if existing_entry:

                if session.get(f'user_{user}_logged_in'):  # Verifica se está logado
                    flash('O usuário está logado!', 'warning')
                    return render_template('login.html', form=kwargs['form'])
                else:

                    user_id, password_encrypted_database = existing_entry[0], existing_entry[2]
                    if check_password_hash(password_encrypted_database, password):
                        session[f'user_{user}_logged_in'] = True
                        session[f'user_{user}_name'] = user
                        session[f'{user}_user_id'] = user_id
                
                        return redirect(url_for('form_post', user=user))
                    else:
                        flash('Usuário ou senha incorretos. Revise os parâmetros!', 'error')
                        return render_template('login.html', form=kwargs['form'])
            else:
                flash('Usuário inexistente.', 'error')
                return render_template('login.html', form=kwargs['form'])
                
        except sqlite3.Error as e:
            print(f"Erro durante a transação: {e}")
            conn.rollback()