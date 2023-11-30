
import pyodbc

from flask import jsonify
from Constants.constants import myMethods as me

import jwt
import datetime
from functools import wraps


class LinkDatabase:
    
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=.;DATABASE=College_management_DB')

        self.conn.setdecoding(pyodbc.SQL_CHAR , encoding='utf-8')
        self.conn.setdecoding(pyodbc.SQL_WCHAR , encoding='utf-8')
        self.conn.setencoding(encoding='utf-8')

        self.cursor = self.conn.cursor()

       

    def getUsers(self , type):
        
        query = "SELECT * FROM Users Where User_type = "+type
        
        result = []
        self.cursor.execute(query)
        # result["message"] = "data retrieved succesfully"
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["Name"] = row[1]
            item_dic["Email"] = row[2]
            item_dic["Nat_ID"] = row[3]
            item_dic["Password"] = row[4]
            item_dic["user_Type"] = row[5]
            item_dic["Confirmed"] = row[7]
            
            result.append(item_dic)
        
        return me.message(message="تم إسترجاع البيانات بنجاح !",data=result)


    
    def getUser(self,id):

        query = "SELECT * FROM Users WHERE ID ="+id

        result = []
        
        self.cursor.execute(query)
        # result["message"] = "data retrieved succesfully"
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["Name"] = row[1]
            item_dic["Email"] = row[2]
            item_dic["Nat_ID"] = row[3]
            item_dic["Password"] = row[4]
            item_dic["user_Type"] = row[5]
            item_dic["Semester"] = row[6]
            item_dic["Confirmed"] = row[7]

            result.append(item_dic)
            

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !")
        else:
            
            return me.message("تم إسترجاع البيانات بنجاح !",data=result[0])
        

    
    def updateUser(self,id,data):
        query = "UPDATE Users SET Name = '"+data["Name"]+"' ,Email = '"+data["Email"]+"',Nat_ID = '"+data["Nat_ID"]+"' WHERE ID = "+id
        try:
            self.cursor.execute(query)
            self.conn.commit()
        
        except Exception as ex:
            
            if 'U_Full_Name' in ex.args[1]:
                return {'Message':"الأسم موجود بالفعل"},400
            
            elif 'U_Nat_ID' in ex.args[1]:
                return {'Message':"رقم الهوية موجود بالفعل"},400
            
            elif 'U_Email' in ex.args[1]:
                return {'Message':"البريد الألكتروني موجود بالفعل"},400
            
            else:
                return {'Message':str(ex)},400
            
        
        
        return {'Message':"تم تعديل البيانات بنجاح"},200



    
    def updateUserpassword(self,id,data):

        query = "SELECT * FROM Users WHERE ID ="+id + " AND Password = '"+ data['current_password']+"'"
        
        result = []
        
        self.cursor.execute(query)
        # result["message"] = "data retrieved succesfully"
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["Name"] = row[1]
            item_dic["Email"] = row[2]
            item_dic["Nat_ID"] = row[3]
            item_dic["Password"] = row[4]
            item_dic["user_Type"] = row[5]
            item_dic["Semester"] = row[6]
            item_dic["Confirmed"] = row[7]

            result.append(item_dic)

            
            

        
        if len(result) == 0 :

            
            return   jsonify({'Message':"كلمة السر القديمة غير صحيحة !"}),400
        else:
            
            


            query2 = "UPDATE Users SET  Password = '"+data["password"]+"' WHERE ID = "+id
            
            try:
                self.cursor.execute(query2)
                self.conn.commit()
            
            except Exception as ex:
                
            
                return {'Message':str(ex)},400
            
      
        
        return {'Message':"تم تعديل البيانات بنجاح"},200
        
    
    
    def deleteUser(self , id):
        query = "DELETE FROM Users WHERE ID = "+id
        self.cursor.execute(query)
        self.conn.commit()
        return {'Message':"تمت عملية الحذف بنجاح"}
    
    def confirmStudent(self,id):
        query = "UPDATE Users Set Confirmed = 1 WHERE ID ="+id
        self.cursor.execute(query)
        self.conn.commit()
        return {"Message":"تم تأكيد الطالب بنجاح"}
    
    def rejectStudent(self,id):
        query = "DELETE FROM Users WHERE ID ="+id
        self.cursor.execute(query)
        self.conn.commit()
        return {"Message":"تم رفض الطالب بنجاح"}
    



    ###############    L O G I N     ################
    
    def login(self,data):

        query = "SELECT * FROM Users WHERE Email = '"+data['email']+"' AND Password = '"+data['password']+"'"
        
        result = []
        self.cursor.execute(query)
        # result["message"] = "data retrieved succesfully"
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["Name"] = row[1]
            item_dic["Email"] = row[2]
            item_dic["Nat_ID"] = row[3]
            # item_dic["Password"] = row[4]
            item_dic["user_Type"] = str(row[5])
            item_dic["Semester"] = row[6]   
            item_dic["Confirmed"] = row[7]
            
            
            result.append(item_dic)
        
        
        if len(result) == 0 :
            
            return   me.message(message="بيانات الدخول غير صحيحة !")
        
        else:
            if result[0]['Confirmed'] == False :
                return me.message(message='في إانظار موافقة المسؤول !'),400
            
            

            if int(result[0]['Semester']) > 8 :
                return me.message(message='لا يمكن تسجيل المواد بعد إنتهاء المرحلة الدراسية'),400
            
            token = jwt.encode({'uid':result[0]["ID"] , 'exp':datetime.datetime.utcnow() + datetime.timedelta(weeks=10)},"654321" )
            return ({'message':'تم تسجيل الدخول بنجاح','data':{'token':token,'user':result[0]}}),200
            



    ###############    R E G I S T E R     ################

    def register(self , data):
        
        query = "INSERT INTO Users (Name ,Email,Nat_ID,Password,User_type,"+("" if data['user_type'] != "2" else "Semester,")+"Confirmed) VALUES('"+data["name"]+"','"+data["email"]+"','"+data["nat_ID"]+"','"+data["password"]+"', '"+data["user_type"]+"', "+("" if data['user_type'] != "2" else  ("'"+ data["semester"]+"'," ))+ "'"+data["confirmed"]+"')"

        try :
            self.cursor.execute(query)
            self.conn.commit()

        except Exception as ex:
            
            if 'U_Full_Name' in ex.args[1]:
                return {'Message':"الأسم موجود بالفعل"},400
            
            elif 'U_Nat_ID' in ex.args[1]:
                return {'Message':"رقم الهوية موجود بالفعل"},400
            
            elif 'U_Email' in ex.args[1]:
                return {'Message':"البريد الألكتروني موجود بالفعل"},400
            
            else:
                return {'Message':str(ex)},400
            
        if data['user_type'] == "2":

            return {'Message':"تم تسجيل الطالب بنجاح , في انتظار موافقة المسؤل"},201
        
        return {'Message':"تم إضافة الموظف بنجاح"},201
    


    ###############    S U B J E C T S     ################

    
    def post_subjects(self , data):
        
        query = "INSERT INTO Subjects (Name_EN ,Name_AR,Hours,Sub_Type,Code,Semester) VALUES('"+data["name_EN"]+"','"+data["name_AR"]+"','"+data["hours"]+"','"+data["sub_Type"]+"','"+data["code"]+"','"+ data["semester"]+"')"

        try :
            self.cursor.execute(query)
            self.conn.commit()

        except pyodbc.Error as ex:
            
            if 'U_Name_AR' in ex.args[1]:
                return {'Message':"اسم المادة عربي مكرر"},200
            
            elif 'U_Name_EN' in ex.args[1]:
                return {'Message':"اسم المادة انجليزي مكرر"},200
            
            elif 'U_Code' in ex.args[1]:
                return {'Message':"كود المادة مكرر"},200
            
        return {'Message':"تم إضافة المادة بنجاح"},201
    
    
    def get_subjects(self , id):
        
        query = "SELECT * FROM  Subjects"

        if(int(id) > 0):
        
            query += " WHERE ID = "+id
        

        self.cursor.execute(query)

        result = []

        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["name_EN"] = row[1]
            item_dic["name_AR"] = row[2]
            item_dic["hours"] = row[3]
            item_dic["sub_Type"] = row[4]
            item_dic["code"] = row[5]
            item_dic["semester"] = row[6]

            result.append(item_dic)
            

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !")
        else:
            if len(result) > 1 :
                return me.message("تم إسترجاع البيانات بنجاح !",data=result)
            return me.message("تم إسترجاع البيانات بنجاح !",data=result[0])
    

    def updateSubject(self ,id, data):
        
        query = "UPDATE Subjects SET Name_EN = '"+data["name_EN"]+"' ,Name_AR = '"+data["name_AR"]+"',Hours = '"+data["hours"]+"',Sub_Type = '"+data["sub_Type"]+"',Code = '"+data["code"]+"',Semester = '"+ data["semester"]+"' WHERE ID = "+id
        try :
            self.cursor.execute(query)
            self.conn.commit()

        except Exception as ex:
            
            if 'U_Name_AR' in ex.args[1]:
                return {'Message':"اسم المادة عربي مكرر"},400
            
            elif 'U_Name_EN' in ex.args[1]:
                return {'Message':"اسم المادة انجليزي مكرر"},400
            
            elif 'U_Code' in ex.args[1]:
                return {'Message':"كود المادة مكرر"},400
        
        except:
            return {'Message':"المادة غير موجودة"},400

        return {'Message':"تم تعديل المادة بنجاح"},200


    def deleteSubject(self , id):
        query = "DELETE FROM Subjects WHERE ID = "+id
        self.cursor.execute(query)
        self.conn.commit()
        return {'Message':"تم حذف المادة بنجاح"}


    ###############    S U B J E C T S   W I T H   S T U D E N T S     ################

    def getStudentSubjects(self,stu_id):

        query = "SELECT * FROM vi_Student_Subjects WHERE Student_ID = "+stu_id

        result = []
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["name_EN"] = row[1]
            item_dic["name_AR"] = row[2]
            item_dic["hours"] = row[3]
            item_dic["sub_Type"] = row[4]
            item_dic["code"] = row[5]
            item_dic["semester"] = row[6]
            
            result.append(item_dic)
        
        
        if(len(result) > 0):
            return me.message(message='تم استرجاع بيانات المواد للطالب بنجاح',data=result)


        
        query2 = "SELECT Semester FROM Users WHERE ID = "+stu_id
        
        self.cursor.execute(query2)
        
        result = []
        
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["semester"] = row[0]
            
            result.append(item_dic)

        
        

        query3 ="SELECT * FROM Subjects WHERE Semester = "+result[0]['semester']

        self.cursor.execute(query3)

        result = []
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["name_EN"] = row[1]
            item_dic["name_AR"] = row[2]
            item_dic["hours"] = row[3]
            item_dic["sub_Type"] = row[4]
            item_dic["code"] = row[5]
            item_dic["semester"] = row[6]
            
            result.append(item_dic)

        return me.message(message='تم استرجاع بيانات المواد للطالب بنجاح',data=result)
    



    def deleteStudentSubjects(self,stu_id):
         

        delQuery = "DELETE FROM Students_Subjects WHERE Student_ID = "+stu_id
        self.cursor.execute(delQuery)
        self.conn.commit()

        return {'Message':'تم حذف بيانات المواد للطالب لاضافة تعديلا جديدة'}




    def deleteAdminStudentSubject(self,data,stu_id,sub_id):
         
        query = "DELETE FROM Students_Subjects WHERE Student_ID = "+data['student_id']+ " AND Subject_ID ="+data['subject_id']

        self.cursor.execute(query)
        self.conn.execute()
        

        return me.message('تم حذف مادة الطالب بنجاح')




    def postStudentSubjects(self,stu_id,sub_id):
        # return jsonify({'s':datetime.datetime.now()})
        query = "INSERT INTO Students_Subjects (Student_ID , Subject_ID , Date) VALUES(?,?,?)"
        try:

            self.cursor.execute(query,(stu_id,sub_id,datetime.datetime.now()))
            self.conn.commit()

        except Exception as ex:
            if 'U_Stu_Sub' in ex.args[1]:
                return me.message(message='تم ربط الطالب بنفس المادة مُسبقا !'),400
            
            return {'Message':'خطأ في الربط بين الطالب و المادة '},400

    

        return me.message(message='تم حفظ البيانات بنجاح')
    

    
    def getSubmittedStudents(self,stu_id):
        #vi_Submitted_Students
        query = "SELECT * FROM vi_Submitted_Students"

        if int(stu_id) > 0:
            query += " WHERE ID = "+stu_id
        
        
        result = []
        
        self.cursor.execute(query)
        # result["message"] = "data retrieved succesfully"
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["Name"] = row[1]
            item_dic["Email"] = row[2]
            item_dic["Nat_ID"] = row[3]
            item_dic["Password"] = row[4]
            item_dic["user_Type"] = row[5]
            item_dic["Semester"] = row[6]
            item_dic["Confirmed"] = row[7]

            result.append(item_dic)
            

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !")
        else:
            if int(stu_id) > 0:
                return  me.message("تم إسترجاع البيانات بنجاح !",data=result[0])
            return me.message("تم إسترجاع البيانات بنجاح !",data=result)







    def moveToNextSemster(self):
        query = "UPDATE Users SET Semester = Semester + 1 WHERE Semester <> 0"
        self.cursor.execute(query)
        self.conn.commit()

        return me.message(message='تم نقل جميع الطلاب الي الصف الدراسي التالي بنجاح')
    

    def closeConn(self):
        self.conn.close()

