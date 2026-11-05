"""Ampliação explícita do cardápio; nunca executada ao abrir o site.

Uso: python deploy/expand_catalog.py /caminho/cupcakes.sqlite
O banco deve existir. Faz backup consistente antes de inserir os novos produtos.
"""
import sqlite3
from contextlib import closing
import sys
from datetime import datetime, timezone
from pathlib import Path

PRODUCTS = [
    ('Limão suave', 'Massa de limão com cobertura cítrica cremosa.', 'Limão',
     'Contém leite, ovos e trigo (glúten).', 1290, 30),
    ('Coco cremoso', 'Massa de coco com cobertura cremosa e coco ralado.', 'Coco',
     'Contém leite, ovos e trigo (glúten).', 1390, 30),
    ('Doce de leite especial', 'Massa de baunilha com cobertura de doce de leite.', 'Doce de leite',
     'Contém leite, ovos e trigo (glúten).', 1490, 30),
]

def expand_catalog(database):
    path = Path(database).resolve(strict=True)
    backup = path.with_name(path.name + '.before-feedback-' +
                            datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.bak')
    with closing(sqlite3.connect(str(path))) as conn:
        # Valida o banco antes de qualquer gravação.
        conn.execute('SELECT id, name, stock FROM products LIMIT 0')
        with closing(sqlite3.connect(str(backup))) as target:
            conn.backup(target)
        backup.chmod(0o600)
        conn.execute('BEGIN IMMEDIATE')
        inserted = 0
        for product in PRODUCTS:
            if not conn.execute('SELECT 1 FROM products WHERE name=?', (product[0],)).fetchone():
                conn.execute('INSERT INTO products(name,description,flavor,allergens,price_cents,stock) VALUES(?,?,?,?,?,?)', product)
                inserted += 1
        conn.commit()
    return inserted, backup

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Uso: python deploy/expand_catalog.py BANCO_EXISTENTE.sqlite')
    inserted, backup = expand_catalog(sys.argv[1])
    print(f'Produtos adicionados: {inserted}. Backup privado: {backup}')
