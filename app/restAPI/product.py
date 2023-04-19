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


api.add_resource(Product,'/product')


