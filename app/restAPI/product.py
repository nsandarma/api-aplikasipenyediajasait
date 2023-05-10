from app.models import ClientModel, UserModel
from .. import api,app,ProductModel,Resource,response,request,ProductModel,db


class Product(Resource):
    def get(self):
        try:
            kategori = request.args['kategori']
            data = [p.to_json_serial() for p in ProductModel.query.filter_by(kategori=kategori).all()]
            return response(msg='berhasil get all data product',status=True,data=data),200
        except Exception as e:
            return response(msg='Masukkan kategori product !',status=False,data=[]),400
    def post(self):
        username = request.args['username']
        u = ClientModel.query.filter_by(username=username).first()
        if not u:
            return response(msg='username anda tidak ditemukan !',status=False,data=[]),404
        productName = request.form['productName']
        price = request.form['price']
        kategori = request.form['kategori']
        keterangan = request.form['keterangan']
        
        try:
            p = ProductModel(username=username,productName=productName,price=price,keterangan=keterangan,kategori=kategori)
            db.session.add(p)
            db.session.commit()
            return response(msg=f'product {p.productName} berhasil ditambahkan',status=True,data=p.to_json_serial()),200
        except Exception as e:
            return response(msg=str(e),status=False,data=[]),404
    def put(self):
        username = request.form['username']
        id = request.form['id']
        p = ProductModel.query.filter_by(username).first()
        if not p:
            return response(msg='Product tidak ada didalam database !',status=False,data=[]),404
        productName = request.form['productName']
        price = request.form['price']
        kategori = request.form['kategori']
        keterangan = request.form['keterangan']
        try:
            p.productName = productName
            p.price = price
            p.kategori= kategori
            p.keterangan = keterangan
            db.session.commit()
            return response(msg=f'product {p.id} berhasil di ubah !',status=True,data=p.to_json_serial())
        except Exception as e:
            return response(msg=str(e),status=False,data=[]),404
    def delete(self):
        id = request.form['id']
        p = ProductModel.query.filter_by(id=id).first()
        if not p:
            return response(msg=f'product {id} tidak ditemukan !',status=False,data=[]),404
        db.session.delete(p)
        db.session.commit()
        return response(msg=f'product ''{p.productName}'' berhasil dihapus !',status=True,data=p.to_json_serial())

class ProductByUsername(Resource):
    def get(self):
        username = request.args['username']
        if not ClientModel.query.filter_by(username=username).first():
            return response(msg='username anda tidak ditemukan !',status=False,data=[]),404

        data = [p.to_json_serial() for p in ProductModel.query.filter_by(username=username).all()]
        return response(msg=f'Product dari username {username}',status=True,data=data)
    def delete(self):
        username = request.args['username']
        data = ProductModel.query.filter_by(username=username).all()
        db.session.delete(data)
        db.session.commit()
        return response(msg=f'Product dari {username} berhasil dihapus !',status=True,data=[])

class ProductDisplay(Resource):
    def get(self):
        data = [p.to_json_serial() for p in ProductModel.query.all()]
        return response(msg='Get all data product',status=True,data=data),200
    def delete(self):
        data = ProductModel.query.all()
        db.session.delete(data)
        db.session.commit()
        return response(msg='Data product berhasil di hapus semua !',status=True,data=[])
api.add_resource(Product,'/product')
api.add_resource(ProductByUsername,'/productByUsername')
api.add_resource(ProductDisplay,'/product/display')


