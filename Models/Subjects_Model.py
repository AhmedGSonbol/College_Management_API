from flask import Blueprint , jsonify ,request
from DB_Connections.DB_connections import LinkDatabase
from Constants.constants import myMethods as me

sub_blp = Blueprint("sub_blp",__name__,static_folder="static",template_folder="templates")

db = LinkDatabase()

@sub_blp.route("/subject",methods=['POST'])
@me.token_required
def post_subjects():
     
     request_data = request.get_json()
     if request_data is None or "name_EN" not in  request_data or "name_AR" not in  request_data or "hours" not in  request_data or "sub_Type" not in  request_data or "code" not in  request_data and "semester" not in request_data:
          
          return jsonify({'Message':'Input data are missing !'}) 

     return db.post_subjects(request_data)


@sub_blp.route("/subject",methods=['GET'])
@me.token_required
def get_subjects():

     return db.get_subjects()