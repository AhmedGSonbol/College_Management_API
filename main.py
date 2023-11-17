from flask import Flask , request , jsonify
import jwt
import datetime
from functools import wraps
from Models.Users_Model import usersblp
from Models.Login_Reg_Model import log_reg_blp
from Models.Subjects_Model import sub_blp

app = Flask(__name__)



app.register_blueprint(log_reg_blp , url_prefix="")
app.register_blueprint(sub_blp , url_prefix="")

app.config['SECRET_KEY'] = '654321'

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
