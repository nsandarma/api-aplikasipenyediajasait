from . import app,UserModel,ClientModel,NegoModel,TransaksiModel,response,db
from flask import render_template,redirect,request,session,url_for
from babel import numbers

@app.route('/admin')
def admin():
    if session.get('login'):

        total_transaksi = [int(t.to_json_serial()['price']) for t in TransaksiModel.query.all() if t.status==2]
        pending_transaksi = [t.to_json_serial() for t in TransaksiModel.query.all() if t.status==1]
        total_pemasukan = sum([5/100 * t for t in total_transaksi])
        sum_price = numbers.format_currency(currency='Rp ',number=sum(total_transaksi))
        total_pemasukan = numbers.format_currency(currency='Rp ',number=total_pemasukan)
        data = {'sum_price':sum_price,'total_pemasukan':total_pemasukan,'jumlah_transaksi':len(total_transaksi),'pending_transaksi':len(pending_transaksi)}
        menunggu_pembayaran = [t.to_json_serial() for t in TransaksiModel.query.all() if t.status==0]
        
        return render_template('index.html',data=data,menunggu_pembayaran=menunggu_pembayaran)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/login',methods=["GET",'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password == 'admin':
            session['login'] = True
            return redirect(url_for('admin'))
        else:
            return "password anda salah"
    return render_template('login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin'))

@app.route('/admin/bayar/<id_transaksi>')
def bayar(id_transaksi):
    t = TransaksiModel.query.filter_by(id=id_transaksi).first()
    if not t:
        return "tidak ada resi ditemukan"
    t.status = 1
    db.session.commit()
    return redirect('/admin')

@app.route('/admin/tables/<request>')
def tables(request):
    if request == 'all':
        data = [t.to_json_serial() for t in TransaksiModel.query.all()]
        title = 'Semua data transaksi'
    elif request == 'mp':
        data = [t.to_json_serial() for t in TransaksiModel.query.all() if t.status==0]
        title = 'Data Menunggu Pembayaran'
    elif request == 'tp':
        title = 'Data Transaksi Pending'
        data = [t.to_json_serial() for t in TransaksiModel.query.all() if t.status==1]
    else:
        title = 'Data transaksi yang sudah selesai'
        data = [t.to_json_serial() for t in TransaksiModel.query.all() if t.status==2]
    return render_template('tables.html',data=data,title=title)
        

        
        
