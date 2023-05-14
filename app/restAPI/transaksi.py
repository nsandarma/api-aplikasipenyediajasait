from .. import Api, Resource, request, db, app, api, response
from app.models import UserModel, ClientModel, ProductModel, TransaksiModel, NegoModel
import datetime


class Nego(Resource):
    def get(self):
        role = request.args['role']
        username = request.args["username"]
        if role == 'client':
            c = ClientModel.query.filter_by(username=username).first()
            if not c:
                return response(msg='username anda tidak ditemukan !',status=False,data=[]),404
            data = NegoModel.query.filter_by(client=username).all()
        else:
            u = UserModel.query.filter_by(username=username).first()
            if not u:
                return (
                    response(msg="username anda tidak ditemukan !", status=False, data=[]),
                    404,
                )
            data = NegoModel.query.filter_by(user=username).all()

        data = [n.to_json_serial() for n in data]
        return (
            response(msg=f"Get data nego <username:{username}>", status=True, data=data),
            200,
        )

    def post(self):
        user = request.args["username"]
        u = UserModel.query.filter_by(username=user).first()
        if not u:
            return (
                response(msg="username anda tidak ditemukan !", status=False, data=[]),
                404,
            )

        id = request.args["id_product"]
        p = ProductModel.query.filter_by(id=id).first()
        if not p:
            return response(msg="product tidak ditemukan !", status=False, data=[]), 404

        # WARNING :for test
        deadline = request.form["deadline"]
        deadline_ = datetime.datetime.now()
        price = request.form["price"]
        desc = request.form["description"]
        client = p.username
        productName = p.productName

        n = NegoModel(
            productName=productName,
            deadline=deadline_,
            user=user,
            client=client,
            price_awal=p.price,
            status="pending",
            price=price,
            description=desc,
        )
        db.session.add(n)
        db.session.commit()
        return (
            response(
                msg="nego berhasil dibuat !", status=True, data=n.to_json_serial()
            ),
            200,
        )
    def delete(self):
        id = request.args['id_nego']
        n = NegoModel.query.filter_by(id=id).first()
        if not n:
            return response(msg='data anda tidak ditemukan !',status=False,data=[]),404
        db.session.delete(n)
        db.session.commit()
        return response(msg='data anda berhasil dihapus !',status=True,data=n.to_json_serial()),200
    


api.add_resource(Nego, "/nego")


class NegoEnd(Resource):
    def post(self):
        id_nego = request.args["id_nego"]
        q = NegoModel.query.filter_by(id=id_nego).first()
        p = ProductModel.query.filter_by(productName=q.productName).first()
        status = request.form["status"]
        if status == "diterima":
            q.status = "accept"
            resi = f"{id_nego}/{p.id}/{p.kategori}/{q.user}/{q.client}"
            t = TransaksiModel(
                productName=q.productName, status="Sedang dikerjakan !", resi=resi
            )
            db.session.add(t)
            db.session.commit()
            return response(
                msg=f"resi : {resi}", status=True, data=[t.to_json_serial()]
            )
        elif status== 'ditolak':
            q.status = "reject"
            db.session.commit()
            return response(
                msg="nego ditolak !", status=False, data=[q.to_json_serial()]
            )
        else:
            return response(msg='status anda tidak diketahui !',status=False,data=[]),400


api.add_resource(NegoEnd, "/nego/end")


class DisplayNego(Resource):
    def get(self):
        nego = NegoModel.query.all()
        data = [n.to_json_serial() for n in nego]
        return response(msg="get all nego", status=True, data=data), 200

    def delete(self):
        nego = NegoModel.query.all()
        db.session.delete(nego)
        db.session.commit()
        return response(msg="berhasil hapus all data nego", status=True, data=[]), 200


api.add_resource(DisplayNego, "/nego/display")

