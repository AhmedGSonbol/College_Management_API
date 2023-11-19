
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
        

    
    def putUser(self,id,data):
        query = "UPDATE Users SET UserName = '"+data["Name"]+"',Password = '"+data["Password"]+"' WHERE ID = "+id
        self.cursor.execute(query)
        self.conn.commit()
        return {'message':"Updated Succesfully"}
    
    
    def addUser(self , data):
        if not data['Name'] | data['Password']:
            return {'message':"Data Is Missing"}
        
        query = "INSERT INTO Users (Name , Password) VALUES ('"+data["Name"]+"','"+data["Password"]+"')"
        self.cursor.execute(query)
        self.conn.commit()
        return {'message':"Added Succesfully"},201
    
    def deleteUser(self , id):
        query = "DELETE FROM Users WHERE ID = "+id
        self.cursor.execute(query)
        self.conn.commit()
        return {'message':"Data Deleted Succesfully"}
    



    ###############    L O G I N     ################
    # unicode(str, errors='ignore')
    def login(self,data):

        query = "SELECT * FROM Users WHERE Email = '"+data['email']+"' AND Password = '"+data['password']+"'"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        if len(data) == 0 :
            
            return   me.message(message="لا يوجد بيانات !")
        
        else:
            token = jwt.encode({'uid':data[0][0] , 'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=5)},"654321" )
            
            return me.message("تم إسترجاع البيانات بنجاح !",data=token) # token here



    ###############    R E G I S T E R     ################

    def register(self , data):
        
        query = "INSERT INTO Users (Name ,Email,Nat_ID,Password,User_type,Semester,Confirmed) VALUES('"+data["name"]+"','"+data["email"]+"','"+data["nat_ID"]+"','"+data["password"]+"','"+data["user_type"]+"','"+ data["semester"]+"','"+data["confirmed"]+"')"

        try :
            self.cursor.execute(query)
            self.conn.commit()

        except pyodbc.Error as ex:
            
            if 'U_Full_Name' in ex.args[1]:
                return {'Message':"الأسم موجود بالفعل"},200
            
            elif 'U_Nat_ID' in ex.args[1]:
                return {'Message':"رقم الهوية موجود بالفعل"},200
            
            elif 'U_Email' in ex.args[1]:
                return {'Message':"البريد الألكتروني موجود بالفعل"},200
            
        if data['user_type'] == "2":

            return {'Message':"تم إضافة الطالب بنجاح"},201
        
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

        except pyodbc.Error as ex:
            
            if 'U_Name_AR' in ex.args[1]:
                return {'Message':"اسم المادة عربي مكرر"},200
            
            elif 'U_Name_EN' in ex.args[1]:
                return {'Message':"اسم المادة انجليزي مكرر"},200
            
            elif 'U_Code' in ex.args[1]:
                return {'Message':"كود المادة مكرر"},200
        
        except:
            return {'Message':"المادة غير موجودة"},200

        return {'Message':"تم تعديل المادة بنجاح"},200


    def deleteSubject(self , id):
        query = "DELETE FROM Subjects WHERE ID = "+id
        self.cursor.execute(query)
        self.conn.commit()
        return {'Message':"تم حذف المادة بنجاح"}





    