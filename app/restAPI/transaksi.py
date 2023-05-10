from .. import Api,Resource,request,db,app
from app.models import UserModel,ClientModel,ProductModel,TransaksiModel,NegoModel,response,api


class Nego(Resource):
    def get(self):
        client = request.args['client']
        try:
            data = [n.to_json_serial() for n in NegoModel.query.filter_by(client=client).all()]
            return response(msg='Get data nego',status=True,data=data),200
        except Exception as e:
            return response(msg=str(e),status=False,data=[]),404
    # def post(self):
    #     user = request.args['user']

    # def put(self):
    #     id_nego = request.args['id_nego']
    #     q = NegoModel.query.filter_by(id=id_nego).first()
        
class NegoEnd(Resource):
    def post(self):
        id_nego = request.args['id_nego']
        q = NegoModel.query.filter_by(id=id_nego).first()
        p = ProductModel.query.filter_by(productName=q.productName).first()
        status = request.form['status']
        if status == 'acc':
            q.status = 'accept'
            resi = f'{id_nego}/{p.id}/{p.kategori}/{q.user}/{q.client}'
            t = TransaksiModel(productName=q.productName,status='Sedang dikerjakan !',resi=resi)
            db.session.add(t)
            db.session.commit()
            return response(msg=f'resi : {resi}',status=True,data=[t.to_json_serial()])
        else:
            q.status = 'reject'
            db.session.commit()
            return response(msg='nego ditolak !',status=False,data=[q.to_json_serial()])

api.add_resource(NegoEnd,'/nego/end')
api.add_resource(Nego,'/nego')
        



        
