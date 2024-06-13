from flask import Blueprint
from flask_restful import Api
from .resources import AudienceItemResource, AudienceResource, DeleteAudience, ProcessSuccessAudience

"""O endpoint(blueprint) '/api/v1/list_audiences' realiza a busca no banco de dados da aplicação [integration_last_15d] para disponibilizar o json que servirá de insumo para outros processos."""

bp = Blueprint("rest_api", __name__, url_prefix='/api/v1')
api = Api(bp)

api.add_resource(AudienceResource, '/list_audiences/')
api.add_resource(AudienceItemResource, '/list_audiences/<parceiro>/<audience_id>')
api.add_resource(DeleteAudience, '/delete/<parceiro>/<audience_id>')
api.add_resource(ProcessSuccessAudience, '/list_processed_audiences/<parceiro>/<audience_id>')

def init_app(app):
    app.register_blueprint(bp)