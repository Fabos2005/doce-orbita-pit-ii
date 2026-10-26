import unittest,tempfile,threading
from pathlib import Path
from app import create_app, models as m

ADDRESS=dict(recipient='Cliente teste',street='Rua de teste',number='10',complement='',district='Centro',city='São Paulo',state='SP',postal_code='01001000')
class ShopTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.app=create_app(dict(TESTING=True,SECRET_KEY='x'*40,ADMIN_PASSWORD='admin-test-1234',DATABASE=str(Path(self.tmp.name)/'db.sqlite')));self.ctx=self.app.app_context();self.ctx.push();self.client=self.app.test_client();self.uid=m.register('Pessoa teste','teste@example.com','password123')
 def tearDown(self):self.ctx.pop();self.tmp.cleanup()
 def post(self,path,data=None):
  self.client.get('/')
  with self.client.session_transaction() as s: token=s['csrf']
  return self.client.post(path,data=dict(csrf=token,**(data or {})),follow_redirects=True)
 def login(self):return self.post('/entrar',dict(email='teste@example.com',password='password123'))
 def buy(self,qty=1,key='key'):return m.checkout(self.uid,{'1':qty},ADDRESS,key)
 def test_catalog_search(self):self.assertEqual(len(m.catalog('Chocolate')),1);self.assertEqual(len(m.catalog('inexistente')),0)
 def test_registration_hash(self):self.assertNotEqual(m.db().execute('SELECT password_hash FROM users').fetchone()[0],'password123')
 def test_registration_duplicate_case(self):
  with self.assertRaises(m.ValidationError):m.register('Outra pessoa','TESTE@example.com','password123')
 def test_registration_invalid_email(self):
  with self.assertRaises(m.ValidationError):m.register('Pessoa','invalido','password123')
 def test_registration_short_password(self):
  with self.assertRaises(m.ValidationError):m.register('Pessoa','a@b.com','123')
 def test_login_invalid(self):self.assertIsNone(m.authenticate('teste@example.com','errada'))
 def test_login_success(self):self.assertEqual(m.authenticate('teste@example.com','password123')['id'],self.uid)
 def test_empty_cart(self):
  with self.assertRaises(m.ValidationError):m.checkout(self.uid,{},ADDRESS,'key')
 def test_quantity_invalid(self):
  for q in [-1,0,100,'1.5','nan']:
   with self.subTest(q=q),self.assertRaises(m.ValidationError):m.checkout(self.uid,{'1':q},ADDRESS,'key')
 def test_stock_atomic(self):
  with self.assertRaises(m.ValidationError):m.checkout(self.uid,{'1':1,'2':99},ADDRESS,'key')
  self.assertEqual(m.product(1)['stock'],30);self.assertEqual(m.db().execute('SELECT count(*) FROM orders').fetchone()[0],0)
 def test_checkout_total_and_reservation(self):
  oid=self.buy(2);self.assertEqual(m.order(oid)['total'],3380);self.assertEqual(m.product(1)['stock'],28)
 def test_checkout_idempotent(self):self.assertEqual(self.buy(),self.buy());self.assertEqual(m.product(1)['stock'],29)
 def test_address_invalid(self):
  for k,v in [('postal_code','123'),('state','XX'),('street','')]:
   with self.subTest(k=k),self.assertRaises(m.ValidationError):m.checkout(self.uid,{'1':1},dict(ADDRESS,**{k:v}),'key')
 def test_cancel_restore_once(self):
  oid=self.buy();m.cancel(oid,self.uid)
  with self.assertRaises(m.ValidationError):m.cancel(oid,self.uid)
  self.assertEqual(m.product(1)['stock'],30)
 def test_payment_declined_retry(self):
  oid=self.buy();m.pay(oid,self.uid,'pix','recusado');self.assertEqual(m.order(oid)['status'],'aguardando pagamento');m.pay(oid,self.uid,'cartao','aprovado');self.assertEqual(m.order(oid)['status'],'confirmado')
 def test_payment_duplicate_rejected(self):
  oid=self.buy();m.pay(oid,self.uid,'pix','aprovado')
  with self.assertRaises(m.ValidationError):m.pay(oid,self.uid,'pix','aprovado')
 def test_payment_invalid(self):
  oid=self.buy()
  with self.assertRaises(m.ValidationError):m.pay(oid,self.uid,'bitcoin','aprovado')
 def test_paid_cancel_rejected(self):
  oid=self.buy();m.pay(oid,self.uid,'pix','aprovado')
  with self.assertRaises(m.ValidationError):m.cancel(oid,self.uid)
 def test_delivery_flow(self):
  oid=self.buy();m.pay(oid,self.uid,'pix','aprovado')
  for st in m.NEXT:m.advance(oid,st)
  self.assertEqual(m.order(oid)['status'],'entregue');self.assertEqual(len(m.order(oid)['events']),5)
 def test_delivery_skip_rejected(self):
  oid=self.buy()
  with self.assertRaises(m.ValidationError):m.advance(oid,'em preparo')
 def test_other_customer_isolation(self):
  oid=self.buy();other=m.register('Outra pessoa','outro@example.com','password123');self.assertIsNone(m.order(oid,other))
  with self.assertRaises(m.ValidationError):m.pay(oid,other,'pix','aprovado')
 def test_product_price_history(self):
  oid=self.buy();m.db().execute('UPDATE products SET price_cents=5000 WHERE id=1');m.db().commit();self.assertEqual(m.order(oid)['total'],2090)
 def test_product_inactive(self):
  m.db().execute('UPDATE products SET active=0 WHERE id=1');m.db().commit()
  with self.assertRaises(m.ValidationError):self.buy()
 def test_product_validation(self):
  with self.assertRaises(m.ValidationError):m.save_product(dict(name='Novo',description='Teste',flavor='Doce',allergens='Leite',price_cents='-1',stock='1',active='1'))
 def test_foreign_key(self):
  import sqlite3
  with self.assertRaises(sqlite3.IntegrityError):m.db().execute('INSERT INTO order_items VALUES(999,1,?,1,100)',('Teste',))
  m.db().rollback()
 def test_sql_injection(self):self.assertEqual(len(m.catalog("' OR 1=1 --")),0)
 def test_http_pages(self):
  for path in ['/','/produto/1','/entrar','/cadastro','/carrinho','/gestao/entrar']:
   with self.subTest(path=path):self.assertEqual(self.client.get(path).status_code,200)
 def test_http_csrf(self):self.assertEqual(self.client.post('/carrinho/1',data={'quantity':1}).status_code,400)
 def test_http_admin_denied(self):self.assertEqual(self.client.get('/gestao').status_code,302)
 def test_http_customer_required(self):self.assertEqual(self.client.get('/pedidos').status_code,302)
 def test_http_register_mismatch(self):r=self.post('/cadastro',dict(name='Pessoa',email='nova@example.com',password='password123',confirmation='outro'));self.assertIn('As senhas não conferem'.encode(),r.data)
 def test_http_cart(self):self.post('/carrinho/1',dict(quantity=2,action='add'));r=self.client.get('/carrinho');self.assertIn(b'R$ 25,80',r.data);self.post('/carrinho/1',dict(quantity=0));self.assertIn('Seu carrinho está vazio'.encode(),self.client.get('/carrinho').data)
 def test_http_checkout_render(self):
  self.login();self.post('/carrinho/1',dict(quantity=1,action='add'));self.client.get('/finalizar')
  with self.client.session_transaction() as s:key=s['checkout_key']
  r=self.post('/finalizar',dict(ADDRESS,request_key=key));self.assertEqual(r.status_code,200);self.assertIn('Pagamento de demonstração'.encode(),r.data)
 def test_http_order_isolation(self):
  oid=self.buy();other=m.register('Outra','other@example.com','password123')
  with self.client.session_transaction() as s:s['uid']=other
  self.assertEqual(self.client.get(f'/pedido/{oid}').status_code,404)
 def test_http_xss(self):
  m.db().execute('UPDATE products SET description=? WHERE id=1',('<script>alert(1)</script>',));m.db().commit();r=self.client.get('/');self.assertNotIn(b'<script>alert',r.data);self.assertIn(b'&lt;script&gt;',r.data)
 def test_http_admin_delivery(self):
  oid=self.buy();m.pay(oid,self.uid,'pix','aprovado');self.post('/gestao/entrar',dict(password='admin-test-1234'));r=self.post(f'/gestao/pedido/{oid}',dict(expected='confirmado'));self.assertEqual(r.status_code,200);self.assertEqual(m.order(oid)['status'],'em preparo')
 def test_http_logout(self):self.login();self.post('/sair');self.assertEqual(self.client.get('/pedidos').status_code,302)
 def test_http_inactive_cart_recovery(self):
  self.login();self.post('/carrinho/1',dict(quantity=1,action='add'));m.db().execute('UPDATE products SET active=0 WHERE id=1');m.db().commit();r=self.client.get('/finalizar',follow_redirects=True);self.assertEqual(r.status_code,200);self.assertIn('Remova-o'.encode(),r.data);self.post('/carrinho/1',dict(quantity=0));self.assertIn('Seu carrinho está vazio'.encode(),self.client.get('/carrinho').data)
 def test_http_headers(self):r=self.client.get('/');self.assertEqual(r.headers['X-Frame-Options'],'DENY');self.assertIn("default-src 'self'",r.headers['Content-Security-Policy'])
 def test_persistence(self):oid=self.buy();m.close_db();self.assertEqual(m.order(oid)['user_id'],self.uid)
 def test_concurrent_last_unit(self):
  m.db().execute('UPDATE products SET stock=1 WHERE id=1');m.db().commit();out=[]
  def run(key):
   with self.app.app_context():
    try:m.checkout(self.uid,{'1':1},ADDRESS,key);out.append('ok')
    except m.ValidationError:out.append('sem estoque')
  a=threading.Thread(target=run,args=('a',));b=threading.Thread(target=run,args=('b',));a.start();b.start();a.join();b.join();self.assertCountEqual(out,['ok','sem estoque']);self.assertEqual(m.product(1)['stock'],0)

 def test_restock_preserves_cancellation_capacity(self):
  oid=self.buy(2)
  data=dict(name='Chocolate intenso',description='Descrição',flavor='Chocolate',allergens='Leite',price_cents='1290',stock='9999',active='1')
  with self.assertRaises(m.ValidationError):m.save_product(data,1)
  self.assertEqual(m.product(1)['stock'],28)
  data['stock']='9997';m.save_product(data,1);m.cancel(oid,self.uid)
  self.assertEqual(m.product(1)['stock'],9999)

if __name__=='__main__':unittest.main()
