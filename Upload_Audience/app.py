from ext import config
from flask import Flask
from blueprints import rest_api
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import os

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

app.secret_key = config.SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

from views import *

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)