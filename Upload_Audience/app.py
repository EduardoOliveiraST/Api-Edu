from ext import config
from ext.database_ext.create_tables import *
from ext.database_ext.list_audiences import *
from ext.formularios import LoginForm, AudiencesForm, CadastroUserForm
from ext.autentication import valid_user_login
from ext import database_operations
from flask import Flask, render_template, redirect, url_for, request, session
from blueprints import rest_api
from flask_wtf.csrf import CSRFProtect, generate_csrf
import os

def validate_session():
    if 'session_id' in session:
        user_in_session = database_operations.execute('verify_session', user_id=session['user_id'], session_id=session['session_id'])
        if user_in_session:
            return True
        return False

#--------------------------------- Destinado para cenários de teste -----------------------------------------#
def minimal_app():
    app = Flask(__name__)
    config.init_app(app)
    return app

def create_app():
    app = minimal_app()
    rest_api.init_app(app)
    return app
#--------------------------------- Destinado para cenários produtivos -----------------------------------------#

app = create_app()
csrf = CSRFProtect(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/valid_user', methods=['POST'])
def valid_user():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        return valid_user_login(form=form, user=request.form['user'], password=request.form['password'], session=session)
    else:
        return redirect(url_for('login'))

@app.route('/formulario', methods=['GET'] )
def form_post():
    in_session = validate_session()
    if in_session: 
        audience_form = AudiencesForm()
        return render_template('form_post.html', audience_form=audience_form)
    return redirect(url_for('login'))
    
@app.route('/send_data', methods=['POST'])
def send_data():
    in_session = validate_session()
    if in_session: 
        audience_form = AudiencesForm(request.form)
        if audience_form.validate_on_submit():
            return database_operations.execute('insert_audience', audience_form=audience_form, id_user_insert=session['user_id'], id_user_session=session['session_id'], db_name=request.form['db_name'], table_name=request.form['table_name'], audience_name=request.form['audience_name'], fornec=request.form['selector'])
        
        return redirect(url_for('login'))

    return redirect(url_for('login'))
    
@app.route('/signup', methods=['GET'])
def signup():
    in_session = validate_session()
    if in_session: 
        form = CadastroUserForm()
        return render_template('create_users.html', form=form)
    return redirect(url_for('login'))

@app.route('/create_user', methods=['POST'])
def create_user():
    in_session = validate_session()
    if in_session: 
        form = CadastroUserForm(request.form)
        if form.validate_on_submit():
            return database_operations.execute('insert_user', username=request.form['user'], password=request.form['password'])
        else:
            error_message = 'As senhas não coincidem. Por favor, verifique.'
            return render_template('create_users.html', form=form, error_message=error_message)
        
    return redirect(url_for('login'))

@app.route('/list_audiences', methods=['GET'])
def list_audiences():
    in_session = validate_session()
    if in_session: 
        audiences = list_existing_audiences()
        csrf_token = generate_csrf()
        return render_template('list_audiences.html',audiences=audiences, csrf_token=csrf_token)
    return redirect(url_for('login'))

@app.route('/delete_audience/<int:audience_id>', methods=['DELETE'])
def delete_audience(audience_id):
    in_session = validate_session()
    if in_session: 
        return database_operations.execute('delete_audience', audience_id=audience_id)
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    in_session = validate_session()
    if in_session: 
        database_operations.execute('remove_session', session=session)
        session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)