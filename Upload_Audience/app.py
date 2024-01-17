from ext import config
from ext.database_ext.create_tables import *
from ext.database_ext.list_audiences import *
from ext.formularios import LoginForm, AudiencesForm, CadastroUserForm
from ext.autentication import valid_user_login
from ext import database_operations
from flask import Flask, render_template, redirect, url_for, request, session
from blueprints import rest_api


#--------------------------------- Destinado para cenários de teste -----------------------------------------#
def minimal_app():
    app = Flask(__name__)
    config.init_app(app)
    return app

def create_app():
    app = minimal_app()
    rest_api.init_app(app)
    database_operations.init_app(app)
    create_table_audiences()
    create_table_sessions()
    return app
#--------------------------------- Destinado para cenários produtivos -----------------------------------------#

app = create_app()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/valid_user', methods=['POST', 'GET'])
def valid_user():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        return valid_user_login(form=form, user=request.form['user'], password=request.form['password'], session=session)
    else:
        return redirect(url_for('login'))

@app.route('/formulario', methods=['GET', 'POST'] )
def form_post():
    if 'session_id' in session:
        user_in_session = database_operations.execute('verify_session', user_id=session['user_id'], session_id=session['session_id'])
        if user_in_session:
            audience_form = AudiencesForm()
            return render_template('form_post.html', audience_form=audience_form)
    return redirect(url_for('login'))
    
@app.route('/send_data', methods=['POST'])
def send_data():
    if 'session_id' in session:
        user_in_session = database_operations.execute('verify_session', user_id=session['user_id'], session_id=session['session_id'])
        if user_in_session:
            audience_form = AudiencesForm(request.form)
            if audience_form.validate_on_submit():
                db_name = request.form['db_name']
                table_name = request.form['table_name']
                audience_name = request.form['audience_name']
                fornec = request.form['selector']
                return database_operations.execute('insert_audience', audience_form=audience_form, id_user_insert=session['user_id'], id_user_session=session['session_id'], db_name=db_name, table_name=table_name, audience_name=audience_name, fornec=fornec)

    return redirect(url_for('login'))
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'session_id' in session:
        user_in_session = database_operations.execute('verify_session', user_id=session['user_id'], session_id=session['session_id'])
        if user_in_session:
            form = CadastroUserForm()
            return render_template('create_users.html', form=form)
    return redirect(url_for('login'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if 'session_id' in session:
        user_in_session = database_operations.execute('verify_session', user_id=session['user_id'], session_id=session['session_id'])
        if user_in_session:
            form = CadastroUserForm(request.form)
            if form.validate_on_submit():
                username = request.form['user']
                return database_operations.execute('insert_user',username=username, password=request.form['password'])
            else:
                error_message = 'As senhas não coincidem. Por favor, verifique.'
                return render_template('create_users.html', form=form, error_message=error_message)
        return redirect(url_for('login'))

    return redirect(url_for('login'))

@app.route('/list_audiences')
def list_audiences():
    if 'session_id' in session:
        user_in_session = database_operations.execute('verify_session', user_id=session['user_id'], session_id=session['session_id'])
        if user_in_session:
            audiences = list_existing_audiences()
            return render_template('list_audiences.html',audiences=audiences)
    return redirect(url_for('login'))

@app.route('/delete_audience/<int:audience_id>', methods=['DELETE'])
def delete_audience(audience_id):
    if 'session_id' in session:
        user_in_session = database_operations.execute('verify_session', user_id=session['user_id'], session_id=session['session_id'])
        if user_in_session:
            return database_operations.execute('delete_audience', audience_id=audience_id)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'session_id' in session:
        user_in_session = database_operations.execute('verify_session', user_id=session['user_id'], session_id=session['session_id'])
        if user_in_session:
            database_operations.execute('remove_session', session=session)

            # Destroi a sessão
            session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)