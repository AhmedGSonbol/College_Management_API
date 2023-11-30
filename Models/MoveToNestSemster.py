from flask import Blueprint , jsonify ,request
from DB_Connections.DB_connections import LinkDatabase
from Constants.constants import myMethods as me
from flask_cors import cross_origin

move_blp = Blueprint("move_blp",__name__,static_folder="static",template_folder="templates")

db = LinkDatabase()

# ================== Move To Next Semester [POST] =========================

@move_blp.route("",methods=['POST'])
@me.token_required
def moveToNextSem(token):
    return db.moveToNextSemster()
