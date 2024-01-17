from dynaconf import FlaskDynaconf
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def init_app(app):
    FlaskDynaconf(app)
    csrf.init_app(app)