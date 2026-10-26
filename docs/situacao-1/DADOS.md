# Projeto de dados

## Modelo conceitual

Um Cliente realiza zero ou muitos Pedidos; cada Pedido pertence a exatamente um Cliente. Cada Pedido possui um ou mais Itens; cada Item referencia exatamente um Produto. Um Produto pode aparecer em muitos Itens. Um Pedido possui zero ou muitas tentativas de Pagamento e um ou muitos Eventos de andamento. Um pagamento aprovado por pedido é o máximo permitido. O endereço informado é o destino histórico daquele pedido, não um cadastro de endereços reutilizável.

## Modelo lógico e normalização

users(id PK, name, email UNIQUE, password_hash, created_at). products(id PK, name UNIQUE, description, flavor, allergens, price_cents, stock, active). orders(id PK, user_id FK, request_key UNIQUE, status, recipient, street, number, complement, district, city, state, postal_code, delivery_cents, created_at). order_items(order_id PK/FK, product_id PK/FK, product_name, quantity, unit_cents). payments(id PK, order_id FK, method, result, amount_cents, simulation, created_at). order_events(id PK, order_id FK, status, created_at).

Primeira forma normal: campos escalares; itens e tentativas são linhas próprias, sem lista de produtos dentro do pedido. Segunda forma normal: na chave composta dos itens, quantidade e valor da compra dependem do par pedido/produto. Terceira forma normal: dados de conta e catálogo ficam em suas entidades; pedido referencia cliente; não replica e-mail ou hash. Nome e preço nos itens representam a condição histórica da compra, que pode diferir do catálogo atual; são snapshots intencionais. O endereço é um fato do pedido. Total não é gravado no cabeçalho: é calculado pelos itens e frete. Valor do pagamento é o valor registrado na tentativa e deve coincidir com o total no momento da operação.

## Projeto físico

SQLite, uma instância WSGI com arquivo persistente. DDL executável: app/schema.sql. Conexões habilitam foreign_keys. Chaves estrangeiras não possuem cascata destrutiva; produtos são desativados, não apagados. Índices: orders_customer, orders_status, one_approved_payment (único parcial). Pedido, reserva, cancelamento e pagamento utilizam transação BEGIN IMMEDIATE para evitar concorrência inconsistente. As alterações são confirmadas em conjunto ou revertidas.

## Dicionário de dados

Todos os campos são NOT NULL, exceto as chaves primárias INTEGER cujo valor é gerado pelo SQLite. Complemento aceita string vazia. Datas created_at são TEXT ISO UTC geradas por CURRENT_TIMESTAMP.

|Tabela|Campo|Tipo|Domínio e integridade|
|---|---|---|---|
|users|id|INTEGER|PK gerada|
|users|name|TEXT|2–80 caracteres|
|users|email|TEXT|5–160; sintaxe validada; único, sem diferença de caixa|
|users|password_hash|TEXT|Hash Werkzeug; senha de entrada 10–128 nunca persistida em claro|
|users|created_at|TEXT|Instante UTC de cadastro|
|products|id|INTEGER|PK gerada|
|products|name|TEXT|2–100, UNIQUE|
|products|description|TEXT|Obrigatória na aplicação, máximo 500|
|products|flavor|TEXT|Obrigatório na aplicação, máximo 50|
|products|allergens|TEXT|Obrigatório; máximo 250 na aplicação|
|products|price_cents|INTEGER|1–100000; centavos|
|products|stock|INTEGER|0–9999; unidades livres|
|products|active|INTEGER|0 inativo,1 ativo|
|orders|id|INTEGER|PK gerada|
|orders|user_id|INTEGER|FK users.id|
|orders|request_key|TEXT|UNIQUE; idempotência gerada pelo servidor|
|orders|status|TEXT|aguardando pagamento, confirmado, em preparo, saiu para entrega, entregue, cancelado|
|orders|recipient|TEXT|1–80; destinatário|
|orders|street|TEXT|1–120; rua|
|orders|number|TEXT|1–12; aceita S/N|
|orders|complement|TEXT|0–100, padrão vazio|
|orders|district|TEXT|1–80|
|orders|city|TEXT|1–80|
|orders|state|TEXT|Sigla de uma das 27 UFs; validada no modelo|
|orders|postal_code|TEXT|8 dígitos normalizados; não consulta serviço externo|
|orders|delivery_cents|INTEGER|Não negativo; regra desta versão 800|
|orders|created_at|TEXT|Instante UTC do pedido|
|order_items|order_id|INTEGER|PK composta e FK orders.id|
|order_items|product_id|INTEGER|PK composta e FK products.id|
|order_items|product_name|TEXT|Snapshot do nome na compra|
|order_items|quantity|INTEGER|1–99|
|order_items|unit_cents|INTEGER|Positivo; snapshot do preço|
|payments|id|INTEGER|PK gerada|
|payments|order_id|INTEGER|FK orders.id|
|payments|method|TEXT|pix ou cartao|
|payments|result|TEXT|aprovado ou recusado; aprovado único por pedido|
|payments|amount_cents|INTEGER|Positivo; total do pedido calculado no servidor|
|payments|simulation|INTEGER|Sempre 1; nenhuma transação real|
|payments|created_at|TEXT|Instante UTC da tentativa|
|order_events|id|INTEGER|PK gerada|
|order_events|order_id|INTEGER|FK orders.id|
|order_events|status|TEXT|Estado resultante da operação validada pelo modelo|
|order_events|created_at|TEXT|Instante UTC do evento|

Limites de formulários e validações no modelo complementam CHECK, NOT NULL, UNIQUE e FK do banco; não se afirma que toda regra semântica está em SQL. A cardinalidade mínima de um item/evento por pedido é assegurada pelo serviço transacional. As transições de estado são regras do modelo.
