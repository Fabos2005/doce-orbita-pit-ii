# PIT I Atualizado

Planejamento atualizado do Doce Órbita, continuidade do PIT I de Fabricio Feliciano Cardoso. O projeto contempla cadastro, autenticação, catálogo com busca, carrinho, pedido, pagamento demonstrativo e acompanhamento de entrega.

## Documentos integrantes

1. [Conferência dos enunciados e decisões](situacao-1/CONFERENCIA.md).
2. [Histórias, mapa de afinidade, backlog, critérios e tarefas](situacao-1/REQUISITOS.md).
3. [Casos de uso expandidos, classes, sequências e atividades](situacao-1/MODELAGEM.md).
4. [Caso de uso geral em SVG](situacao-1/casos-de-uso.svg).
5. [Modelo conceitual, lógico normalizado e dicionário de dados](situacao-1/DADOS.md).
6. [Projeto físico executável](../app/schema.sql).
7. [Interface, mapas e especificação das telas](situacao-1/INTERFACE.md).
8. [Wireframes em PDF](situacao-1/Wireframes-Doce-Orbita.pdf) , [mockups coloridos](situacao-1/Mockups-Doce-Orbita.pdf) e [fonte HTML](situacao-1/prototipo.html).
9. [Manual de uso](situacao-2/MANUAL.md).
10. [Verificação técnica](situacao-3/QUALIDADE.md) e [resultados](situacao-3/test-results.txt).

## Revisão do planejamento original

O PIT I entregue utilizava o nome provisório **Cupcake App** e previa cadastro, login, consulta de produtos e pedidos. A identidade atual passa a ser **Doce Órbita**. Permanecem a busca, a lista vertical de produtos e a ação Comprar do wireframe original.

O escopo detalhado reúne as três situações-problema: especificação ágil com 16 histórias, modelagem UML e projeto de interface. Para o PIT II, acrescenta carrinho, endereço, reserva transacional de estoque, pagamento demonstrativo com aprovação/recusa, cancelamento e acompanhamento de entrega, além da gestão do catálogo. Os modelos conceitual, lógico e físico e o dicionário de dados documentam seis tabelas SQLite.

A implementação utiliza Python/Flask, HTML, CSS e JavaScript. A hospedagem gratuita utiliza banco persistente; nenhuma compra, cobrança ou entrega real ocorre. O pagamento é uma simulação didática local e não representa integração bancária. Essa delimitação deve ser validada com o tutor se for exigido um provedor externo.

A validação compreende testes automatizados e funcionais no navegador, seguida de cinco avaliações reais por colegas de curso ou profissionais. As sugestões pertinentes serão incorporadas, documentadas e retestadas. Os dois vídeos serão narrados pelo aluno e os links reunidos no template Word oficial. Avaliações e resultados futuros não são antecipados como realizados.

## Acessos

- Aplicação: https://fabrifeliciano.pythonanywhere.com/
- Repositório: https://github.com/Fabos2005/doce-orbita-pit-ii
- Formulário de avaliação: https://forms.cloud.microsoft/r/0q6yHsUuGE

Este documento reúne o planejamento revisado e as mudanças de escopo e identidade. O PIT I original permanece como fonte da continuidade do projeto.
