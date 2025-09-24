from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, Date
import enum
from .. import db

class StatusReserva(enum.Enum):
    ativa = "ativa"
    cancelada = "cancelada"
    concluida = "concluida"

class Reserva(db.Model):
    __tablename__ = 'reserva'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    inicio_previsto = db.Column(Date, nullable=False)
    final_previsto = db.Column(Date, nullable=False)
    status = db.Column(Enum(StatusReserva), nullable=False, default=StatusReserva.ativa)

    usuario = db.relationship('Usuario', back_populates='reservas')
    veiculo = db.relationship('Veiculo', back_populates='reservas')
    alocacao = db.relationship('Alocacao', uselist=False, back_populates='reserva', cascade='all, delete-orphan')
