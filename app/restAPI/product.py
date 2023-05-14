from app.models import ClientModel, UserModel
from .. import api, app, ProductModel, Resource, response, request, ProductModel, db


# TODO : Clear
class Product(Resource):
    def get(self):
        try:
            id = request.args["id_product"]
            product = ProductModel.query.filter_by(id=id).first()
            if not product:
                return (
                    response(
                        msg="product anda tidak ditemukan !", status=False, data=[]
                    ),
                    404,
                )
            return (
                response(
                    msg="berhasil get single product by id_product",
                    status=True,
                    data=[product.to_json_serial()],
                ),
                200,
            )
        except:
            kategori = request.args["kategori"]
            if kategori not in ["WD", "MD", "UI"]:
                return (
                    response(
                        msg="Masukkan kategori product yang sesuai format [WD,MD,UI]!",
                        status=False,
                        data=[],
                    ),
                    400,
                )
            data = [
                p.to_json_serial()
                for p in ProductModel.query.filter_by(kategori=kategori).all()
            ]
            return (
                response(
                    msg="berhasil get all data product by kategori ",
                    status=True,
                    data=data,
                ),
                200,
            )

    def post(self):
        username = request.args["username"]
        u = ClientModel.query.filter_by(username=username).first()
        if not u:
            return (
                response(msg="username anda tidak ditemukan !", status=False, data=[]),
                404,
            )
        productName = request.form["productName"]
        price = request.form["price"]
        kategori = request.form["kategori"]
        if kategori not in ["WD", "MD", "UI"]:
            return (
                response(
                    "anda salah memasukkan kategori, masukkan kategori sesuai format !",
                    status=False,
                    data=[],
                ),
                400,
            )
        keterangan = request.form["keterangan"]
        try:
            p = ProductModel(
                username=username,
                productName=productName,
                price=price,
                keterangan=keterangan,
                kategori=kategori,
            )
            db.session.add(p)
            db.session.commit()
            return (
                response(
                    msg=f"berhasil add data product",
                    status=True,
                    data=p.to_json_serial(),
                ),
                200,
            )
        except Exception as e:
            return response(msg=str(e), status=False, data=[]), 404

    def put(self):
        id = request.args["id_product"]
        # username = request.args['username']
        p = ProductModel.query.filter_by(id=id).first()
        if not p:
            return response(msg="product tidak ditemukan !", status=False, data=[]), 404
        productName = request.form["productName"]
        price = request.form["price"]
        kategori = request.form["kategori"]
        keterangan = request.form["keterangan"]
        try:
            p.productName = productName
            p.price = price
            p.kategori = kategori
            p.keterangan = keterangan
            db.session.commit()
            return response(
                msg=f"product <id:{p.id}> berhasil di ubah !",
                status=True,
                data=[p.to_json_serial()],
            )
        except Exception as e:
            return response(msg=str(e), status=False, data=[]), 404

    def delete(self):
        id = request.args["id_product"]
        p = ProductModel.query.filter_by(id=id).first()
        if not p:
            return (
                response(msg=f"product tidak ditemukan !", status=False, data=[]),
                404,
            )
        db.session.delete(p)
        db.session.commit()
        return response(
            msg=f"product <id:{p.id}> berhasil dihapus !",
            status=True,
            data=[p.to_json_serial()],
        )


api.add_resource(Product, "/product")


# TODO : Clear
class ProductByUsername(Resource):
    def get(self):
        username = request.args["username"]
        if not ClientModel.query.filter_by(username=username).first():
            return (
                response(msg="username anda tidak ditemukan !", status=False, data=[]),
                404,
            )

        data = [
            p.to_json_serial()
            for p in ProductModel.query.filter_by(username=username).all()
        ]
        return response(
            msg=f"berhasil get all data product by username:{username}",
            status=True,
            data=data,
        )


class ProductDisplay(Resource):
    def get(self):
        data = [p.to_json_serial() for p in ProductModel.query.all()]
        return response(msg="Get all data product", status=True, data=data), 200

    def delete(self):
        data = ProductModel.query.all()
        db.session.delete(data)
        db.session.commit()
        return response(
            msg="Data product berhasil di hapus semua !", status=True, data=[]
        )


api.add_resource(ProductByUsername, "/productByUsername")
api.add_resource(ProductDisplay, "/product/display")
