import datetime
from .. import app,api,Resource, request,db,create_refresh_token,create_access_token,jwt_required,response
from .. import UserModel,UserDataModel


class User(Resource):
    def get(self):
        data = [user.to_json_serial() for user in UserModel.query.all()]
        return data,200
    def post(self):
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        try:
            u = UserModel(username=username,role=role)
            u.setPassword(password)
            db.session.add(u)
            db.session.commit()
            return {'msg':'success insert !'},200
        except Exception as e:
            return {'msg':str(e)},404
    def delete(self):
        id = request.args['id']
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            return {'msg':'user anda tidak ditemukan !'},404
        db.session.delete(user)
        db.session.commit()
        return {'msg':'success deleted !'},200
    def put(self):
        id = request.args['id']
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            return {'msg':'data tidak ada !'},404
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        user.userame = username
        user.setPassword(password)
        user.role = role
        db.session.commit()
        return {'msg':'success update!'},200


class Login(Resource):
    # def post(self):
    #     username = request.form['username']
    #     password = request.form['password']
    #     user = UserModel.query.filter_by(username=username).first()
    #     if not user:
    #         return {"msg":'username anda tidak terdaftar'},400
    #     if not user.checkPassword(password):
    #         return {'msg':'password anda salah !'},404
    #     data = user.to_json_serial()
    #     expires = datetime.timedelta(hours=6)
    #     expires_refresh = datetime.timedelta(days=7)
    #     access_token = create_access_token(data,expires_delta=expires)
    #     refresh_token = create_refresh_token(data,expires_delta=expires_refresh)
    #     return {'msg':'success Login !','access_token':access_token},200
    def post(self):
        username = request.form['username']
        password = request.form['password']
        user = UserModel.query.filter_by(username=username).first()
        if not user or not user.checkPassword(password):
            res =  response(msg="username anda tidak ditemukan & password anda salah",status=False,data=None)
            return res,404
        data = user.to_json_serial()
        data['time'] = datetime.datetime.now().isoformat()
        return response(msg='Anda berhasil Login !',status=True,data=data),200

class Register(Resource):
    def post(self):
        role = request.args['role']
        if role == 'user':
            username = request.form['username']
            password = request.form['password']
            try:
                u = UserModel(username=username,role='user')
                u.setPassword(password)
                db.session.add(u)
                db.session.commit()
                return response(msg='anda berhasil mendaftar !',status=True,data=[u.to_json_serial()])
            except Exception as e:
                return response(msg=str(e),status=False,data=[None]),404
        elif role == 'client':
            data = request.json['data']
            try:
                u = UserDataModel(username=data['username'],nama=data['nama'],alamat=data['alamat'],
                                  nik=data['nik'],jenis_kelamin=data['jenis_kelamin'],portofolio=data['portofolio'],
                                  email=data['email']
                                  )
                u1 = UserModel(username=data['username'],password=data['password'],role='client')
                db.session.add(u1,u)
                db.session.commit()
                return response(msg='anda berhasil mendaftar !',status=True,data=[data])
            except Exception as e:
                return response(msg=f'{e}',status=False,data=[None]),404

        
class UserData(Resource):
    def get(self):
        data = [user.to_json_serial() for user in UserDataModel.query.all()]
        return data,200
    def post(self):
        username = request.args['username']
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return {'msg':"username anda tidak ditemukan !"},404
        data = request.json['data']
        try:

            u = UserDataModel(username=username,nama=data['nama'],alamat=data['alamat'],
                              nik=data['nik'],jenis_kelamin=data['jenis_kelamin'],portofolio=data['portofolio'],
                              email=data['email']
                              )
            db.session.add(u)
            db.session.commit()
            return {'msg':'success insert !'},200
        except Exception as e:
            return {'msg':str(e)},404


        return data,200
        

class Display(Resource):
    def get(self):
        user = [user.to_json_serial() for user in UserModel.query.all()]
        client = [user.to_json_serial() for user in UserDataModel.query.all()]

        data = {'user':user,'client':client}
        return response(msg='berhasil get all data',status=True,data=data)

api.add_resource(UserData,'/user/data')
api.add_resource(Display,'/display')
api.add_resource(User,'/user')
api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
