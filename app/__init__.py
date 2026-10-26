import os
import secrets
import hmac
from pathlib import Path
from flask import Flask, session, request, abort
from . import models

def create_app(config=None):
    app=Flask(__name__,instance_relative_config=True)
    app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY'),ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD'),DATABASE=os.environ.get('DATABASE',str(Path(app.instance_path)/'cupcakes.sqlite')),SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE='Lax',SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE')=='1',MAX_CONTENT_LENGTH=65536)
    if config:app.config.update(config)
    if not app.config['SECRET_KEY'] or len(app.config['SECRET_KEY'])<32:raise RuntimeError('Configure SECRET_KEY com pelo menos 32 caracteres.')
    if not app.config['ADMIN_PASSWORD'] or len(app.config['ADMIN_PASSWORD'])<12:raise RuntimeError('Configure ADMIN_PASSWORD com pelo menos 12 caracteres.')
    Path(app.config['DATABASE']).parent.mkdir(parents=True,exist_ok=True)
    app.teardown_appcontext(models.close_db)
    with app.app_context():models.init_db()
    @app.before_request
    def csrf():
        session.setdefault('csrf',secrets.token_urlsafe(32))
        if request.method=='POST' and not hmac.compare_digest(str(session['csrf']),str(request.form.get('csrf',''))):abort(400,description='Sessão expirada ou formulário inválido. Recarregue a página.')
    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['X-Frame-Options']='DENY'
        response.headers['Referrer-Policy']='same-origin'
        response.headers['Content-Security-Policy']="default-src 'self'; style-src 'self'; img-src 'self' data:; script-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'"
        response.headers['Cache-Control']='no-store'
        return response
    @app.template_filter('money')
    def money(cents):return 'R$ '+f'{cents/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
    @app.context_processor
    def context():return dict(cart_count=sum(session.get('cart',{}).values()),next_status=models.NEXT)
    from .controllers import bp
    app.register_blueprint(bp)
    for code in (400,403,404,413,500):
        app.register_error_handler(code,lambda e:(__import__('flask').render_template('error.html',code=e.code,message=e.description if e.code!=500 else 'Não foi possível concluir. Tente novamente.'),e.code))
    return app
