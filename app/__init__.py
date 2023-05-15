from flask import Flask, request, make_response, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


def response(msg, status, data):
    return {"msg": msg, "status": status, "data": data}


from .models import UserModel, ClientModel, ProductModel, TransaksiModel,NegoModel
from .restAPI import user, product, transaksi
from . import admin

class DisplayAll(Resource):
    def get(self):
        u = [u.to_json_serial() for u in UserModel.query.all()]
        c = [c.to_json_serial() for c in ClientModel.query.all()]
        p = [p.to_json_serial() for p in ProductModel.query.all()]
        n = [n.to_json_serial() for n in NegoModel.query.all()]
        t = [t.to_json_serial() for t in TransaksiModel.query.all()]

        data = {'user':u,'client':c,'product':p,'nego':n,'transaksi':t}
        return response(msg='berhasil get all data didalam database !',status=True,data=data)

api.add_resource(DisplayAll,'/display/all')