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
                    "audience_id": audience[0],
                    "db_name": audience[3],
                    "table_name": audience[4],
                    "audience_name": audience[5],
                    "platform": audience[6],
                    "advertiser_name": audience[7]
                } for audience in audiences
            ]
        }

        return jsonify(json)

class AudienceItemResource(Resource):
    @auth.login_required
    def get(self, audience_id):
        try:
            audience = list_item_existing_audiences(id_audience=audience_id)
            json = {
                
                    "audience_id": audience[0][0],
                    "db_name": audience[0][3],
                    "table_name": audience[0][4],
                    "audience_name": audience[0][5],
                    "platform": audience[0][6],
                    "advertiser_name": audience[0][7]
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