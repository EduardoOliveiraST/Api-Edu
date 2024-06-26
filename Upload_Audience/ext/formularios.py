from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    user = StringField('Usuário:', validators=[DataRequired(), Length(min=6, max=40)], render_kw={'placeholder': 'Insira seu usuário'})
    password = PasswordField('Senha:', validators=[DataRequired(), Length(min=6, max=20)], render_kw={'placeholder': 'Insira sua senha'})
    submit = SubmitField('Login')

class AudiencesForm(FlaskForm):
    db_name = StringField('Nome do Banco de Dados', validators=[DataRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Ex: db_database'})
    table_name = StringField('Nome da Tabela', validators=[DataRequired(), Length(min=6, max=60)])
    audience_name = StringField('Nome da Audiência', validators=[DataRequired(), Length(min=6, max=60)])
    parceiro = SelectField('parceiro', choices=[('Tiktok', 'Tiktok'), ('Salesforce', 'Salesforce')], validators=[DataRequired()])
    advertiser_name = SelectField('advertiser_name', choices=[('Serasa_Limpa_Nome', 'Serasa_Limpa_Nome'), ('Serasa_Score', 'Serasa_Score'), ('Serasa_Premium', 'Serasa_Premium'), ('Serasa_Ecred', 'Serasa_Ecred'), ('Serasa_Carteira_Digital', 'Serasa_Carteira_Digital')])    
    submit = SubmitField('Criar Audiência')

class CadastroUserForm(FlaskForm):
    user = StringField('Usuário', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Criar usuário')

class SalesforceForm(FlaskForm):
    db_name_sf = StringField('Nome do Banco de Dados', validators=[DataRequired(), Length(min=6, max=20)],render_kw={'placeholder': 'Ex: db_database'})
    table_name_sf = StringField('Nome da Tabela', validators=[DataRequired(), Length(min=6, max=60)])
    file_name = StringField('Nome do arquivo', validators=[DataRequired(), Length(min=6, max=50)])
    sftp_path = StringField('Path SFTP', validators=[DataRequired(), Length(min=6, max=50)])
    submit = SubmitField('Enviar Audiência')