from ext.formularios import LoginForm, AudiencesForm, CadastroUserForm, SalesforceForm
from ext.autentication import valid_user_login
from ext import database_operations
from flask import render_template, redirect, url_for, request, session, flash
from flask_wtf.csrf import generate_csrf
from ext.database_ext.list_audiences import *
from ext.database_ext.create_tables import *
from functools import wraps
from app import app

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user = kwargs.get('user')  # Obtém o nome de usuário da rota
        if not session.get(f'user_{user}_name'):
            flash('Você precisa estar logado para acessar esta página.', 'error')
            return redirect(url_for('login'))  # Redireciona para a página de login
        return view_func(*args, **kwargs)
    return wrapper

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
@login_required
def form_post(user):
    audience_form = AudiencesForm()
    salesforce_form = SalesforceForm()
    return render_template('form_post.html', user=user, audience_form=audience_form, salesforce_form=salesforce_form)

# ROTA DE PROCESSAMENTO DE INFORMAÇÕES DO FORMULÁRIO
@app.route('/send_data/<user>', methods=['POST'])
@login_required
def send_data(user):
    audience_form = AudiencesForm(request.form)
    salesforce_form = SalesforceForm(request.form)
    partner = request.form.get('parceiro')

    if partner == 'Tiktok':
        if audience_form.validate_on_submit():
            return database_operations.execute('insert_audience', user=user, audience_form=audience_form, salesforce_form=salesforce_form, id_user_insert=session[f'{user}_user_id'], db_name=request.form['db_name'], table_name=request.form['table_name'], audience_name=request.form['audience_name'], parceiro=request.form['parceiro'], advertiser_name=request.form['advertiser_name'])
            
    elif partner == 'Salesforce':
        if salesforce_form.validate_on_submit():
            return database_operations.execute('insert_audience', user=user, audience_form=audience_form, salesforce_form=salesforce_form, id_user_insert=session[f'{user}_user_id'], db_name=request.form['db_name_sf'], table_name=request.form['table_name_sf'], file_name=request.form['file_name'], sftp_path=request.form['sftp_path'], parceiro=request.form['parceiro'])

@app.route('/update/<user>/<partner>/<int:id>', methods=['GET'])
@login_required
def update(user, partner, id):
    if partner ==  'Tiktok':
        audience = list_existing_audiences(id)[0]
        audience_form = AudiencesForm(advertiser_name=audience[6])
        salesforce_form = SalesforceForm()
    else:
        audience = list_existing_audiences_salesforce(id)[0]
        audience_form = AudiencesForm()
        salesforce_form = SalesforceForm()
        
    return render_template('update_audience.html', user=user, audience_form=audience_form, salesforce_form=salesforce_form, audience=audience)

# ROTA DE PROCESSAMENTO DA ATUALIZAÇÃO DE AUDIÊNCIA
@app.route('/update_data/<user>/<int:id>', methods=['POST'])
@login_required
def update_data(user, id):
    partner = request.form.get('parceiro')
    audience_form = AudiencesForm(request.form)
    salesforce_form = SalesforceForm(request.form)

    if partner == 'Tiktok':
        return database_operations.execute('update_audience', id=id, audience_form=audience_form, salesforce_form=salesforce_form,user=user, db_name=request.form['db_name'], table_name=request.form['table_name'], audience_name=request.form['audience_name'], parceiro=request.form['parceiro'], advertiser_name=request.form['advertiser_name'])
            
    elif partner == 'Salesforce':
        return database_operations.execute('update_audience', id=id, audience_form=audience_form, salesforce_form=salesforce_form,user=user, db_name=request.form['db_name_sf'], table_name=request.form['table_name_sf'], parceiro=request.form['parceiro'], file_name=request.form['file_name'], sftp_path=request.form['sftp_path'])

@app.route('/signup/<user>', methods=['GET'])
@login_required
def signup(user):
    form = CadastroUserForm()
    return render_template('create_users.html', user=user, form=form)

# ROTA DE PROCESSAMENTO DE INFORMAÇÕES DA CRIAÇÃO DE USUÁRIO
@app.route('/create_user/<user>', methods=['POST'])
@login_required
def create_user(user):
    form = CadastroUserForm(request.form)
    if form.validate_on_submit():
        return database_operations.execute('insert_user', user=user, username=request.form['user'], password=request.form['password'])
    else:
        error_message = 'As senhas não coincidem. Por favor, verifique.'
        return render_template('create_users.html', user=user, form=form, error_message=error_message)

@app.route('/list_audiences/<user>', methods=['GET'])
@login_required
def list_audiences(user):
    audiences = list_existing_audiences()
    audiences_sf = list_existing_audiences_salesforce()
    csrf_token = generate_csrf()
    return render_template('list_audiences.html', user=user, audiences=audiences, audiences_sf=audiences_sf, csrf_token=csrf_token)

@app.route('/list_processed_audiences/<user>', methods=['GET'])
@login_required
def list_processed_audiences(user):
    audiences = list_existing_audiences(processed_audiences=True)
    audiences_sf = list_existing_audiences_salesforce(processed_audiences=True)
    csrf_token = generate_csrf()
    return render_template('list_processed_audiences.html', user=user, audiences=audiences, audiences_sf=audiences_sf, csrf_token=csrf_token)

# ROTA DE PROCESSAMENTO DE INFORMAÇÕES DA EXCLUSÃO DE AUDIÊNCIAS
@app.route('/delete_audience/<user>/<int:audience_id>/<parceiro>', methods=['DELETE'])
@login_required
def delete_audience(user, audience_id, parceiro):
    return database_operations.execute('delete_audience', audience_id=audience_id, parceiro=parceiro)

@app.route('/logout/<user>', methods=['GET'])
@login_required
def logout(user):
    session[f'user_{user}_logged_in'] = False
    session[f'user_{user}_name'] = None
    session[f'{user}_user_id'] = None
    return redirect(url_for('login'))