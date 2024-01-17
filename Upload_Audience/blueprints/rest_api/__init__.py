from flask import Blueprint
from flask_restful import Api
from .resources import AudienceItemResource, AudienceResource

bp = Blueprint("rest_api", __name__, url_prefix='/api/v1')
api = Api(bp)

api.add_resource(AudienceResource, '/list_audiences/')
api.add_resource(AudienceItemResource, '/list_audiences/<audience_id>')

def init_app(app):
    app.register_blueprint(bp)

