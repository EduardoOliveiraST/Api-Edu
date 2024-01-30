from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    user = StringField('Usuário:', validators=[DataRequired(), Length(min=6, max=40)], render_kw={'placeholder': 'Insira seu usuário'})
    password = PasswordField('Senha:', validators=[DataRequired(), Length(min=6, max=20)], render_kw={'placeholder': 'Insira sua senha'})
    submit = SubmitField('Login')

class AudiencesForm(FlaskForm):
    db_name = StringField('Nome do Banco de Dados', validators=[DataRequired(), Length(min=6, max=20)])
    table_name = StringField('Nome da Tabela', validators=[DataRequired(), Length(min=6, max=20)])
    audience_name = StringField('Nome da Audiência', validators=[DataRequired(), Length(min=6, max=50)])
    selector = SelectField('Fornecedor', choices=[('Tiktok', 'Tiktok'), ('Salesforce', 'Salesforce')], validators=[DataRequired()])  
    submit = SubmitField('Criar Audiência')

class CadastroUserForm(FlaskForm):
    user = StringField('Usuário', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Criar usuário')