# Melhorias após as avaliações — 05/11/2026

## Origem e decisão

Consultei as cinco respostas reais do formulário Avaliação da Doce Órbita — PIT II. Registrei abaixo as três sugestões concretas da pergunta 9. Uso apenas os IDs das respostas neste repositório público; os nomes e as avaliações completas ficam no material de entrega acadêmica. Não criei avaliações artificiais.

|Resposta|Sugestão recebida|Mudança que implementei|
|---|---|---|
|1|Melhorar o design do layout com mais cores|Acrescentei fundos suaves rosa, creme, verde, lilás e caramelo. Mantive a navegação e os nomes dos sabores visíveis, sem depender apenas das cores.|
|2|Oferecer mais produtos no cardápio|Preparei Limão suave (R$ 12,90), Coco cremoso (R$ 13,90) e Doce de leite especial (R$ 14,90), com 30 unidades demonstrativas iniciais cada. Preservei chocolate, baunilha e morango.|
|3|Mostrar a quantidade disponível também no carrinho|Passei a exibir o saldo livre atual por item e um aviso quando a quantidade selecionada supera o estoque. Mantive o cálculo de subtotal e a reserva apenas na confirmação do pedido.|

A resposta 4 informou “Sem sugestões”; a resposta 5 escreveu “isso”, sem uma proposta concreta. Na pergunta sobre falhas, quatro participantes informaram não encontrar falhas e o quinto escreveu “isso”. Não interpretei essa resposta ambígua como validação do sistema.

Revisei o PIT I entregue e o enunciado do PIT II: não identifiquei limite obrigatório de três sabores nem paleta imposta. Classifiquei as mudanças como melhorias de usabilidade e variedade, não como correções de defeitos relatados pelos participantes.

## Continuidade e proteção dos dados

Recuperei a implementação anterior e comparei os hashes Git de modelos, controladores, inicialização, CSS, catálogo, detalhe, manual e laudo com o GitHub: os arquivos conferiram. Executei a suíte anterior: 42 testes aprovados antes das alterações.

Mantive a estrutura SQLite, as rotas, a autenticação, o pagamento simulado, as reservas e o cancelamento. A ampliação do cardápio é explícita, pelo script `deploy/expand_catalog.py`: ele exige um banco existente, cria backup consistente privado e insere somente os nomes que ainda não existem, em transação. Reexecutá-lo não duplica produtos, não repõe estoque vendido e não reativa produtos desativados. Não publiquei banco, senhas ou dados dos clientes.

## Verificação executada

Executei `python -m unittest discover -s tests -v`: **47 testes aprovados**. A saída completa está em [test-results-feedback.txt](test-results-feedback.txt). Os cinco novos testes cobrem:

- preservação de produto, estoque, pedido e possibilidade de cancelamento após a ampliação; backup e reexecução sem reposição ou reativação;
- busca, detalhe, ilustrações, compra e pagamento simulado dos três novos sabores;
- saldo atualizado no carrinho e aviso após redução concorrente do estoque;
- saldo zero e remoção de produto indisponível;
- recusa de um caminho de banco inexistente, sem criar banco vazio.

Os testes usam bancos temporários. Não equivalem a retestes dos participantes nem a verificação no servidor público.

## Publicação e pendências

**Alterações preparadas e testadas localmente; publicação no PythonAnywhere pendente de login.** Não declarei a versão pública atualizada. Ainda preciso comparar os arquivos e os dados atuais do servidor, fazer backup, aplicar a versão, executar a suíte no servidor, reiniciar e conferir catálogo/carrinho em desktop e celular.

Preservei os PDFs de wireframes/mockups anteriores como evidência do planejamento. O detalhamento atualizado da interface está em `docs/situacao-1/INTERFACE.md`; os PDFs ainda não representam esta revisão de cores/cardápio. O Word final, PDF com as cinco opiniões e segundo vídeo continuam pendentes. O primeiro vídeo foi informado pelo aluno como gravado, com 9min35s; não o analisei. Não enviei nada à faculdade.

## Roteiro de publicação e reversão

1. Comparo a versão do servidor com a base recuperada; interrompo se houver alterações posteriores não incorporadas.
2. Faço cópia privada dos arquivos substituídos. O script de ampliação faz backup do SQLite antes de inserir os três produtos.
3. Publico apenas os arquivos desta revisão; não substituo a configuração privada nem o banco.
4. Executo os 47 testes com banco temporário no servidor e aplico `python deploy/expand_catalog.py /home/fabrifeliciano/.local/share/cupcakes/cupcakes.sqlite` usando o ambiente virtual já existente.
5. Reinicio a aplicação e verifico as três melhorias, fluxo de compra, desktop e celular. Só então registro a publicação como concluída.
6. Se necessário, restauro os arquivos anteriores. Não restauro um backup antigo de banco sobre pedidos posteriores: desativo os novos produtos pela gestão e preservo o histórico. A restauração do banco exige verificar que não houve novas gravações.
