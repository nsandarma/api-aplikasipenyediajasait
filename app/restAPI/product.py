from .. import api,app,ProductModel,Resource,response,request,ProductModel


class Product(Resource):
    def get(self):
        data = [p.to_json_serial() for p in ProductModel.query.all()]
        return response(msg='berhasil get all data product',status=True,data=data),200
    def post(self):
        username = request.args['username']
        productName = request.form['productName']
        price = request.form['price']
        kategori = request.form['kategori']
        pass


