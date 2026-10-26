# PIT I Atualizado

## Planejamento de requisitos

A continuidade do projeto Doce Órbita parte do PIT I entregue. São incorporados pagamento demonstrativo, entrega, gestão, dados e testes. As estimativas abaixo representam esforço previsto por tarefa, não tempo realizado.

## Mapa de afinidade

- **Conta e acesso:** HU01, HU02, HU03.
- **Catálogo:** HU04, HU05, HU06.
- **Compra:** HU07, HU08, HU09, HU10, HU12.
- **Pagamento:** HU11.
- **Entrega:** HU13, HU15.
- **Gestão:** HU14.
- **Qualidade:** HU16.

## Backlog priorizado

|Ordem|ID|História|Prioridade|Pontos|
|---|---|---|---|---|
|1|HU01|Criar conta|A|3|
|2|HU02|Entrar|A|2|
|3|HU03|Sair|A|1|
|4|HU04|Consultar vitrine|A|3|
|5|HU05|Buscar cupcake|A|2|
|6|HU07|Adicionar ao carrinho|A|3|
|7|HU08|Revisar carrinho|A|2|
|8|HU09|Informar entrega|A|3|
|9|HU10|Confirmar pedido|A|5|
|10|HU11|Pagar em demonstração|A|3|
|11|HU13|Acompanhar meus pedidos|A|3|
|12|HU15|Atualizar entrega|A|3|
|13|HU06|Ver detalhes|B|2|
|14|HU12|Cancelar pedido pendente|B|3|
|15|HU14|Gerenciar catálogo|B|5|
|16|HU16|Receber retorno claro|B|3|

Prioridades: A essencial, B importante; C desejável, D baixa e E futura não utilizadas nesta versão. Pontos são relativos, não horas. Iterações propostas: acesso/catálogo; compra/dados; pagamento/entrega; revisão/testes/avaliação.

## HU01 Criar conta

**ID:** HU01. **Título:** Criar conta. **Requerente:** visitante.

**Ação:** Como visitante, quero criar minha conta para comprar e consultar meus pedidos.

**Comentários:** Grupo Conta e acesso; implementação rastreada em `register`.

**CA01:** Dado um e-mail novo, quando confirmar os dados válidos, então criar uma conta e autenticar; e-mail repetido ou senha inválida mostra erro.

**RN01:** Nome de 2–80, e-mail válido único sem diferença de caixa; senha 10–128, confirmação igual.

**RNF01:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 3.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_registration_duplicate_case`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU02 Entrar

**ID:** HU02. **Título:** Entrar. **Requerente:** cliente.

**Ação:** Como cliente, quero entrar com e-mail e senha para acessar minhas compras.

**Comentários:** Grupo Conta e acesso; implementação rastreada em `login`.

**CA02:** Dado cadastro existente, quando informar senha correta, então abrir sessão; senha incorreta não autentica.

**RN02:** Validar hash; mensagem genérica para credencial incorreta.

**RNF02:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 2.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_login_invalid`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU03 Sair

**ID:** HU03. **Título:** Sair. **Requerente:** cliente.

**Ação:** Como cliente, quero encerrar a sessão para evitar acesso à minha conta.

**Comentários:** Grupo Conta e acesso; implementação rastreada em `logout`.

**CA03:** Dada sessão ativa, quando sair, então pedidos exigem novo login.

**RN03:** POST com CSRF; limpar autenticação e carrinho da sessão.

**RNF03:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 1.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_http_logout`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU04 Consultar vitrine

**ID:** HU04. **Título:** Consultar vitrine. **Requerente:** visitante.

**Ação:** Como visitante, quero ver cupcakes, preços e sabores para escolher uma opção.

**Comentários:** Grupo Catálogo; implementação rastreada em `home`.

**CA04:** Dado produto ativo, quando abrir cardápio, então mostrar descrição e preço; inativo não aparece.

**RN04:** Apenas produtos ativos; preço em reais; informar alergênicos e estoque.

**RNF04:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 3.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_catalog_search`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU05 Buscar cupcake

