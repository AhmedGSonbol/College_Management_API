from flask import request , jsonify
import jwt
from functools import wraps
# from main import app

class myMethods :

    tableName = ""
        

    def message( message , data={}):
        return jsonify({'Message' : message,
                'Data' : data})
    
    def queryAll(tableName):
        return ""
    
    

    def token_required(f):
        @wraps(f)
        def decorated(*args,**kwargs):

            token = None

            if 'x-access-token' in request.headers:

                token = request.headers['x-access-token']
        

            if not token:
                return jsonify({"message":'Token Is Missing!'})

            try:
                data = jwt.decode(token,"654321",algorithms=["HS256"])
            except:
            
                return jsonify({"Message":'Token Is Invalid'})
        
            return f(*args,**kwargs)
        
        return decorated