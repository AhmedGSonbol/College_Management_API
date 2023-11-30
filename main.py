from flask import Flask , request , jsonify
import jwt
import datetime
from functools import wraps
from Models.Users_Model import usersblp
from Models.Login_Reg_Model import log_reg_blp
from Models.Subjects_Model import sub_blp
from Models.Students_Subjects_Model import stu_sub_blp
from Models.MoveToNestSemster import move_blp
from flask import Flask
from flask_cors import CORS ,cross_origin

app = Flask(__name__)

CORS(app)



app.register_blueprint(log_reg_blp , url_prefix="")
app.register_blueprint(sub_blp , url_prefix="/subject")
app.register_blueprint(usersblp , url_prefix="/users")
app.register_blueprint(stu_sub_blp , url_prefix="/StudentSubjects")
app.register_blueprint(move_blp, url_prefix="/movetonextsem")



app.config['SECRET_KEY'] = '654321'

if __name__ == '__main__':
    # app.run(debug=False,host='0.0.0.0')
    app.run(debug=True)
