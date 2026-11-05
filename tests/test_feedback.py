"""Regressões das sugestões reais; todos os dados são temporários."""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from app import create_app, models as m
from deploy.expand_catalog import expand_catalog

class FeedbackTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'shop.sqlite'
        self.app = create_app(dict(TESTING=True, SECRET_KEY='x'*40,
                                  ADMIN_PASSWORD='test-password-123', DATABASE=str(self.path)))
        self.ctx = self.app.app_context(); self.ctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.ctx.pop(); self.tmp.cleanup()

    def test_expansion_preserves_history_and_stock_on_rerun(self):
        uid = m.register('Teste', 'feedback@example.com', 'test-password')
        from test_shop import ADDRESS
        oid = m.checkout(uid, {'1': 2}, ADDRESS, 'before-feedback')
        before = dict(m.product(1)); order_before = m.order(oid)
        inserted, backup = expand_catalog(self.path)
        self.assertEqual(inserted, 3)
        self.assertEqual(dict(m.product(1)), before)
        self.assertEqual(m.order(oid)['total'], order_before['total'])
        with sqlite3.connect(backup) as conn:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM products').fetchone()[0], 3)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0], 1)
        m.db().execute('UPDATE products SET stock=7, active=0 WHERE name=?', ('Limão suave',)); m.db().commit()
        self.assertEqual(expand_catalog(self.path)[0], 0)
        lemon = m.db().execute('SELECT stock,active FROM products WHERE name=?', ('Limão suave',)).fetchone()
        self.assertEqual(tuple(lemon), (7, 0))
        m.cancel(oid, uid)
        self.assertEqual(m.product(1)['stock'], 30)

    def test_new_products_search_detail_and_checkout(self):
        expand_catalog(self.path)
        self.assertEqual(len(m.catalog()), 6)
        uid = m.register('Teste', 'buy@example.com', 'test-password')
        from test_shop import ADDRESS
        for flavor, image in [('Limão', 'limao'), ('Coco', 'coco'), ('Doce de leite', 'doce-de-leite')]:
            p = m.catalog(flavor)[0]
            response = self.client.get(f'/produto/{p["id"]}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(f'cupcake-{image}.svg'.encode(), response.data)
            oid = m.checkout(uid, {str(p['id']): 1}, ADDRESS, flavor)
            m.pay(oid, uid, 'pix', 'aprovado')
            self.assertEqual(m.order(oid)['total'], p['price_cents'] + 800)
            self.assertEqual(m.product(p['id'])['stock'], 29)

    def test_cart_reads_current_stock_and_warns_when_changed(self):
        with self.client.session_transaction() as session:
            session['cart'] = {'1': 3}
        self.assertIn(b'30 unidades', self.client.get('/carrinho').data)
        m.db().execute('UPDATE products SET stock=2 WHERE id=1'); m.db().commit()
        response = self.client.get('/carrinho')
        self.assertIn(b'2 unidades', response.data)
        self.assertIn('O estoque mudou'.encode(), response.data)
        self.assertIn(b'R$ 38,70', response.data)
        self.assertEqual(m.product(1)['stock'], 2)

    def test_cart_out_of_stock_and_inactive_can_be_removed(self):
        with self.client.session_transaction() as session:
            session['cart'] = {'1': 1}
        m.db().execute('UPDATE products SET stock=0 WHERE id=1'); m.db().commit()
        self.assertIn(b'0 unidades', self.client.get('/carrinho').data)
        m.db().execute('UPDATE products SET active=0 WHERE id=1'); m.db().commit()
        self.assertIn('Remova-o'.encode(), self.client.get('/carrinho').data)
        with self.client.session_transaction() as session:
            csrf = session['csrf']
        result = self.client.post('/carrinho/1', data=dict(csrf=csrf, quantity=0), follow_redirects=True)
        self.assertIn('Seu carrinho está vazio'.encode(), result.data)

    def test_missing_database_does_not_create_file(self):
        missing = Path(self.tmp.name) / 'missing.sqlite'
        with self.assertRaises(FileNotFoundError):
            expand_catalog(missing)
        self.assertFalse(missing.exists())
