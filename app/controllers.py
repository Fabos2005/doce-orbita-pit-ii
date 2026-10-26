import hmac
import secrets
from functools import wraps
from flask import Blueprint,render_template,request,session,redirect,url_for,flash,abort,current_app
from . import models as m
bp=Blueprint('shop',__name__)

def customer(fn):
    @wraps(fn)
    def wrapped(*args,**kwargs):
        if not session.get('uid'):
            flash('Entre na sua conta para continuar.','info');return redirect(url_for('shop.login'))
        return fn(*args,**kwargs)
    return wrapped

def manager(fn):
    @wraps(fn)
    def wrapped(*args,**kwargs):
        if not session.get('admin'):return redirect(url_for('shop.admin_login'))
        return fn(*args,**kwargs)
    return wrapped

@bp.route('/')
def home():return render_template('catalog.html',products=m.catalog(request.args.get('q','')[:100]),query=request.args.get('q','')[:100])

@bp.route('/produto/<int:pid>')
def detail(pid):
    p=m.product(pid)
    if not p or not p['active']:abort(404)
    return render_template('product.html',p=p)

@bp.route('/cadastro',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            if request.form.get('password')!=request.form.get('confirmation'):raise m.ValidationError('As senhas não conferem.')
            uid=m.register(request.form.get('name'),request.form.get('email'),request.form.get('password',''))
            cart=session.get('cart',{});session.clear();session.update(uid=uid,cart=cart,csrf=secrets.token_urlsafe(32))
            flash('Conta criada. Você já pode comprar.','success');return redirect(url_for('shop.home'))
        except m.ValidationError as e:flash(str(e),'error')
    return render_template('auth.html',mode='register',values=request.form)

@bp.route('/entrar',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=m.authenticate(request.form.get('email',''),request.form.get('password',''))
        if user:
            cart=session.get('cart',{});session.clear();session.update(uid=user['id'],cart=cart,csrf=secrets.token_urlsafe(32))
            return redirect(url_for('shop.cart'))
        flash('E-mail ou senha incorretos.','error')
    return render_template('auth.html',mode='login',values=request.form)

@bp.post('/sair')
def logout():session.clear();return redirect(url_for('shop.home'))

@bp.route('/carrinho')
def cart():
    try:rows=m.basket(session.get('cart',{}),allow_unavailable=True)
    except m.ValidationError as e:flash(str(e),'error');rows=[]
    return render_template('cart.html',rows=rows,total=sum(p['subtotal'] for p in rows))

@bp.post('/carrinho/<int:pid>')
def cart_change(pid):
    try:
        cart=dict(session.get('cart',{}));q=m.integer(request.form.get('quantity'),'Quantidade',0,99)
        if request.form.get('action')=='add':q+=cart.get(str(pid),0)
        if q==0:cart.pop(str(pid),None)
        else:
            p=m.product(pid)
            if not p or not p['active']:raise m.ValidationError('Produto indisponível.')
            if q>99 or q>p['stock']:raise m.ValidationError('Quantidade superior ao estoque disponível.')
            if len(cart)>=30 and str(pid) not in cart:raise m.ValidationError('Limite de 30 produtos diferentes no carrinho.')
            cart[str(pid)]=q
        session['cart']=cart;session.pop('checkout_key',None)
        flash('Carrinho atualizado.','success')
    except m.ValidationError as e:flash(str(e),'error')
    return redirect(url_for('shop.cart'))

@bp.route('/finalizar',methods=['GET','POST'])
@customer
def checkout():
    session.setdefault('checkout_key',secrets.token_urlsafe(24))
    if request.method=='POST':
        try:
            if not hmac.compare_digest(session['checkout_key'],request.form.get('request_key','')):raise m.ValidationError('Este formulário expirou. Revise o carrinho.')
            oid=m.checkout(session['uid'],session.get('cart',{}),request.form,session['checkout_key'])
            session['cart']={};session.pop('checkout_key',None)
            return redirect(url_for('shop.order',oid=oid))
        except m.ValidationError as e:flash(str(e),'error')
    try:rows=m.basket(session.get('cart',{}))
    except m.ValidationError as e:
        flash(str(e),'error');return redirect(url_for('shop.cart'))
    if not rows:return redirect(url_for('shop.cart'))
    return render_template('checkout.html',rows=rows,total=sum(p['subtotal'] for p in rows)+800,values=request.form)

@bp.route('/pedidos')
@customer
def orders():return render_template('orders.html',orders=m.db().execute('SELECT * FROM orders WHERE user_id=? ORDER BY id DESC',(session['uid'],)).fetchall(),admin=False)

@bp.route('/pedido/<int:oid>')
@customer
def order(oid):
    o=m.order(oid,session['uid'])
    if not o:abort(404)
    return render_template('order.html',o=o,admin=False)

@bp.post('/pedido/<int:oid>/pagar')
@customer
def pay(oid):
    if not m.order(oid,session['uid']):abort(404)
    try:
        m.pay(oid,session['uid'],request.form.get('method'),request.form.get('result'))
        flash('Simulação registrada: '+request.form['result']+'. Nenhuma cobrança foi realizada.','success')
    except m.ValidationError as e:flash(str(e),'error')
    return redirect(url_for('shop.order',oid=oid))

@bp.post('/pedido/<int:oid>/cancelar')
@customer
def cancel(oid):
    if not m.order(oid,session['uid']):abort(404)
    try:m.cancel(oid,session['uid']);flash('Pedido cancelado. Estoque liberado.','success')
    except m.ValidationError as e:flash(str(e),'error')
    return redirect(url_for('shop.order',oid=oid))

@bp.route('/gestao/entrar',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if hmac.compare_digest(request.form.get('password','').encode(),current_app.config['ADMIN_PASSWORD'].encode()):
            session.clear();session.update(admin=True,csrf=secrets.token_urlsafe(32));return redirect(url_for('shop.admin'))
        flash('Senha de gestão incorreta.','error')
    return render_template('auth.html',mode='admin',values={})

@bp.route('/gestao')
@manager
def admin():return render_template('orders.html',orders=m.db().execute('SELECT * FROM orders ORDER BY id DESC').fetchall(),admin=True)

@bp.route('/gestao/pedido/<int:oid>',methods=['GET','POST'])
@manager
def admin_order(oid):
    if request.method=='POST':
        try:m.advance(oid,request.form.get('expected'));flash('Andamento atualizado.','success')
        except m.ValidationError as e:flash(str(e),'error')
        return redirect(url_for('shop.admin_order',oid=oid))
    o=m.order(oid)
    if not o:abort(404)
    return render_template('order.html',o=o,admin=True)

@bp.route('/gestao/produtos')
@manager
def admin_products():return render_template('admin_products.html',products=m.db().execute('SELECT * FROM products ORDER BY id').fetchall())

@bp.route('/gestao/produto/novo',methods=['GET','POST'])
@bp.route('/gestao/produto/<int:pid>',methods=['GET','POST'])
@manager
def edit_product(pid=None):
    if pid and not m.product(pid):abort(404)
    if request.method=='POST':
        try:m.save_product(request.form,pid);flash('Produto salvo.','success');return redirect(url_for('shop.admin_products'))
        except m.ValidationError as e:flash(str(e),'error')
    return render_template('edit_product.html',p=request.form if request.method=='POST' else (dict(m.product(pid)) if pid else {'active':1,'stock':0}))
