from flask import Blueprint , jsonify
from DB_Connections.DB_connections import LinkDatabase
# from constants import myMethods


usersblp = Blueprint("usersblp",__name__,static_folder="static",template_folder="templates")

db = LinkDatabase()

@usersblp.route("/users",methods=['GET'])
def get():
     
     return jsonify({'test':'nice'})


@usersblp.route("/users",methods=['POST'])
def get():
     
     return jsonify({'test':'nice'})