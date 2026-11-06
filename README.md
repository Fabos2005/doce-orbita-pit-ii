# Doce Órbita

Loja virtual de cupcakes para continuidade do PIT I e execução das três situações do PIT II. Projeto acadêmico com dados fictícios, pagamento e entrega simulados, sem cobrança.

## Executar

Python 3.12. Crie um ambiente virtual e instale `requirements.txt`. Configure `SECRET_KEY` aleatória com pelo menos32 caracteres, `ADMIN_PASSWORD` exclusiva com pelo menos12, e opcionalmente `DATABASE` com caminho absoluto. Execute `python run.py` e abra http://127.0.0.1:5000. Nunca use a senha pessoal na demonstração. O banco é criado na primeira execução e recebe três sabores de exemplo. Não apague o SQLite para atualizar o código.

PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
$env:SECRET_KEY = (.\.venv\Scripts\python -c "import secrets; print(secrets.token_hex(32))")
$env:ADMIN_PASSWORD = Read-Host 'Senha exclusiva da gestão (mínimo 12 caracteres)'
.\.venv\Scripts\python run.py
```

## Uso

Cliente: criar conta, buscar cupcake, selecionar quantidade, atualizar carrinho, informar entrega fictícia, confirmar pedido, simular pagamento e acompanhar andamento. Gestão: /gestao/entrar, cadastrar/editar/desativar produtos e avançar pedidos confirmados por preparo, saída e entrega. O cliente pode cancelar antes do pagamento aprovado; estoque retorna uma vez. Pagamento recusado permite nova tentativa.

## Organização

- app: modelo, controladores, telas, estilos e banco físico.
- docs/situacao-1: planejamento atualizado, histórias, UML, dados e interface.
- docs/situacao-2: manual e roteiros.
- docs/situacao-3: testes, formulário, laudo e melhorias após feedback.
- tests: suíte automatizada com bancos temporários.
- deploy: WSGI para PythonAnywhere.

Testar: `python -m unittest discover -s tests -v`. Resultados em docs/situacao-3. O teste automatizado não substitui avaliação visual nem os cinco participantes.

## Publicação gratuita

Preparado para a conta PythonAnywhere existente, sem upgrade. Enviar esta pasta para ~/cupcakes-pit-ii; criar ~/.config/cupcakes.json com SECRET_KEY, ADMIN_PASSWORD, DATABASE apontando para o banco exclusivo cupcakes.sqlite e COOKIE_SECURE="1"; arquivo privado com permissão0600. Configurar o virtualenv, instalar requirements, copiar deploy/pythonanywhere_wsgi.py para o WSGI e recarregar. Verificar HTTPS, cadastro, pedido, pagamento, entrega e persistência após reinício. Conservar a renovação mensal gratuita. A aplicação foi publicada e verificada no navegador, incluindo persistência após reinício.

Aplicação: https://fabrifeliciano.pythonanywhere.com/

Código: https://github.com/Fabos2005/doce-orbita-pit-ii

Avaliação: https://forms.cloud.microsoft/r/0q6yHsUuGE

Não é necessário instalar Python para usar o site. Cada avaliador cria uma conta com dados fictícios. As cinco avaliações foram coletadas, as três melhorias foram publicadas e o Word foi preenchido com os links dos vídeos. O PDF das cinco avaliações está concluído e disponível no material de entrega acadêmica. Consulte o estado detalhado e as limitações conhecidas em [QUALIDADE.md](docs/situacao-3/QUALIDADE.md).

## Vídeos da entrega

- [Apresentação inicial (9min35s)](https://www.youtube.com/watch?v=_3d2BDXhaKE).
- [Melhorias após os feedbacks (3min18s)](https://www.youtube.com/watch?v=FHVv_Q8VOn0).

Vídeos não listados. Os links também constam no Word oficial. A entrega à faculdade permanece não realizada até a confirmação do envio no AVA.
