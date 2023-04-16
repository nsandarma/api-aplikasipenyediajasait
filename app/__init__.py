from flask import Flask,request,make_response,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from config import Config
from flask_jwt_extended import create_access_token,create_refresh_token,JWTManager,jwt_required
app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app,db)
jwt = JWTManager(app=app)



def response(msg,status,data):
    data = [data]
    return {"msg":msg,'status':status,'data':data}


from .models import UserModel,ClientModel
from .admin import routes
from .restAPI import user
