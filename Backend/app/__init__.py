# arquivo que cria o banco de dados e define rotas

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    # Importar blueprints (rotas)
    from app.routes.usuario_routes import usuario_bp
    from app.routes.veiculos_routes import veiculo_bp
    from app.routes.reserva_routes import reserva_bp
    from app.routes.alocacao_routes import alocacao_bp
    from app.routes.multa_routes import multa_bp

    app.register_blueprint(usuario_bp, url_prefix='/')
    app.register_blueprint(veiculo_bp, url_prefix='/')
    app.register_blueprint(reserva_bp, url_prefix='/')
    app.register_blueprint(alocacao_bp, url_prefix='/')
    app.register_blueprint(multa_bp, url_prefix='/')

    # Importar Tabelas/Classes para o banco
    from .models.usuario import Usuario
    from .models.veiculo import Veiculo
    from .models.reserva import Reserva
    from .models.alocacao import Alocacao
    from .models.multa import Multa

    with app.app_context():
        db.drop_all()
        db.create_all()

        from datetime import date

        u1 = Usuario(nome="Rafael", email="rafael@email.com", bloqueado=False)
        u2 = Usuario(nome="Maria", email="maria@email.com", bloqueado=False)

        v1 = Veiculo(modelo="Fiat Uno", placa="ABC-1234", categoria="economico", disponivel=True)
        v2 = Veiculo(modelo="BMW X5", placa="XYZ-5678", categoria="luxo", disponivel=True)
       
        v4 = Veiculo(modelo="Fiat Marea", placa="GHI-5432", categoria="economico", disponivel=True)
        v5 = Veiculo(modelo="Volkswagen Voyage", placa="JKL-1098", categoria="economico", disponivel=True)

        db.session.add_all([u1, u2, v1, v2, v4, v5])
        db.session.commit()

        r1 = Reserva(usuario_id=u1.id, veiculo_id=v1.id,
                    inicio_previsto=date(2025, 9, 25),
                    final_previsto=date(2025, 9, 30),
                    status="ativa")
        r2 = Reserva(usuario_id=u2.id, veiculo_id=v2.id,
                    inicio_previsto=date(2025, 10, 1),
                    final_previsto=date(2025, 10, 7),
                    status="ativa")
        db.session.add_all([r1, r2])
        db.session.commit()

        a1 = Alocacao(reserva_id=r1.id, km_saida=1200.0,
                    data_saida=date(2025, 9, 25),
                    data_retorno=date(2025, 9, 30))
        db.session.add(a1)
        db.session.commit()

        m1 = Multa(alocacao_id=a1.id, motivo="Excesso de velocidade", valor=150.0,
                    data=date(2025, 9, 26))
        db.session.add(m1)
        db.session.commit()

    return app