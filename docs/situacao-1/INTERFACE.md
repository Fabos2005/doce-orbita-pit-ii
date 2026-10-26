# Interface e arquitetura de informação

## Continuidade do protótipo entregue

Preservados: título Doce Órbita, busca, listagem vertical de produtos e ação Comprar. Acrescentados: descrição, sabor, alergênicos, preço, estoque, navegação, carrinho, entrega, pagamento, histórico e gestão. A paleta rosa/creme e a ilustração SVG são decisões desta revisão; o PIT I tinha um wireframe sem paleta. Não se afirma fidelidade a telas inexistentes no documento original.

## Mapa conceitual

Loja oferece Produtos; Cliente seleciona Produtos em Carrinho; Carrinho confirmado origina Pedido; Pedido reúne Itens e Endereço; Pagamento simulado confirma Pedido; Gestão altera Estado da entrega; Eventos tornam o andamento consultável. Estoque diminui na confirmação do pedido e retorna no cancelamento pendente. A rejeição do pagamento mantém a reserva até nova tentativa ou cancelamento.

## Mapa navegacional

Catálogo → Detalhe → Carrinho → Login/Cadastro (se necessário) → Carrinho → Entrega/Resumo → Pedido/Pagamento → Meus pedidos → Detalhe/Histórico. Catálogo e carrinho são acessíveis pela navegação global. Gestão → Login gestor → Pedidos recebidos → Detalhe/Avançar. Gestão → Produtos → Novo/Editar. Logout volta ao catálogo.

## Telas e especificações

|ID|Tela / arquivo|Campos, ações e estados|
|---|---|---|
|T01|Catálogo / catalog.html|Busca q até 100; lista de ativos; Comprar soma 1; esgotado desabilitado; nenhum resultado permite limpar|
|T02|Detalhe / product.html|Nome, descrição, sabor, alergênicos, preço, estoque; quantidade 1–99; adicionar;404 para inativo|
|T03|Cadastro / auth.html|Nome 2–80, e-mail 5–160, senha 10–128, confirmação; obrigatório; nome/e-mail preservados após erro|
|T04|Login / auth.html|E-mail e senha; erro genérico; link cadastrar; senha não reapresentada|
|T05|Carrinho / cart.html|Itens, quantidades 0–99, subtotais, frete, total; atualizar e remover por zero; vazio; estoque revalidado na compra|
|T06|Entrega / checkout.html|Destinatário, CEP, rua, número, complemento, bairro, cidade, UF; resumo lado a lado no desktop; campos mantidos após erro|
|T07|Pedido e pagamento / order.html|Identificador, status, itens, destino, total, eventos; método Pix/cartão; aprovação/recusa; confirmação de cancelamento com Manter pedido/Escape|
|T08|Meus pedidos / orders.html|Lista do proprietário; detalhe; estado vazio|
|T09|Login gestão / auth.html|Senha exclusiva; erro de senha; nenhuma senha no código|
|T10|Pedidos gestão / orders.html|Todos pedidos; detalhe; avanço sequencial do estado|
|T11|Produtos gestão / admin_products.html|Listagem ativos/inativos; novo e editar|
|T12|Edição produto / edit_product.html|Nome, descrição, sabor, alergênicos, preço em centavos, estoque, visibilidade; mensagens de validação e campos preservados|
|T13|Erros / error.html|400/403/404/413/500; explicação sem stacktrace e link cardápio|

## Wireframes e mockups

`prototipo.html` reúne esquemas de todas as telas e seus estados principais. Os templates executáveis e style.css são os mockups funcionais desta revisão, sujeitos à inspeção visual em navegador. Não há evidência visual de homologação ainda. O PDF Wireframes-Cupcake-App.pdf reúne os esquemas. Antes do aceite, exportar as telas definitivas para PDF ou apresentação conforme orientação do PIT I e incorporar às evidências.

## Critérios de usabilidade

Layout responsivo em 650px, fluxo em coluna no celular, rótulos associados, títulos hierárquicos, pular para conteúdo, foco visível, botões≥46px, mensagens role=alert, estado expresso em texto, sem animação essencial. Ilustração decorativa tem alt vazio na lista e descrição no detalhe. Cancelamento possui confirmação dentro da página. HTTPS e sessão segura são exigências da hospedagem. Testar teclado,390px, zoom 200%, contraste e leitor de tela antes de declarar acessibilidade. Não há certificação WCAG.
