
import pyodbc

from flask import jsonify , request
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

       

    def getUsers(self):
        
        query = "SELECT * FROM Users"
        
        result = []
        self.cursor.execute(query)
        # result["message"] = "data retrieved succesfully"
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["UserName"] = row[1]
            item_dic["Password"] = row[2]
            
            result.append(item_dic)

        return me.message(message="Data Retrived Succesfully !",data=result)


    
    def getUser(self,id):

        query = "SELECT * FROM Users WHERE ID ="+id

        result = []
        
        self.cursor.execute(query)
        # result["message"] = "data retrieved succesfully"
        for row in self.cursor.fetchall():
            item_dic ={}
            item_dic["ID"] = row[0]
            item_dic["Name"] = row[1]
            item_dic["Password"] = row[2]

            result.append(item_dic)
            

        if len(result) == 0 :
            
            return   me.message(message="No Record Found !")
        else:
            
            return me.message("Data Retrived Succesfully",data=result[0])
        

    
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

    def login(self,data):

        query = "SELECT * FROM Users WHERE Email = '"+data['email']+"' AND Password = '"+data['password']+"'"
        self.cursor.execute(query)
        data = self.cursor.fetchall()[0]
        if len(data) == 0 :
            
            return   me.message(message="No Record Found !")
        
        else:
            token = jwt.encode({'uid':data[0] , 'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=5)},"654321" )
            
            return me.message("Data Retrived Succesfully",data=token) # token here



    ###############    R E G I S T E R     ################

    def register(self , data):
        
        query = "INSERT INTO Users (Name ,Email,Nat_ID,Password,User_type,Semester,Confirmed) VALUES('"+data["name"]+"','"+data["email"]+"','"+data["nat_ID"]+"','"+data["password"]+"','"+data["user_type"]+"','"+ data["semester"]+"','"+data["confirmed"]+"')"

        self.cursor.execute(query)
        self.conn.commit()
        if data['user_type'] == "2":

            return {'Message':"Student Added Succesfully"},201
        
        return {'Message':"Employee Added Succesfully"},201
    
    ###############    S U B J E C T S     ################

    
    def post_subjects(self , data):
        
        query = "INSERT INTO Subjects (Name_EN ,Name_AR,Hours,Sub_Type,Code,Semester) VALUES('"+data["name_EN"]+"','"+data["name_AR"]+"','"+data["hours"]+"','"+data["sub_Type"]+"','"+data["code"]+"','"+ data["semester"]+"')"

        self.cursor.execute(query)
        self.conn.commit()
        return {'Message':"Subject Added Succesfully"},201
    
    
    def get_subjects(self):
        
        query = "SELECT * FROM  Subjects"

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
            
            return   me.message(message="No Record Found !")
        else:
            
            return me.message("Data Retrived Succesfully",data=result)







    