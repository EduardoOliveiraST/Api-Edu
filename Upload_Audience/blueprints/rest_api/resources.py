from flask import jsonify, abort
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from ext.database_ext.list_audiences import *
from ext import database_operations

auth = HTTPBasicAuth()

USER_DATA = {
    "admin": "qwe123@A"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

class AudienceResource(Resource):
    @auth.login_required
    def get(self):
        audiences = list_existing_audiences()
        json = {
            "Created_Audiences": [
                {
                    "audience_id": item[0],
                    "db_name": item[3],
                    "table_name": item[4],
                    "audience_name": item[5],
                    "platform": item[6]
                } for item in audiences
            ]
        }

        return jsonify(json)

class AudienceItemResource(Resource):
    @auth.login_required
    def get(self, audience_id):
        try:
            audiences = list_item_existing_audiences(id_audience=audience_id)
            json = {
                
                    "audience_id": audiences[0][0],
                    "db_name": audiences[0][3],
                    "table_name": audiences[0][4],
                    "audience_name": audiences[0][5],
                    "platform": audiences[0][6]
            }

            return jsonify(json)
        except:
            return abort(404)

class DeleteAudienceWithNoSuchTable(Resource):
    @auth.login_required
    def get(self, audience_id):
        try:
            database_operations.execute('delete_audience', audience_id=audience_id)
        except:
            return abort(404)