# arquivo que cria o banco de dados e adiciona as tabelas (objetos) definidas em models 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# instância geral do anco sqlite
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes.alocacao_routes import alocacao_bp
    app.register_blueprint(alocacao_bp, url_prefix='/api')

    from .models.usuario import Usuario
    from .models.veiculo import Veiculo
    from .models.reserva import Reserva
    from .models.alocacao import Alocacao
    from .models.multa import Multa

    with app.app_context():
        db.create_all()

    return app
