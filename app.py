from flask import*
from flask_restful import Api
app = Flask(__name__)
import os
api = Api(app)
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_cors import CORS
CORS(app)

# SET UP JWT
app.secret_key="dfgjvnosihfgilfjshfeudfljaweio;rhf aweu;hfiwea hfuetgeruoa;ghfpe___RGARNgfguyrg"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)


# endpoints/ routes

from views.views import UserSignup,UserSignin,UserProfile, ChangePassword, Locations, Shoes, MakeOrder, MakePayment,MyOrders, Shoes


api.add_resource(UserSignup, '/api/usersignup')
api.add_resource(UserSignin, '/api/usersignin')
api.add_resource(UserProfile, '/api/userprofile')
api.add_resource(ChangePassword, '/api/changepass')
api.add_resource(Locations, '/api/location')
api.add_resource(Shoes, '/api/shoes')
api.add_resource(MakeOrder, '/api/makeorder')
api.add_resource(MyOrders, '/api/myorders')
api.add_resource(MakePayment, '/api/payment')




from views.views_dashboard import AddShoeWithPhoto,AdminSignup, AdminSignin, AdminProfile, AddCategoty, Orders, Categories,UpdateCategory,DeleteAllShoes,DeleteShoe
api.add_resource(AddShoeWithPhoto, '/api/addshoe')
api.add_resource(DeleteShoe, '/api/deleteshoe')
api.add_resource(DeleteAllShoes, '/api/deleteallshoe')
api.add_resource(AddCategoty, '/api/addcategory')
api.add_resource(AdminSignup, '/api/adminsignup')
api.add_resource(AdminSignin, '/api/adminsignin')
api.add_resource(AdminProfile, '/api/adminprofile')
api.add_resource(Orders, '/api/orders')
api.add_resource(Categories, '/api/categories')
api.add_resource(UpdateCategory, '/api/updatecategory')






# if __name__ =='__main__':
#     app.run(debug=True)