"""Persistência e regras de negócio. Valores monetários em centavos inteiros."""
import re
import sqlite3
from pathlib import Path
from flask import g, current_app
from werkzeug.security import generate_password_hash, check_password_hash

class ValidationError(ValueError): pass

def db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], timeout=10)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys=ON')
    return g.db

def close_db(_=None):
    conn=g.pop('db',None)
    if conn: conn.close()

def init_db():
    db().executescript(Path(__file__).with_name('schema.sql').read_text())
    if not db().execute('SELECT 1 FROM products LIMIT 1').fetchone():
        db().executemany('INSERT INTO products(name,description,flavor,allergens,price_cents,stock) VALUES(?,?,?,?,?,?)',[
          ('Chocolate intenso','Massa de cacau com cobertura de chocolate.','Chocolate','Contém leite, ovos e trigo (glúten).',1290,30),
          ('Baunilha delicada','Massa de baunilha e creme suave.','Baunilha','Contém leite, ovos e trigo (glúten).',1190,30),
          ('Morango da casa','Massa de baunilha com cobertura de morango.','Morango','Contém leite, ovos e trigo (glúten).',1390,30)])
        db().commit()

def text(value,label,limit=100,minimum=1):
    value=str(value or '').strip()
    if not minimum<=len(value)<=limit: raise ValidationError(f'{label}: informe de {minimum} a {limit} caracteres.')
    return value

def integer(value,label,low=1,high=99):
    if not re.fullmatch(r'[0-9]+',str(value or '')): raise ValidationError(f'{label}: informe um número inteiro.')
    n=int(value)
    if not low<=n<=high: raise ValidationError(f'{label}: use um valor entre {low} e {high}.')
    return n

def register(name,email,password):
    name=text(name,'Nome',80,2);email=text(email,'E-mail',160,5).lower()
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email): raise ValidationError('Informe um e-mail válido.')
    if not 10<=len(password)<=128: raise ValidationError('A senha deve ter entre 10 e 128 caracteres.')
    try:
        with db():
            return db().execute('INSERT INTO users(name,email,password_hash) VALUES(?,?,?)',(name,email,generate_password_hash(password))).lastrowid
    except sqlite3.IntegrityError: raise ValidationError('Este e-mail já está cadastrado. Entre na sua conta.')

def authenticate(email,password):
    row=db().execute('SELECT * FROM users WHERE email=?',(email.strip().lower(),)).fetchone()
    return row if row and check_password_hash(row['password_hash'],password) else None

def catalog(query=''):
    return db().execute('SELECT * FROM products WHERE active=1 AND (name LIKE ? OR flavor LIKE ?) ORDER BY id',('%'+query+'%','%'+query+'%')).fetchall()

def product(pid): return db().execute('SELECT * FROM products WHERE id=?',(pid,)).fetchone()

def basket(cart,allow_unavailable=False):
    rows=[]
    for pid,qty in cart.items():
        p=product(integer(pid,'Produto',1,2147483647))
        q=integer(qty,'Quantidade')
        if not p or (not p['active'] and not allow_unavailable): raise ValidationError('Um produto do carrinho não está disponível. Remova-o para continuar.')
        rows.append(dict(p,quantity=q,subtotal=p['price_cents']*q))
    return rows

def delivery_address(data):
    out={k:text(data.get(k),label,limit) for k,label,limit in [
      ('recipient','Destinatário',80),('street','Rua',120),('number','Número',12),('district','Bairro',80),('city','Cidade',80),('state','UF',2),('postal_code','CEP',9)]}
    out['complement']=text(data.get('complement',''),'Complemento',100,0)
    out['postal_code']=re.sub(r'\D','',out['postal_code'])
    if not re.fullmatch(r'\d{8}',out['postal_code']): raise ValidationError('CEP: informe oito dígitos.')
    out['state']=out['state'].upper()
    if out['state'] not in 'AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO'.split():raise ValidationError('Informe uma UF válida.')
    return out

def checkout(uid,cart,data,key):
    if not cart: raise ValidationError('Seu carrinho está vazio.')
    address=delivery_address(data)
    conn=db()
    try:
        conn.execute('BEGIN IMMEDIATE')
        old=conn.execute('SELECT id,user_id FROM orders WHERE request_key=?',(key,)).fetchone()
        if old:
            if old['user_id']!=uid: raise ValidationError('Pedido inválido.')
            conn.rollback(); return old['id']
        rows=basket(cart)
        for p in rows:
            if p['quantity']>p['stock']:raise ValidationError(f'Estoque insuficiente para {p["name"]}. Ajuste o carrinho.')
        oid=conn.execute('''INSERT INTO orders(user_id,request_key,recipient,street,number,complement,district,city,state,postal_code,delivery_cents)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)''',(uid,key,address['recipient'],address['street'],address['number'],address['complement'],address['district'],address['city'],address['state'],address['postal_code'],800)).lastrowid
        for p in rows:
            conn.execute('INSERT INTO order_items VALUES(?,?,?,?,?)',(oid,p['id'],p['name'],p['quantity'],p['price_cents']))
            conn.execute('UPDATE products SET stock=stock-? WHERE id=?',(p['quantity'],p['id']))
        conn.execute('INSERT INTO order_events(order_id,status) VALUES(?,?)',(oid,'aguardando pagamento'))
        conn.commit();return oid
    except Exception:
        conn.rollback();raise

