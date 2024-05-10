from ext.formularios import LoginForm, AudiencesForm, CadastroUserForm, SalesforceForm
from ext.autentication import valid_user_login
from ext import database_operations
from flask import render_template, redirect, url_for, request, session
from flask_wtf.csrf import generate_csrf
from ext.database_ext.list_audiences import *
from ext.database_ext.create_tables import *
from app import app

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

# ROTA DE PROCESSAMENTO DE INFORMAÇÕES DO LOGIN 
@app.route('/auth', methods=['POST'])
def valid_user():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        return valid_user_login(form=form, user=request.form['user'], password=request.form['password'], session=session)
    else:
        return redirect(url_for('login'))

@app.route('/form/<user>', methods=['GET'])
def form_post(user):
    if session.get(f'user_{user}_name'):
        audience_form = AudiencesForm()
        salesforce_form = SalesforceForm()
        return render_template('form_post.html', user=user, audience_form=audience_form, salesforce_form=salesforce_form)
    else:
        return redirect(url_for('login'))

# ROTA DE PROCESSAMENTO DE INFORMAÇÕES DO FORMULÁRIO
@app.route('/send_data/<user>', methods=['POST'])
def send_data(user):
    if session.get(f'user_{user}_name'): 
        audience_form = AudiencesForm(request.form)
        salesforce_form = SalesforceForm(request.form)
        partner = request.form.get('parceiro')

        if partner == 'Tiktok':
            if audience_form.validate_on_submit():
                return database_operations.execute('insert_audience', user=user, audience_form=audience_form, salesforce_form=salesforce_form, id_user_insert=session[f'{user}_user_id'], db_name=request.form['db_name'], table_name=request.form['table_name'], audience_name=request.form['audience_name'], parceiro=request.form['parceiro'], advertiser_name=request.form['advertiser_name'])
            
        elif partner == 'Salesforce':
            if salesforce_form.validate_on_submit():
                return database_operations.execute('insert_audience', user=user, audience_form=audience_form, salesforce_form=salesforce_form, id_user_insert=session[f'{user}_user_id'], db_name=request.form['db_name_sf'], table_name=request.form['table_name_sf'], file_name=request.form['file_name'], sftp_path=request.form['sftp_path'], parceiro=request.form['parceiro'])
        
        return redirect(url_for('form_post'))

    return redirect(url_for('login'))
    
@app.route('/signup/<user>', methods=['GET'])
def signup(user):
    if session.get(f'user_{user}_name'): 
        form = CadastroUserForm()
        return render_template('create_users.html', user=user, form=form)
    return redirect(url_for('login'))

# ROTA DE PROCESSAMENTO DE INFORMAÇÕES DA CRIAÇÃO DE USUÁRIO
@app.route('/create_user/<user>', methods=['POST'])
def create_user(user):
    if session.get(f'user_{user}_name'): 
        form = CadastroUserForm(request.form)
        if form.validate_on_submit():
            return database_operations.execute('insert_user', user=user, username=request.form['user'], password=request.form['password'])
        else:
            error_message = 'As senhas não coincidem. Por favor, verifique.'
            return render_template('create_users.html', user=user, form=form, error_message=error_message)
        
    return redirect(url_for('login'))

@app.route('/list_audiences/<user>', methods=['GET'])
def list_audiences(user):
    if session.get(f'user_{user}_name'): 
        audiences = list_existing_audiences()
        audiences_sf = list_existing_audiences_salesforce()
        csrf_token = generate_csrf()
        return render_template('list_audiences.html', user=user, audiences=audiences, audiences_sf=audiences_sf, csrf_token=csrf_token)
    return redirect(url_for('login'))

# ROTA DE PROCESSAMENTO DE INFORMAÇÕES DA EXCLUSÃO DE AUDIÊNCIAS
@app.route('/delete_audience/<user>/<int:audience_id>/<parceiro>', methods=['DELETE'])
def delete_audience(user, audience_id, parceiro):
    if session.get(f'user_{user}_name'): 
        return database_operations.execute('delete_audience', audience_id=audience_id, parceiro=parceiro)
    else:
        return redirect(url_for('login'))

@app.route('/logout/<user>', methods=['GET'])
def logout(user):
    if session.get(f'user_{user}_name'): 
        session.clear()
    return redirect(url_for('login'))