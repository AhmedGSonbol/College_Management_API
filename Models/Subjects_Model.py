from flask import Blueprint , jsonify ,request
from DB_Connections.DB_connections import LinkDatabase
from Constants.constants import myMethods as me

sub_blp = Blueprint("sub_blp",__name__,static_folder="static",template_folder="templates")

db = LinkDatabase()


# ================== Subjects [POST] =========================
@sub_blp.route("",methods=['POST'])
@me.token_required
def post_subjects(token):
     
     request_data = request.get_json()
     if request_data is None or "name_EN" not in  request_data or "name_AR" not in  request_data or "hours" not in  request_data or "sub_Type" not in  request_data or "code" not in  request_data and "semester" not in request_data:
          
          return jsonify({'Message':'Inputs data are missing !'}) 

     return db.post_subjects(request_data)


# ================== Subjects [GET] =========================
@sub_blp.route("",methods=['GET'])
@sub_blp.route("/<id>",methods=['GET'])
@me.token_required
def get_subjects(token,id = 0):

     return db.get_subjects(id=id)

# ================== Subjects [UPDATE] =========================
@sub_blp.route("/<id>",methods=['PUT'])
@me.token_required
def update_subjects(token,id):
     
     request_data = request.get_json()
     if request_data is None or "name_EN" not in  request_data or "name_AR" not in  request_data or "hours" not in  request_data or "sub_Type" not in  request_data or "code" not in  request_data and "semester" not in request_data:
          
          return jsonify({'Message':'Inputs data are missing !'}) 

     return db.updateSubject(id=id,data=request_data)

# ================== Subjects [DELETE] =========================
@sub_blp.route("/<id>",methods=['DELETE'])
@me.token_required
def delete_subjects(token,id):


     return db.deleteSubject(id=id)