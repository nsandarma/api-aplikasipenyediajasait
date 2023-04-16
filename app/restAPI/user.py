import datetime
from .. import app,api,Resource, request,db,create_refresh_token,create_access_token,jwt_required,response
from .. import UserModel,ClientModel


class User(Resource):
    def get(self):
        data = [user.to_json_serial() for user in UserModel.query.all()]
        return data,200
    def post(self):
        username = request.form['username']
        password = request.form['password']
        try:
            u = UserModel(username=username)
            u.setPassword(password)
            db.session.add(u)
            db.session.commit()
            return {'msg':'success insert !'},200
        except Exception as e:
            return {'msg':str(e)},404
    def delete(self):
        username = request.args['username']
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return {'msg':'user anda tidak ditemukan !'},404
        db.session.delete(user)
        db.session.commit()
        return {'msg':'success deleted !'},200
    def put(self):
        username = request.args['username']
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return {'msg':'data tidak ada !'},404
        username = request.form['username']
        password = request.form['password']
        
        user.userame = username
        user.setPassword(password)

        db.session.commit()
        return {'msg':'success update!'},200


class Login(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']
        role = request.args['role']
        if role == 'client':
            c = ClientModel.query.filter_by(username=username).first()
            if not c or not c.checkPassword(password):
                return response(msg='username anda tidak ditemukan or password anda salah ! 1',status=False,data=[None])
            return response(msg='Anda berhasil Login ! role <user>',status=True,data=c.to_json_serial())
        elif role =='user':
            u = UserModel.query.filter_by(username=username).first()
            if not u or not u.checkPassword(password):
                return response(msg='username anda tidak ditemukan or password anda salah ! 2',status=False,data=[None])
            return response(msg=f'Anda berhasil Login ! role <client>',status=True,data=u.to_json_serial())
        else:
            return response(msg='Bad Request !',status=False,data=[None]),404

class Register(Resource):
    def post(self):
        role = request.args['role']
        if role == 'user':
            username = request.form['username']
            password = request.form['password']
            try:
                u = UserModel(username=username)
                u.setPassword(password)
                db.session.add(u)
                db.session.commit()
                return response(msg='anda berhasil mendaftar !',status=True,data=[u.to_json_serial()])
            except Exception as e:
                return response(msg=str(e),status=False,data=[None]),404
        elif role == 'client':
            username = request.form['username']
            password = request.form['password']
            alamat = request.form['alamat']
            nik = request.form['nik']
            jenis_kelamin = request.form['jenis_kelamin']
            portofolio = request.form['portofolio']
            email = request.form['email']
            nama = request.form['nama']
            
            try:
                u = ClientModel(username=username,alamat=alamat,nik=nik,jenis_kelamin=jenis_kelamin,portofolio=portofolio,email=email,nama=nama)
                u.setPassword(password)
                
                db.session.add(u)
                db.session.commit()
                return response(msg='anda berhasil mendaftar !',status=True,data=[u.to_json_serial()])
            except Exception as e:
                return response(msg=f'{e}',status=False,data=[None]),404

        
class Client(Resource):
    def get(self):
        data = [user.to_json_serial() for user in ClientModel.query.all()]
        return data,200
    def put(self):
        username = request.args['username']
        user = UserModel.query.filter_by(username=username).first()
        userData = ClientModel.query.filter_by(username=username).first()
        if not user or not userData:
            return response(msg='username anda tidak ditemukan !',status=False,data=[None])
        try:
            data = request.json['data']
            user.username = data['username']
            password = data['password']
            user.setPassword(password)
            userData.username = data['username']
            userData.alamat = data['alamat']
            userData.nik = data['nik']
            userData.jenis_kelamin = data['jenis_kelamin']
            userData.portofolio = data['portofolio']
            userData.email = data['email']
            userData.nama = data['nama']
            db.session.commit()
            return response(msg=f'data {data["username"]} berhasil diubah !',status=True,data=[userData.to_json_serial()])
        except Exception as e:
            return response(msg=str(e),status=False,data=[None])

        

class Display(Resource):
    def get(self):
        user = [user.to_json_serial() for user in UserModel.query.all()]
        client = [user.to_json_serial() for user in ClientModel.query.all()]

        data = {'user':user,'client':client}
        return response(msg='berhasil get all data',status=True,data=data)
    def delete(self):
        try:
            UserModel.query.delete()
            ClientModel.query.delete()
            db.session.commit()
            return response(msg='data berhasil dihapus !',status=True,data=[None])
        except Exception as e:
            return response(msg=str(e),status=False,data=[None])
        

api.add_resource(Client,'/client')
api.add_resource(Display,'/display')
api.add_resource(User,'/user')
api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
