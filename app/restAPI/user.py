import datetime
from .. import app,api,Resource, request,db,create_refresh_token,create_access_token,jwt_required
from .. import UserModel

class User(Resource):
    @jwt_required()
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


class Login(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return {"msg":'username anda tidak terdaftar'},400
        if not user.checkPassword(password):
            return {'msg':'password anda salah !'},404
        data = user.to_json_serial()
        expires = datetime.timedelta(hours=6)
        expires_refresh = datetime.timedelta(days=7)
        access_token = create_access_token(data,expires_delta=expires)
        refresh_token = create_refresh_token(data,expires_delta=expires_refresh)
        return {'msg':'success Login !','access_token':access_token},200




api.add_resource(User,'/api/user')
api.add_resource(Login,'/api')
