import pymysql
from flask_restful import Resource
from flask import *
import base64
from functions import *
# import JWT packages#
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required



# Add a member class
# member_signup and member_signin
class UserSignup(Resource):
    def post(self):
        # get data from client
        data = request.json
        surname= data["surname"]
        others= data["others"]
        email= data["email"]
        phone= data["phone"]
        password= data["password"]
        location_id= data["location_id"]


        # Check phone number format
        if not check_phone(phone):
            return jsonify({"message": "Invalid phone number format"})

        # Normalize phone number
        phone = normalize_phone(phone)


        # check if password is valid
        response = passwordValidity(password)
        if response == True:
            # connect to DB
            # connection = pymysql.connect(host ='localhost',user = 'root', password ='', database = 'shoeapp')
            connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
            cursor = connection.cursor()
            # instert into database
            sql = "insert into users (surname, others, email, phone, password ,location_id) values( %s, %s, %s, %s, %s, %s)"
            data = (surname, others, email, phone, hash_password(password),location_id)
            try:
                cursor.execute(sql, data)
                connection.commit( )
                code = gen_random(4)
                send_sms(phone, '''Thank you for Joining Shoeapp.
                    Your Secret No: {}. Do not share.'''.format(code))
                return jsonify({ "message": "REGISTER SUCCESSFUL. Thanks" })

            except:
                connection.rollback()
                return jsonify({ "message": "FAILED. Please Try Again" })

        else:
            return jsonify({ "message": response })


class UserSignin(Resource):
    def post(self):
        # get request from client
        data = request.json
        phone = data ["phone"]
        password = data ["password"]
        #  Check phone number format
        if not check_phone(phone):
            return jsonify({"message": "Invalid phone number format"})

         # Normalize phone number
        phone = normalize_phone(phone)

        # connect to db
        connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')

        # connection = pymysql.connect(host ='localhost',user = 'root', password ='', database = 'shoeapp')
        # check if phone exist
        sql = "select* from users where phone =%s"
        cursor =connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, phone)
        if cursor.rowcount == 0:
            return jsonify({"message":"phone does not exist"})
        else:
            # check password////
            user = cursor.fetchone()
            hashed_password =user['password']
            is_matchpassword = hash_verify(password,hashed_password)
            if is_matchpassword == True:
                #including jwt
                access_token = create_access_token(identity= phone, fresh= True)
                return jsonify({'access_token': access_token,'user':user})

                # is_matchpassword == False:
            elif is_matchpassword == False:
                return jsonify({ "message":"LOGIN FAILED,wrong password" })

            else:

                return jsonify({ "message": "Something went wrong" })


class UserProfile(Resource):
    @jwt_required(fresh=True)
    def get(self):
        data = request.json
        user_id = data["user_id"]
        # connection = pymysql.connect(host ='localhost',user = 'root', password ='', database = 'shoeapp')
        # connect to DB
        connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')


        sql = "SELECT * FROM users WHERE user_id = %s"
        cursor  = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, user_id)
        count = cursor.rowcount
        if  count == 0:
            return jsonify({  "message":"User does not exist!"  })
        else:
            user = cursor.fetchone()
            return jsonify({  "message": user })



class ChangePassword(Resource):
    @jwt_required(fresh= True)
    def put(self):
        data = request.json
        user_id = data["user_id"]
        current_password = data["current_password"]
        new_password = data['new_password']
        confirm_password = data["confirm_password"]
        # connection = pymysql.connect(host ='localhost',user = 'root', password ='', database = 'shoe')
        connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')

        sql = "select* from users where user_id = %s"
        cursor =connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, user_id)
        if cursor.rowcount ==0:
            return jsonify({"message":"User not found"})
        else:
            member =cursor.fetchone()
            hashed_password= member["password"]
            is_matchpassword = hash_verify(current_password,hashed_password)
            if is_matchpassword:
                rensponse = passwordValidity(new_password)
                if rensponse ==True:
                    if new_password == confirm_password:
                        # password match
                        sql = "update users set password =%s where user_id=%s"
                        cursor1= connection.cursor()
                        data = ( hash_password(new_password), user_id)
                        try:
                            cursor1.execute(sql,data)
                            connection.commit()
                            return jsonify({"message":"Password changed"})
                        except:
                            connection.rollback()
                            return jsonify({"message":"Password not changed"})
                    else:
                        # Password not match entry
                        return jsonify({"message":"New password does not match with confirm password"})
                else:
                    return jsonify({"message":rensponse})


            else:
                return jsonify({"message":"old password is wrong"})



class Locations(Resource):
     def post(self):
          sql = "select * from location"
        #   connection = pymysql.connect(host='localhost',
        #                                         user='root',
        #                                         password='',
        #                                         database='shoeapp')
          connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'No locations'})
          else:
               locations  = cursor.fetchall()
               return jsonify(locations)




#  connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')


class Shoes(Resource):
     def get(self):
          sql = "select * from shoes"
        #   connection = pymysql.connect(host='localhost', user='root', password='', database='shoeapp')
          connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'No shoes available'})
          else:
            shoes = cursor.fetchall()
                # Convert any bytes data to base64 encoded strings
            for shoe in shoes:
                 for key, value in shoe.items():
                    if isinstance(value, bytes):
                        shoe[key] = base64.b64encode(value).decode('utf-8')
            return jsonify(shoes)




class MakeOrder(Resource):
     @jwt_required(fresh=True)
     def post(self):
          json = request.json
          user_id = json['user_id']
          total_amount = json['total_amount']
          latitude = json['latitude']
          longitude  = json['longitude']
          invoice_no = json['invoice_no']

        #   connection = pymysql.connect(host='localhost',
        #                              user='root',
        #                              password='',
        #                              database='shoeapp')
          connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
          cursor = connection.cursor()

          # Insert Data
          sql = ''' Insert into orders(user_id,total_amount, latitude,longitude, invoice_no )
          values(%s, %s, %s, %s, %s) '''
          # Provide Data
          data = (user_id,total_amount, latitude,longitude, invoice_no)

          try:
               cursor.execute(sql, data)
               connection.commit()
               # Get Member Phone No
               sql = "select * from users where user_id = %s"
               cursor = connection.cursor(pymysql.cursors.DictCursor)
               cursor.execute(sql, user_id)
               member = cursor.fetchone()
               phone = member['phone']

            #    send_sms(decrypt(phone), 'Booking On {} at {} , Invoice {}'
            #             .format( invoice_no))

               return jsonify({'message': 'Order Received'})

          except Exception as error:
               connection.rollback()
               return jsonify({'message': 'Failed'})






class MyOrders(Resource):
    @jwt_required(fresh=True)
    def __init__(self):
         self.sql = "select * from orders where order_id = %s"
         self.connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')

         self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def post(self):
          # try:
               json = request.json
               order_id = json['order_id']

               self.cursor.execute(self.sql, order_id)
               count = self.cursor.rowcount
               if count == 0:
                    return jsonify({'message': 'No Order'})
               else:
                    orders = self.cursor.fetchall()

                    import json
                    jsonStr = json.dumps(orders, indent=1, sort_keys=True, default=str)
                    # then covert json string to json object
                    return json.loads(jsonStr)


          # except Exception as e:
          #      return jsonify({'message': e})

class MakePayment(Resource):
    def post(self):
        data = request.json
        invoice_no = data["invoice_no"]
        total_amount = data["total_amount"]
        phone = data["phone"]
        mpesa_payment(total_amount, phone, invoice_no)
        return jsonify({"message":"Payment Successful"})
