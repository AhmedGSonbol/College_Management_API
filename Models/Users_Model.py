from flask import Blueprint , jsonify
from DB_Connections.DB_connections import LinkDatabase
from Constants.constants import myMethods as me


usersblp = Blueprint("usersblp",__name__,static_folder="static",template_folder="templates")

db = LinkDatabase()


# ================== All Users By Type [GET] =========================

@usersblp.route("/<type>",methods=['GET'])
@me.token_required
def getUsersByType(token,type = 0):
     
     return db.getUsers(type=type)

# ================== GET One User By Token [GET] =========================

@usersblp.route("",methods=['GET'])
@me.token_required
def getUserByToken(token):
     
     return db.getUser(id=str(token['uid']))
