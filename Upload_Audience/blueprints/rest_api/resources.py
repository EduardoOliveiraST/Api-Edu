from flask import jsonify, abort, Response
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from ext.database_ext.list_audiences import *
from ext import database_operations
import json

auth = HTTPBasicAuth()


@auth.verify_password
def verify(username, password):
    USER_DATA = {"admin": "qwe123@A"}

    if not (username and password):
        return False
    return USER_DATA.get(username) == password

class AudienceResource(Resource):
    @auth.login_required
    def get(self):
        audiences = list_existing_audiences()
        audiences_sf = list_existing_audiences_salesforce()
        json_tk = {
            "Created_Audiences": [
                {
                    "audience_id": audience[0],
                    "db_name": audience[2],
                    "table_name": audience[3],
                    "audience_name": audience[4],
                    "platform": audience[5],
                    "advertiser_name": audience[6],
                    "created_by": audience[7]
                } for audience in audiences
            ]
        }

        json_sf = {
            "Created_Audiences": [
                {
                  "audience_id": audience[0],
                  "db_name_sf": audience[2],
                  "table_name_sf": audience[3],
                  "file_name": audience[4],
                  "platform": audience[5],
                  "sftp_path": audience[6],
                  "created_by": audience[7]
                  } for audience in audiences_sf
            ]
        }
        # Combine the audience lists
        combined_audiences = json_tk["Created_Audiences"] + json_sf["Created_Audiences"]

        # Create the final JSON structure
        final_json = {"Created_Audiences": combined_audiences}

        json_response = json.dumps(final_json, ensure_ascii=False, indent=2).encode('utf-8')

        # Retornar a resposta com Content-Type definido como application/json
        return Response(json_response, content_type='application/json')

class AudienceItemResource(Resource):
    @auth.login_required
    def get(self, parceiro, audience_id):
        try:
            if parceiro in ['Tiktok', 'tiktok']:
                audience = list_existing_audiences(audienceid=audience_id)[0]
                json_audience = {
                        "audience_id": audience[0],
                        "db_name": audience[2],
                        "table_name": audience[3],
                        "audience_name": audience[4],
                        "platform": audience[5],
                        "advertiser_name": audience[6],
                        "created_by": audience[7]
                }
            
            else:
                audience = list_existing_audiences_salesforce(audienceid=audience_id)[0]
                json_audience = {
                      "audience_id": audience[0],
                      "db_name_sf": audience[2],
                      "table_name_sf": audience[3],
                      "file_name": audience[4],
                      "platform": audience[5],
                      "sftp_path": audience[6],
                      "created_by": audience[7]
                }
              

            json_response = json.dumps(json_audience, ensure_ascii=False, indent=2).encode('utf-8')

            # Retornar a resposta com Content-Type definido como application/json
            return Response(json_response, content_type='application/json')
        except:
            return abort(404)

class DeleteAudience(Resource):
    @auth.login_required
    def get(self, parceiro, audience_id):
        try:
            database_operations.execute('delete_audience', parceiro=parceiro, audience_id=audience_id)
        except:
            return abort(404)

class ProcessSuccessAudience(Resource):
    @auth.login_required
    def get(self, parceiro, audience_id):
        try:
            database_operations.execute('process_success_audience', parceiro=parceiro, audience_id=audience_id)
        except:
            return abort(404)

class ListProcessedAudience(Resource):
    @auth.login_required
    def get(self):
        audiences = list_existing_audiences(processed_audiences = True)
        audiences_sf = list_existing_audiences_salesforce(processed_audiences = True)
        json_tk = {
            "Created_Audiences": [
                {
                    "audience_id": audience[0],
                    "db_name": audience[2],
                    "table_name": audience[3],
                    "audience_name": audience[4],
                    "platform": audience[5],
                    "advertiser_name": audience[6],
                    "created_by": audience[7]
                } for audience in audiences
            ]
        }

        json_sf = {
            "Created_Audiences": [
                {
                  "audience_id": audience[0],
                  "db_name_sf": audience[2],
                  "table_name_sf": audience[3],
                  "file_name": audience[4],
                  "platform": audience[5],
                  "sftp_path": audience[6],
                  "created_by": audience[7]
                  } for audience in audiences_sf
            ]
        }
        # Combine the audience lists
        combined_audiences = json_tk["Created_Audiences"] + json_sf["Created_Audiences"]

        # Create the final JSON structure
        final_json = {"Created_Audiences": combined_audiences}

        json_response = json.dumps(final_json, ensure_ascii=False, indent=2).encode('utf-8')

        # Retornar a resposta com Content-Type definido como application/json
        return Response(json_response, content_type='application/json')