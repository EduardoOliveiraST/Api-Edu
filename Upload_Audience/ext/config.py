import toml
from dynaconf import FlaskDynaconf

def read_settings(file_path='settings.toml', environment='default'):
    # Carrega o arquivo TOML
    with open(file_path, 'r') as file:
        settings_data = toml.load(file)
        
    environment_data = settings_data.get(environment, {})

    # Obtém o valor de SQLALCHEMY_DATABASE_URI
    sqlalchemy_database_uri = environment_data.get('SQLALCHEMY_DATABASE_URI', None)

    return sqlalchemy_database_uri

def init_app(app):
    FlaskDynaconf(app)


DATABASE = read_settings(environment='default')
TABLE_AUDIENCES = 'tb_upload_audiences_ecs_marketing'
TABLE_USERS = 'tb_login'
TABLE_SESSIONS = 'tb_sessions'