**ID:** HU05. **Título:** Buscar cupcake. **Requerente:** visitante.

**Ação:** Como visitante, quero buscar por nome ou sabor para encontrar o produto desejado.

**Comentários:** Grupo Catálogo; implementação rastreada em `home`.

**CA05:** Dado sabor chocolate, quando buscar Chocolate, então listar correspondências; texto inexistente mostra estado vazio.

**RN05:** Busca parcial por nome/sabor, até 100 caracteres; estado vazio e limpar busca.

**RNF05:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 2.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_catalog_search`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU06 Ver detalhes

**ID:** HU06. **Título:** Ver detalhes. **Requerente:** visitante.

**Ação:** Como visitante, quero ver descrição e alergênicos para avaliar o cupcake antes da compra.

**Comentários:** Grupo Catálogo; implementação rastreada em `detail`.

**CA06:** Dado produto disponível, quando abrir detalhes, então mostrar descrição, preço, estoque e alergênicos; id inexistente retorna 404.

**RN06:** Produto ativo; quantidade 1–99 e disponibilidade visível.

**RNF06:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** B. **Pontos:** 2.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_http_pages`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU07 Adicionar ao carrinho

**ID:** HU07. **Título:** Adicionar ao carrinho. **Requerente:** visitante.

**Ação:** Como visitante, quero adicionar quantidades de cupcakes para montar minha compra.

**Comentários:** Grupo Compra; implementação rastreada em `cart_change`.

**CA07:** Dado estoque disponível, quando adicionar 2 unidades, então atualizar subtotal; quantidade maior que estoque é recusada.

**RN07:** Somar até 99 por produto e até estoque atual; máximo 30 produtos distintos.

**RNF07:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 3.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_http_cart`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU08 Revisar carrinho

**ID:** HU08. **Título:** Revisar carrinho. **Requerente:** cliente.

**Ação:** Como cliente, quero alterar ou remover itens para corrigir minha seleção.

**Comentários:** Grupo Compra; implementação rastreada em `cart_change`.

**CA08:** Dado item no carrinho, quando alterar quantidade para 0, então removê-lo e atualizar o total.

**RN08:** Quantidade 0 remove; recalcular subtotais e informar frete 8 reais.

**RNF08:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 2.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_http_cart`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU09 Informar entrega

**ID:** HU09. **Título:** Informar entrega. **Requerente:** cliente.

**Ação:** Como cliente, quero preencher endereço para definir o destino do pedido.

**Comentários:** Grupo Compra; implementação rastreada em `checkout`.

**CA09:** Dado carrinho, quando informar CEP inválido, então mostrar erro e conservar campos; endereço válido permite confirmar.

**RN09:** Destinatário, rua, número, bairro, cidade, UF e CEP obrigatórios; complemento opcional; UF válida e CEP 8 dígitos.

**RNF09:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 3.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_address_invalid`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU10 Confirmar pedido

**ID:** HU10. **Título:** Confirmar pedido. **Requerente:** cliente.

**Ação:** Como cliente, quero confirmar o resumo da compra para registrar meu pedido sem duplicação.

**Comentários:** Grupo Compra; implementação rastreada em `checkout`.

**CA10:** Dado último exemplar, quando dois pedidos concorrem, então apenas um reserva; repetir a mesma chave retorna o mesmo pedido.

**RN10:** Autenticação; totais no servidor; reserva transacional de estoque e chave idempotente.

**RNF10:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 5.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_concurrent_last_unit`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU11 Pagar em demonstração

**ID:** HU11. **Título:** Pagar em demonstração. **Requerente:** cliente.

**Ação:** Como cliente, quero simular Pix ou cartão para testar aprovação e recusa sem cobrança.

**Comentários:** Grupo Pagamento; implementação rastreada em `pay`.

**CA11:** Dado pedido pendente, quando simular recusa, então manter pendente; quando aprovar, então confirmar; segunda aprovação é recusada.

