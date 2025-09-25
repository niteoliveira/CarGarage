# Script de teste para criação de um banco sqlite, inserção de dados e consulta basica em tabelas

from app import create_app, db
from app.models.usuario import Usuario
from app.models.veiculo import Veiculo
from app.models.reserva import Reserva
from app.models.alocacao import Alocacao
from app.models.multa import Multa
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    u1 = Usuario(nome="Rafael", email="rafael@email.com", bloqueado=False)
    u2 = Usuario(nome="Maria", email="maria@email.com", bloqueado=False)

    v1 = Veiculo(modelo="Fiat Uno", placa="ABC-1234", categoria="economico", disponivel=True)
    v2 = Veiculo(modelo="BMW X5", placa="XYZ-5678", categoria="luxo", disponivel=True)

    db.session.add_all([u1, u2, v1, v2])
    db.session.commit()

    r1 = Reserva(usuario_id=u1.id, veiculo_id=v1.id,
                inicio_previsto=date(2025, 9, 25),
                final_previsto=date(2025, 9, 30),
                status="ativa")
    db.session.add(r1)
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

    print("Usuarios:", Usuario.query.all())
    print("Veiculos:", Veiculo.query.all())
    print("Reservas:", Reserva.query.all())
    print("Alocacoes:", Alocacao.query.all())
    print("Multas:", Multa.query.all())
