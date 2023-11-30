from flask import Blueprint , jsonify ,request
from DB_Connections.DB_connections import LinkDatabase
from Constants.constants import myMethods as me
from flask_cors import cross_origin


usersblp = Blueprint("usersblp",__name__,static_folder="static",template_folder="templates")

db = LinkDatabase()


# ================== All Users By Type [GET] =========================

@usersblp.route("/<type>",methods=['GET'])
@me.token_required
def getUsersByType(token,type = 0):
     
     return db.getUsers(type=type)

# ================== GET One User By Token [GET] =========================

@usersblp.route("",methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','x-access-token'])
@me.token_required
def getUserByToken(token):
     
     return db.getUser(id=str(token['uid']))


# ================== Update User [PUT] =========================
@usersblp.route("/profile",methods=['PUT'])
@me.token_required
def register(token):
     
     request_data = request.get_json()
     if request_data is None or "Name" not in  request_data or "Email" not in  request_data or "Nat_ID" not in  request_data:
          return jsonify({'Message':'Inputs data are missing !'}),400 
     # if  request_data['user_type'] == "2":
     #      if 'semester' not in  request_data:
     # return jsonify({'Message':'semester is missing !'}) 


     return db.updateUser(id= str(token['uid']), data=request_data)

# ================== Update User Password [PUT] =========================
@cross_origin(origin='*',headers=['Content-Type','x-access-token'])
@usersblp.route("/updatepass",methods=['PUT'])
@me.token_required
def registerPassword(token):
     
     request_data = request.get_json()
     if request_data is None or "current_password" not in  request_data or "password" not in  request_data :
          return jsonify({'Message':'password data are missing !'}) 



     return db.updateUserpassword(id= str(token['uid']), data=request_data)

# ================== Delete User [DELETE] =========================

@usersblp.route("/<id>",methods=['DELETE'])
@me.token_required
def deleteUser(token,id):
     
     return db.deleteUser(id=id)

# ================== Confirm Student [POST] =========================

@usersblp.route("/confirmStudent/<id>",methods=['POST'])
@me.token_required
def confirmStudent(token,id):
     
     return db.confirmStudent(id=id)

# ================== Reject Student [POST] =========================

@usersblp.route("/rejectuser/<id>",methods=['POST'])
@me.token_required
def rejectuser(token,id):
     
     return db.rejectStudent(id=id)