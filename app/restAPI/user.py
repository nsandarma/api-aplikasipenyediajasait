import datetime
from .. import app, api, Resource, request, db, response
from .. import UserModel, ClientModel


# TODO:Clear
class User(Resource):
    def get(self):
        try:
            username = request.args["username"]
            data = UserModel.query.filter_by(username=username).first()
            if not data:
                return (
                    response(msg="data anda tidak ditemukan !", status=False, data=[]),
                    404,
                )
            return (
                response(
                    msg=f"Berhasil get single data user <username:{data.username}>",
                    status=True,
                    data=[data.to_json_serial()],
                ),
                200,
            )
        except:
            data = [user.to_json_serial() for user in UserModel.query.all()]
            return (
                response(msg="berhasil get all data user", status=True, data=data),
                200,
            )

    def delete(self):
        username = request.args["username"]
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return (
                response(msg="data anda tidak ditemukan !", status=False, data=[]),
                404,
            )
        db.session.delete(user)
        db.session.commit()
        return (
            response(
                msg=f"berhasil hapus single user <username:{username}>",
                status=True,
                data=[user.to_json_serial()],
            ),
            200,
        )

    def put(self):
        username = request.args["username"]
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return (
                response(msg="data anda tidak ditemukan !", status=False, data=[]),
                404,
            )
        username = request.form["username"]
        password = request.form["password"]

        user.username = username
        user.setPassword(password)
        db.session.commit()
        return (
            response(
                msg=f"berhasil update single user <username:{username}>",
                status=True,
                data=[user.to_json_serial()],
            ),
            200,
        )


api.add_resource(User, "/user")


# TODO:Clear
class Login(Resource):
    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        role = request.args["role"]
        if role == "client":
            c = ClientModel.query.filter_by(username=username).first()
            if not c or not c.checkPassword(password):
                return (
                    response(
                        msg="username anda tidak ditemukan or password anda salah ! <client>",
                        status=False,
                        data=[],
                    ),
                    404,
                )
            return response(
                msg="Anda berhasil Login ! role <client>",
                status=True,
                data=[c.to_json_serial()],
            )
        elif role == "user":
            u = UserModel.query.filter_by(username=username).first()
            if not u or not u.checkPassword(password):
                return (
                    response(
                        msg="username anda tidak ditemukan or password anda salah ! <user>",
                        status=False,
                        data=[],
                    ),
                    404,
                )
            return response(
                msg=f"Anda berhasil Login ! role <user>",
                status=True,
                data=[u.to_json_serial()],
            )
        else:
            return response(msg="Bad Request !", status=False, data=[]), 404


api.add_resource(Login, "/login")


# TODO:Clear
class Register(Resource):
    def post(self):
        role = request.args["role"]
        if role == "user":
            username = request.form["username"]
            password = request.form["password"]
            try:
                u = UserModel(username=username)
                u.setPassword(password)
                db.session.add(u)
                db.session.commit()
                return response(
                    msg="anda berhasil mendaftar !",
                    status=True,
                    data=[u.to_json_serial()],
                )
            except Exception as e:
                return response(msg=str(e), status=False, data=[]), 404
        elif role == "client":
            username = request.form["username"]
            password = request.form["password"]
            alamat = request.form["alamat"]
            nik = request.form["nik"]
            jenis_kelamin = request.form["jenis_kelamin"]
            portofolio = request.form["portofolio"]
            email = request.form["email"]
            nama = request.form["nama"]

            try:
                u = ClientModel(
                    username=username,
                    alamat=alamat,
                    nik=nik,
                    jenis_kelamin=jenis_kelamin,
                    portofolio=portofolio,
                    email=email,
                    nama=nama,
                )
                u.setPassword(password)

                db.session.add(u)
                db.session.commit()
                return response(
                    msg="anda berhasil mendaftar !",
                    status=True,
                    data=[u.to_json_serial()],
                )
            except Exception as e:
                return response(msg=f"{e}", status=False, data=[]), 404


api.add_resource(Register, "/register")


# TODO:Clear
class Client(Resource):
    def get(self):
        try:
            username = request.args["username"]
            data = ClientModel.query.filter_by(username=username).first()
            if not data:
                return (
                    response(msg="data anda tidak ditemukan !", status=False, data=[]),
                    404,
                )
            return (
                response(
                    msg="berhasil get single data client <username:{}>".format(
                        data.username
                    ),
                    status=True,
                    data=[data.to_json_serial()],
                ),
                200,
            )
        except:
            data = [user.to_json_serial() for user in ClientModel.query.all()]
            return (
                response(msg="berhasil get all data client", status=True, data=data),
                200,
            )

    def put(self):
        username = request.args["username"]
        client = ClientModel.query.filter_by(username=username).first()
        if not client:
            return (
                response(msg="data anda tidak ditemukan !", status=False, data=[]),
                404,
            )
        client.username = request.form["username"]
        client.nama = request.form["nama"]
        client.jenis_kelamin = request.form["jenis_kelamin"]
        client.alamat = request.form["alamat"]
        client.email = request.form["email"]
        client.portofolio = request.form["portofolio"]
        client.nik = request.form["nik"]
        password = request.form["password"]
        client.setPassword(password)
        db.session.commit()
        return (
            response(
                msg=f"berhasil update single client <username:{client.username}>",
                status=True,
                data=[client.to_json_serial()],
            ),
            200,
        )

    def delete(self):
        username = request.args["username"]
        client = ClientModel.query.filter_by(username=username).first()
        if not client:
            return (
                response(msg="data anda tidak ditemukan !", status=False, data=[]),
                404,
            )
        db.session.delete(client)
        db.session.commit()
        return (
            response(
                msg=f"berhasil hapus single client <username:{username}>",
                status=True,
                data=[client.to_json_serial()],
            ),
            200,
        )


api.add_resource(Client, "/client")


# TODO : Clear
class Display(Resource):
    def get(self):
        user = [user.to_json_serial() for user in UserModel.query.all()]
        client = [user.to_json_serial() for user in ClientModel.query.all()]

        data = {"user": user, "client": client}
        return response(msg="berhasil get all data", status=True, data=data)

    def delete(self):
        try:
            UserModel.query.delete()
            ClientModel.query.delete()
            db.session.commit()
            return response(msg="data berhasil dihapus !", status=True, data=[None])
        except Exception as e:
            return response(msg=str(e), status=False, data=[None])


api.add_resource(Display, "/display/role")
