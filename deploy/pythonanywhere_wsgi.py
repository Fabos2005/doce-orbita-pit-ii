"""Copiar para WSGI após configurar caminhos/variáveis privados na hospedagem."""
import json, os, sys, time
from pathlib import Path
project=Path.home()/'cupcakes-pit-ii'
sys.path.insert(0,str(project))
os.environ.update(json.loads((Path.home()/'.config'/'cupcakes.json').read_text()))
os.environ['TZ']='America/Sao_Paulo'
time.tzset()
from app import create_app
application=create_app()
