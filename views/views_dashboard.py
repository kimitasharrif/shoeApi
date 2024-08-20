# Import Required modules
import pymysql
from flask_restful import *
from flask import *
from functions import *
import pymysql.cursors

# import JWT Packages
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token


import os
import pymysql
from flask import request, jsonify
from flask_restful import Resource
from werkzeug.utils import secure_filename


# Define the directory where you want to save uploaded files
UPLOAD_FOLDER = '/home/SherrifShoe/mysite/static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AddShoeWithPhoto(Resource):
    def post(self):
        # Get shoe details from the request
        data = request.form.to_dict()
        category_id = data.get("category_id")
        name = data.get("name")
        price = data.get("price")
        description = data.get("description")
        brand = data.get("brand")
        quantity = data.get("quantity")  # Get quantity from the request

        # Handle file upload
        if 'file' not in request.files:
            return jsonify({"Message": "No file part"})

        file = request.files['file']

        if not category_id or not name or not price or not description or not brand or not quantity or not file:
            return jsonify({"Message": "All fields and file are required"})

        if file.filename == '':
            return jsonify({"Message": "No selected file"})

        if not allowed_file(file.filename):
            return jsonify({"Message": "Invalid file type"})

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Construct the URL path for the image
        base_url = "https://sherrifshoe.pythonanywhere.com/static/images/"
        photo = base_url + filename

        # Connect to the database
        connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
        cursor = connection.cursor()

        try:
            # Insert shoe details into the database
            insert_shoe_sql = """
                INSERT INTO shoes (category_id, name, price, description, brand, photo, quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_shoe_sql, (category_id, name, price, description, brand, photo, quantity))
            connection.commit()

            return jsonify({"Message": "Shoe and photo added successfully"})
        except Exception as e:
            connection.rollback()
            print(e)  # Log the exception for debugging
            return jsonify({"Message": "Shoe and photo not added"})
        finally:
            cursor.close()
            connection.close()


class DeleteShoe(Resource):
    def delete(self):
        # Get the shoe_id from the request
        shoe_id = request.args.get('shoe_id')

        if not shoe_id:
            return jsonify({"Message": "Shoe ID is required"})

        # Connect to the database
        connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
        cursor = connection.cursor()

        try:
            # Fetch the photo URL from the database
            fetch_photo_sql = "SELECT photo FROM shoes WHERE shoe_id = %s"
            cursor.execute(fetch_photo_sql, (shoe_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"Message": "Shoe not found"})

            photo_url = result[0]

            # Extract the filename from the photo URL
            filename = photo_url.split("/")[-1]

            # Delete the shoe from the database
            delete_shoe_sql = "DELETE FROM shoes WHERE shoe_id = %s"
            cursor.execute(delete_shoe_sql, (shoe_id,))
            connection.commit()

            # Delete the photo file from the server
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

            return jsonify({"Message": "Shoe and photo deleted successfully"})
        except Exception as e:
            connection.rollback()
            print(e)  # Log the exception for debugging
            return jsonify({"Message": "Shoe not deleted"})
        finally:
            cursor.close()
            connection.close()




class DeleteAllShoes(Resource):
    def delete(self):
        # Connect to the database
        connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',
                                     password='shoe1234', database='SherrifShoe$default')
        cursor = connection.cursor()

        try:
            # Fetch all photo URLs from the database
            fetch_photos_sql = "SELECT photo FROM shoes"
            cursor.execute(fetch_photos_sql)
            photos = cursor.fetchall()

            # Delete all shoes from the database
            delete_all_shoes_sql = "DELETE FROM shoes"
            cursor.execute(delete_all_shoes_sql)
            connection.commit()

            # Delete all photo files from the server
            for photo in photos:
                photo_url = photo[0]
                filename = photo_url.split("/")[-1]
                file_path = os.path.join(UPLOAD_FOLDER, filename)

                if os.path.exists(file_path):
                    os.remove(file_path)

            return jsonify({"Message": "All shoes and photos deleted successfully"})
        except Exception as e:
            connection.rollback()
            print(e)  # Log the exception for debugging
            return jsonify({"Message": "Failed to delete all shoes"})
        finally:
            cursor.close()
            connection.close()




class AddCategoty(Resource):
     @jwt_required(fresh=True) # Refresh Token
     def post(self):
          json = request.json
          category_name= json['category_name']
        #   connection = pymysql.connect(host='localhost', user='root', password='', database='shoeapp')
          connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
          cursor = connection.cursor()
          # Insert Data
          sql = ''' Insert into category(category_name)
          values(%s) '''
          # Provide Data
          data = (category_name)
          try:
               cursor.execute(sql, data)
               connection.commit()
               return jsonify({'message': 'Category Added'})
          except:
               connection.rollback()
               return jsonify({'message': 'Failed. Try Again'})

class UpdateCategory(Resource):
    @jwt_required(fresh=True)  # Requires a valid JWT token
    def put(self):
        data = request.json
        category_id = data.get('category_id')
        new_name = data.get('category_name')

        connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
        cursor = connection.cursor()

        try:
            sql = "UPDATE categories SET category_name = %s WHERE category_id = %s"
            cursor.execute(sql, (new_name, category_id))
            connection.commit()
            return jsonify({'message': 'Category updated successfully'})
        except Exception as e:
            connection.rollback()
            return jsonify({'message': 'Failed to update category', 'error': str(e)})
        finally:
            connection.close()






class AdminSignup(Resource):
    def post(self):
        json = request.json
        username = json['username']
        email = json['email']
        phone = json['phone']
        password = json['password']

        # Check Password
        response = passwordValidity(password)
        if response:
            if check_phone(phone):
                # connection = pymysql.connect(host='localhost',
                #                                 user='root',
                #                                 password='',
                #                                 database='shoeapp')
                connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
                cursor = connection.cursor()
                sql = '''insert into admin(username, email,
                phone, password) values(%s, %s, %s, %s)'''

                # Data
                data = (username, email, encrypt(phone),
                        hash_password(password))
                try:
                    cursor.execute(sql, data)
                    connection.commit()
                    code = gen_random(4)
                    send_sms(phone, '''Thank you for Joining Shoeapp.
                    Your Secret No: {}. Do not share.'''.format(code))
                    return jsonify({'message': 'Thank you for Joining Shoeapp'})
                except:
                    connection.rollback()
                    return jsonify({'message': 'Not OK'})

            else:
                return jsonify({'message': 'Invalid Phone Enter +254'})
        else :
            return jsonify({'message': response})


class AdminSignin(Resource):
    def post(self):
        json = request.json
        username = json['username']
        password = json['password']

        sql = "select * from admin where username = %s"
        # connection = pymysql.connect(host='localhost',
        #                                         user='root',
        #                                         password='',
        #                                         database='shoeapp')

        connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, username)
        count = cursor.rowcount
        if count == 0:
            return jsonify({'message': 'Username does Not exist'})
        else:
            admin = cursor.fetchone()
            hashed_password = admin['password']
            # Verify
            if hash_verify(password, hashed_password):
                # TODO JSON WEB Tokens
                       access_token = create_access_token(identity=username,
                                                          fresh=True)

                       return jsonify({'message': admin,
                                       'access_token': access_token})
            else:
                       return jsonify({'message': 'Login Failed'})



class AdminProfile(Resource):
     @jwt_required(fresh=True)
     def post(self):
          json = request.json
          admin_id = json['admin_id']
          sql = "select * from admin where admin_id = %s"
        #   connection = pymysql.connect(host='localhost',
        #                                         user='root',
        #                                         password='',
        #                                         database='shoeapp')

          connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql, admin_id)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'No Such Admin'})
          else:
               admin = cursor.fetchone()
               return jsonify({'message': admin})

class Orders(Resource):
     @jwt_required(fresh=True)
     def post(self):
          sql = "select * from orders"
        #   connection = pymysql.connect(host='localhost',
        #                                         user='root',
        #                                         password='',
        #                                         database='shoeapp')
          connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'No orders'})
          else:
               orders  = cursor.fetchall()
               return jsonify(orders)


class Categories(Resource):
     @jwt_required(fresh=True)
     def post(self):
          sql = "select * from category"
        #   connection = pymysql.connect(host='localhost',
        #                                         user='root',
        #                                         password='',
        #                                         database='shoeapp')
          connection = pymysql.connect(host='SherrifShoe.mysql.pythonanywhere-services.com', user='SherrifShoe',password='shoe1234',database='SherrifShoe$default')
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute(sql)
          count = cursor.rowcount
          if count == 0:
               return jsonify({'message': 'No categories'})
          else:
               categories  = cursor.fetchall()
               return jsonify(categories)