def order(oid,uid=None):
    sql='SELECT * FROM orders WHERE id=?';args=[oid]
    if uid is not None: sql+=' AND user_id=?';args.append(uid)
    row=db().execute(sql,args).fetchone()
    if not row:return None
    out=dict(row)
    out['items']=db().execute('SELECT * FROM order_items WHERE order_id=?',(oid,)).fetchall()
    out['total']=sum(i['quantity']*i['unit_cents'] for i in out['items'])+out['delivery_cents']
    out['events']=db().execute('SELECT * FROM order_events WHERE order_id=? ORDER BY id',(oid,)).fetchall()
    out['payments']=db().execute('SELECT * FROM payments WHERE order_id=? ORDER BY id',(oid,)).fetchall()
    return out

def pay(oid,uid,method,result):
    if method not in ('pix','cartao') or result not in ('aprovado','recusado'):raise ValidationError('Selecione uma opção de pagamento válida.')
    conn=db()
    try:
        conn.execute('BEGIN IMMEDIATE');o=order(oid,uid)
        if not o or o['status']!='aguardando pagamento':raise ValidationError('Este pedido não está aguardando pagamento.')
        conn.execute('INSERT INTO payments(order_id,method,result,amount_cents) VALUES(?,?,?,?)',(oid,method,result,o['total']))
        if result=='aprovado':
            conn.execute("UPDATE orders SET status='confirmado' WHERE id=?",(oid,))
            conn.execute("INSERT INTO order_events(order_id,status) VALUES(?,'confirmado')",(oid,))
        conn.commit()
    except Exception:conn.rollback();raise

def cancel(oid,uid):
    conn=db()
    try:
        conn.execute('BEGIN IMMEDIATE');o=order(oid,uid)
        if not o or o['status']!='aguardando pagamento':raise ValidationError('Só é possível cancelar antes da aprovação do pagamento.')
        for i in o['items']:conn.execute('UPDATE products SET stock=stock+? WHERE id=?',(i['quantity'],i['product_id']))
        conn.execute("UPDATE orders SET status='cancelado' WHERE id=?",(oid,))
        conn.execute("INSERT INTO order_events(order_id,status) VALUES(?,'cancelado')",(oid,));conn.commit()
    except Exception:conn.rollback();raise

NEXT={'confirmado':'em preparo','em preparo':'saiu para entrega','saiu para entrega':'entregue'}
def advance(oid,expected):
    if expected not in NEXT: raise ValidationError('Transição inválida.')
    with db():
        c=db().execute('UPDATE orders SET status=? WHERE id=? AND status=?',(NEXT[expected],oid,expected))
        if c.rowcount!=1:raise ValidationError('O pedido mudou. Atualize a página.')
        db().execute('INSERT INTO order_events(order_id,status) VALUES(?,?)',(oid,NEXT[expected]))

def save_product(data,pid=None):
    fields=(text(data.get('name'),'Nome',100,2),text(data.get('description'),'Descrição',500),text(data.get('flavor'),'Sabor',50),text(data.get('allergens'),'Alergênicos',250),integer(data.get('price_cents'),'Preço em centavos',1,100000),integer(data.get('stock'),'Estoque',0,9999),1 if data.get('active')=='1' else 0)
    try:
        with db():
            db().execute("BEGIN IMMEDIATE")
            if pid:
                if not product(pid):raise ValidationError('Produto não encontrado.')
                reserved=db().execute("SELECT COALESCE(SUM(i.quantity),0) FROM order_items i JOIN orders o ON o.id=i.order_id WHERE i.product_id=? AND o.status='aguardando pagamento'",(pid,)).fetchone()[0]
                if fields[5]+reserved>9999:raise ValidationError(f'Estoque livre mais reservas pendentes não pode ultrapassar 9999. Há {reserved} unidades reservadas.')
                db().execute('UPDATE products SET name=?,description=?,flavor=?,allergens=?,price_cents=?,stock=?,active=? WHERE id=?',(*fields,pid))
            else:db().execute('INSERT INTO products(name,description,flavor,allergens,price_cents,stock,active) VALUES(?,?,?,?,?,?,?)',fields)
    except sqlite3.IntegrityError:raise ValidationError('Já existe um produto com este nome.')
