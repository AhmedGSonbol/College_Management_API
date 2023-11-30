from flask import Blueprint , jsonify ,request
from DB_Connections.DB_connections import LinkDatabase
from Constants.constants import myMethods as me
from flask_cors import cross_origin


stu_sub_blp = Blueprint("stu_sub_blp",__name__,static_folder="static",template_folder="templates")

db = LinkDatabase()

# ================== Get Student Subjects [GET] =========================
@stu_sub_blp.route("",methods=['GET'])
@me.token_required
def getStudentSubjects(token):
     
     return db.getStudentSubjects(stu_id=str(token['uid']))

# ================== DELETE Student Subjects [DELETE] =========================
@stu_sub_blp.route("",methods=['DELETE'])
@me.token_required
def deleteStudentSubjects(token):

     return db.deleteStudentSubjects(stu_id=str(token['uid']))

# ================== DELETE ADMIN Student Subjects [DELETE] =========================
@stu_sub_blp.route("/AdminDeleteSub",methods=['DELETE'])
@me.token_required
def deleteAdminStudentSubject(token):
      request_data = request.get_json()
      if request_data is None or "subject_id" not in request_data or  "student_id" not in request_data:
          return jsonify({'Message':'subject_id , student_id are missing !'}),400 
     
      return db.deleteAdminStudentSubject(request_data)

     

# ================== ADD Student Subjects [POST] =========================
@stu_sub_blp.route("",methods=['POST'])
@me.token_required
def postStudentSubjects(token):
     request_data = request.get_json()
     if request_data is None or "subject_id" not in request_data:
          return jsonify({'Message':'subject_id is missing !'}),400 
     
     return db.postStudentSubjects(stu_id=str(token['uid']),sub_id=request_data['subject_id'])

# ================== GET SUBMITTED STUDENTS [GET] =========================
@stu_sub_blp.route("/Submitted",methods=['GET'])
@me.token_required
def getSubmittedStudents(token):
     request_data = request.get_json()
     stu_id = 0
     if request_data is not None and 'student_id' in request_data:
          stu_id = request_data['student_id']
     return db.getSubmittedStudents(stu_id)