**RN11:** Somente proprietário e pedido aguardando pagamento; recusa permite tentar; uma aprovação por pedido.

**RNF11:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 3.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_payment_declined_retry`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU12 Cancelar pedido pendente

**ID:** HU12. **Título:** Cancelar pedido pendente. **Requerente:** cliente.

**Ação:** Como cliente, quero cancelar antes da aprovação para desfazer a compra.

**Comentários:** Grupo Compra; implementação rastreada em `cancel`.

**CA12:** Dado pedido pendente, quando confirmar cancelamento, então devolver estoque; repetir não devolve novamente.

**RN12:** Confirmação reversível no navegador; servidor aceita só pendente e devolve estoque uma vez.

**RNF12:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** B. **Pontos:** 3.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_cancel_restore_once`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU13 Acompanhar meus pedidos

**ID:** HU13. **Título:** Acompanhar meus pedidos. **Requerente:** cliente.

**Ação:** Como cliente, quero consultar situação e histórico para saber o andamento da entrega.

**Comentários:** Grupo Entrega; implementação rastreada em `orders/order`.

**CA13:** Dado pedido de outro cliente, quando consultar seu id, então retornar 404; pedido próprio mostra histórico.

**RN13:** Acesso restrito ao proprietário; exibir itens, endereço, eventos e pagamentos.

**RNF13:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 3.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_http_order_isolation`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU14 Gerenciar catálogo

**ID:** HU14. **Título:** Gerenciar catálogo. **Requerente:** gestor.

**Ação:** Como gestor, quero cadastrar, editar e desativar cupcakes para manter a vitrine atualizada.

**Comentários:** Grupo Gestão; implementação rastreada em `edit_product`.

**CA14:** Dado cadastro válido, quando salvar, então atualizar catálogo; preço negativo é recusado; alteração não muda preço de pedido anterior.

**RN14:** Senha exclusiva; preço positivo em centavos, estoque inteiro não negativo; desativar preserva histórico.

**RNF14:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** B. **Pontos:** 5.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_product_price_history`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU15 Atualizar entrega

**ID:** HU15. **Título:** Atualizar entrega. **Requerente:** gestor.

**Ação:** Como gestor, quero avançar a situação dos pedidos pagos para informar preparo e entrega.

**Comentários:** Grupo Entrega; implementação rastreada em `admin_order`.

**CA15:** Dado confirmado, quando avançar três vezes, então terminar entregue; pedido pendente não pode avançar para preparo.

**RN15:** Confirmado→em preparo→saiu para entrega→entregue; não pular estados; guardar evento.

**RNF15:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** A. **Pontos:** 3.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_delivery_flow`; quando houver critério visual, completar inspeção em navegador e avaliação externa.

## HU16 Receber retorno claro

**ID:** HU16. **Título:** Receber retorno claro. **Requerente:** usuário.

**Ação:** Como usuário, quero entender os erros e usar em tela pequena para concluir tarefas com segurança.

**Comentários:** Grupo Qualidade; implementação rastreada em `templates/static`.

**CA16:** Dado erro de entrada, quando enviar formulário, então apresentar mensagem; teclado e 390px precisam de inspeção humana em navegador.

**RN16:** Rótulos associados, foco visível, alertas textuais, campos preservados no checkout, layout responsivo; não declarar conformidade sem avaliação.

**RNF16:** Validação no servidor, mensagem em português, escape de saída e operação de alteração protegida por CSRF quando aplicável. Os controles devem funcionar em telas estreitas e por teclado.

**Prioridade:** B. **Pontos:** 3.

**Tarefas previstas:** especificar campos e fluxos (2 h); implementar modelo/controlador/tela (4 h); verificar cenários e atualizar documentação (2 h). Decompor caso ultrapasse 12 h.

**Evidência de verificação:** `test_http_headers`; quando houver critério visual, completar inspeção em navegador e avaliação externa.
