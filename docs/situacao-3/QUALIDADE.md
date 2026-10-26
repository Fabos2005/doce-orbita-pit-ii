# Laudo preliminar de verificação

Objeto: Doce Órbita, versão reconstruída para a loja de cupcakes. Responsável: Fabricio Feliciano Cardoso. A verificação local não constitui validação pelos cinco participantes nem homologação da hospedagem.

## Método

Suíte Python unittest com bancos SQLite temporários, regras de negócio e cliente HTTP Flask. Comando: python -m unittest discover -s tests -v. Ambiente Python 3.12, Flask 3.1.3. A saída completa final está em test-results.txt:42 testes passaram. Não foi medida cobertura de linhas nem carga. O teste de concorrência faz duas conexões competirem pelo último exemplar; só uma compra é aceita.

## Defeito e correção observados

A execução inicial falhou no cenário test_http_admin_delivery: o template orders.html fechava um laço com endif em vez de endfor, impedindo a renderização da listagem. Evidência antes: test-results-before-fix.txt. Correção: fechamento Jinja apropriado. Reteste: a suíte completa passou, incluindo a navegação de gestão e avanço para preparo. Também foi tratado o caminho de checkout com produto inativo para retornar mensagem ao carrinho em vez de erro não tratado; esse caminho foi validado no teste test_http_inactive_cart_recovery, incluindo a remoção do item inativo.

## Resultados

Cadastro, hash, duplicidade, e-mail inválido, senha curta, login, catálogo/busca, quantidades, endereço, totais, reserva, concorrência, idempotência, cancelamento único, recusa/repetição de pagamento, aprovação única, propriedade do pedido, preços históricos, produto inativo, estado de entrega, chaves estrangeiras, injeção SQL, escape HTML, CSRF, autorização, logout, cabeçalhos e reabertura do banco foram exercitados pelos testes nomeados na saída.

## Pendências de validação

Publicação GitHub bloqueada por 403 da integração; controle de navegador indisponível para atualizar PythonAnywhere e Forms nesta sessão. Inspeção visual desktop/mobile, teclado, contraste e confirmação JavaScript não executada. Testar no servidor HTTPS, persistência após reinício e fluxo cliente/gestor antes de liberar para colegas. Pagamento e entrega são simulados e precisam ser apresentados assim ao tutor.

Depois: coletar cinco opiniões reais, PDF das avaliações, priorização de sugestões, correções, retestes, evidências antes/depois, vídeo inicial e atualizado, Word final. Sem esses itens não se declara atendimento integral do PIT II. Nenhuma entrega acadêmica realizada nesta etapa.

## Verificação da hospedagem e do navegador

Em 25/10/2026, foram verificados no Edge: cadastro, login, busca por Morango, inclusão no carrinho, endereço fictício, pagamento recusado e posteriormente aprovado, acompanhamento pela gestão nas etapas preparo/saída/entregue, persistência após reinício e logout. Um segundo pedido foi mantido na confirmação de cancelamento e depois cancelado com liberação do estoque. A página inicial foi inspecionada em desktop e viewport de 390 pixels. Esses testes técnicos não substituem as cinco avaliações externas.

Na revisão do estoque foi identificada a possibilidade de editar o saldo livre para 9999 enquanto existiam reservas, impedindo sua restituição no cancelamento. A atualização do produto passa a validar saldo livre mais reservas pendentes em transação. Um teste reproduz a condição, verifica a rejeição e confirma cancelamento no limite. A suíte atual passa em 42 testes.
