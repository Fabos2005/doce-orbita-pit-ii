# Conferência de requisitos e continuidade do PIT I

Responsável: Fabricio Feliciano Cardoso. Projeto: Doce Órbita.

## Base documental

O PIT I entregue, sob o nome provisório Cupcake App, escolheu a situação-problema 1 e propôs venda de cupcakes, cadastro, login, consulta de produtos e pedidos. Seu caso de uso apresenta essas quatro ações; o wireframe inicial apresenta o título Doce Órbita, busca, produtos em lista e Comprar. A continuidade preserva esses elementos. O documento relata cerca de dez horas na etapa anterior; essa informação não é reutilizada como tempo de execução do PIT II. Não há data de execução inventada.

Fontes: PIT_preenchido.pdf, páginas 1–3; material PIT I, páginas 27–49; material PIT II, páginas 30–39; template oficial PIT_atividade (8).docx. Os PDFs originais são preservados fora do código público por conterem dados acadêmicos pessoais.

## Matriz de rastreabilidade

| Exigência | Fonte | Artefato ou implementação | Verificação / situação |
|---|---|---|---|
| Tema loja virtual de cupcakes; vitrine, pedido, pagamento e entrega | PIT I p.27–29 | Catálogo, checkout, pagamentos e estados de entrega | Publicado; pagamento e entrega simulados |
| Cadastro, login, visualizar produtos e realizar pedido | PIT entregue p.1–2 | controllers.py, auth/catalog/checkout | Testes HTTP e modelo |
| Busca, lista de produtos e Comprar | PIT entregue p.3 | catalog.html, CSS responsivo | Implementado; catálogo inspecionado no Edge desktop e 390 px |
| Pelo menos 15 histórias com critérios, regras e prioridades | PIT I p.35–37 | REQUISITOS.md | 16 histórias com tarefas e aceitação |
| Mapa de afinidade, backlog priorizado, tarefas de 2–12 h | PIT I p.28–39 | REQUISITOS.md | Estimativas de planejamento, não horas realizadas |
| Caso de uso geral e casos expandidos | PIT I p.30–31 e 40–44 | MODELAGEM.md | Fluxos normais e alternativos |
| Classes e sequências | PIT I p.31 e 44–45 | MODELAGEM.md | Diagramas vinculados ao código |
| Wireframes, mockups, mapas conceitual e navegacional, erros | PIT I p.32–33 e 45–49 | INTERFACE.md e prototipo.html | Revisão visual browser pendente |
| Revisão do escopo, UML, atividades, IHC | PIT II p.30–31 | Documentos da situação 1 | Incorpora pagamento, entrega, gestão e falhas |
| Modelo conceitual, lógico normalizado e físico | PIT II p.31 | DADOS.md e app/schema.sql | SQLite com FK, CHECK e índices |
| Dicionário de dados e domínios | PIT II p.31 | DADOS.md | Campos, nulidade, limites, chaves |
| Front-end e back-end, MVC, tratamento de erros | PIT II p.32–34 | app/models.py, controllers.py, templates/static | Suíte em situacao-3/test-results.txt |
| GitHub, código, bibliotecas e manual | PIT II p.32 e 38 | requirements.txt, README e MANUAL.md | Código local; publicação GitHub bloqueada por permissão |
| Vídeo inicial narrado pelo aluno, pelo menos 5 min | PIT II p.38 e template | ROTEIROS.md | Gravação pendente |
| Cinco colegas ou profissionais, formulário e snapshots | PIT II p.35–36 e 39 | FORMULARIO.md | Coleta real pendente; Forms atualizado para cupcakes; anexos externos exigem consolidação |
| PDF com cinco opiniões e testes | PIT II p.39 | Após coleta real | Pendente; não fabricado |
| Correções, melhorias pertinentes, documentação, retestes | PIT II p.35–39 | QUALIDADE.md | Correção técnica inicial registrada; feedback externo pendente |
| Segundo vídeo mostrando mudanças, até 5 min | PIT II p.36/39 e template | ROTEIROS.md | Pendente após avaliações |
| Word oficial preenchido com links | Template do AVA | PIT-II-Cupcakes-Atividade.docx | Rascunho até publicar e completar avaliações/vídeos |

## Decisões de implementação

Os documentos não impõem uma marca de banco, cores específicas, gateway de pagamentos ou transportadora. SQLite é adotado para uma instância WSGI com armazenamento persistente; Python/Flask implementa MVC, HTML/CSS/JavaScript a apresentação. A identidade mantém Doce Órbita e usa fundo claro, rosa e tons de confeitaria. O catálogo mantém a lista e a busca do protótipo original. A taxa de entrega demonstrativa é R$8,00, explicitada antes da confirmação; é uma regra definida nesta revisão, não um valor fornecido pelo enunciado.

Pagamento: adaptador didático local com Pix/cartão, aprovação e recusa persistidos. Não existe integração bancária, coleta de cartão, cobrança, Pix real, estorno ou entrega física. A aceitabilidade da simulação deve ser confirmada com o tutor; se exigir gateway, será necessária conta de testes e credenciais próprias do provedor. Nenhum serviço pago será habilitado.

O artigo indicado pelo briefing foi consultado: https://novonegocio.com.br/ideias-de-negocios/stands-ou-loja-de-cupcakes/ (consulta em 24/10/2026). Ele orienta variedade de sabores, apresentação e vendas/entregas online; daí a descrição de sabor, catálogo e acompanhamento. Seus números comerciais não foram adotados como orçamento. O vídeo mencionado no material não foi localizado no conteúdo textual atual da página; não se afirma que foi assistido.

## Limites antes da entrega

A aplicação não está autorizada para vendas reais. A hospedagem e os fluxos principais foram verificados. Faltam concluir documentação visual, cinco avaliações reais, PDF das avaliações, vídeos e fechamento do laudo/Word. Não se declara conformidade integral até concluir a matriz com evidências. Recuperação de senha, limitador de tentativas distribuído, expiração automática de reservas, e-mails e pagamentos reais ficam fora da demonstração e devem ser considerados antes de operação comercial.
