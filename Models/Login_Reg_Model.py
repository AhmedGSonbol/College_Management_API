from flask import Blueprint , jsonify ,request
from DB_Connections.DB_connections import LinkDatabase
from flask_cors import cross_origin
# from constants import myMethods


log_reg_blp = Blueprint("log_reg_blp",__name__,static_folder="static",template_folder="templates")

db = LinkDatabase()

@cross_origin(origin='*',headers=['Content-Type','x-access-token'])
@log_reg_blp.route("/login",methods=['POST'])
def login():
     
     request_data = request.get_json()
     if request_data is None or "email" not in  request_data or "password" not in request_data:
          return jsonify({'Message':'email & password are requeired !'}) 
     return db.login(request_data)





@cross_origin(origin='*',headers=['Content-Type','x-access-token'])
@log_reg_blp.route("/register",methods=['POST'])
def register():
     
     request_data = request.get_json()
     if request_data is None or "name" not in  request_data or "email" not in  request_data or "nat_ID" not in  request_data or "password" not in  request_data or "user_type" not in  request_data:
          return jsonify({'Message':'Input data are missing !'}) 
     if  request_data['user_type'] == "student":
          if 'semester' not in  request_data:
               return jsonify({'Message':'semester is missing !'}) 
          request_data['confirmed'] = "0"
     else:
          request_data['semester'] = None
          request_data['confirmed'] = "1"


     return db.register(request_data)