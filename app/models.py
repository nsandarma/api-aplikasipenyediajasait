from sqlalchemy import DateTime
from . import db, generate_password_hash
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    created_by = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self) -> str:
        return f'Username : {self.username}'
    def setPassword(self,password):
        self.password = generate_password_hash(password)
    def to_json_serial(self):
        return {"id":self.id,"username":self.username,'created_by':self.created_by.isoformat()}
    def checkPassword(self,password):
        return check_password_hash(self.password,password)

class ClientModel(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    nama = db.Column(db.String,nullable=False)
    nik = db.Column(db.String,nullable=False,unique=True)
    alamat = db.Column(db.String,nullable=False)
    portofolio = db.Column(db.String,nullable=False)
    email = db.Column(db.String)
    jenis_kelamin = db.Column(db.String,nullable=False)
    created_by = db.Column(db.DateTime,default=datetime.now())
    
    def setPassword(self,password):
        self.password = generate_password_hash(password)
    def checkPassword(self,password):
        return check_password_hash(self.password,password)
    def __repr__(self):
        return f"nama => {self.nama}"
    def to_json_serial(self):
        return {
            "id":self.id,
            "username":self.username,
                "nama":self.nama,
                "jenis_kelamin":self.jenis_kelamin,
                "nik":self.nik,
                "alamat":self.alamat,
                "email":self.email,
                "portofolio":self.portofolio,
                "created_by":self.created_by.isoformat()
                }

class ProductModel(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer,primary_key=True)
    productName = db.Column(db.String,nullable=False)
    kategori = db.Column(db.String,nullable=False)
    username = db.Column(db.String)
    created_by = db.Column(db.DateTime,default=datetime.now())
    price = db.Column(db.String,nullable=False)
    keterangan = db.Column(db.String)

    def to_json_serial(self):
        return {'id':self.id,
                'productName':self.productName,
                'kategori':self.kategori,
                'username':self.username,
                'created_by':self.created_by,
                'price':self.price,
                'keterangan':self.keterangan,
                'created_by':self.created_by.isoformat()
                }

    



# class TransaksiModel(db.Model):
#     __tablename__ = 'transaksi'
#     resi = db.Column(db.String,nullable=False,unique=True)
#     productName = db.Column(db.String,db.ForeignKey('product.productName'))
#     tenggangWaktu = db.Column(db.DateTime,nullable=False) 
#     status = db.Column(db.Integer,nullable=False)
#
#     def setDurasi(self,tenggang):
#         self.tenggangWaktu = self.tenggangWaktu+timedelta(days=tenggang)
        







