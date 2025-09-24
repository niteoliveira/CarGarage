from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import enum
from .. import db

class CategoriaVeiculo(enum.Enum):
    economico = "economico"
    luxo = "luxo"
    SUV = "SUV"
    van = "van"

class Veiculo(db.Model):
    __tablename__ = 'veiculo'

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(255), nullable=False)
    placa = db.Column(db.String(255), nullable=False)
    categoria = db.Column(Enum(CategoriaVeiculo), nullable=False)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)

    reservas = db.relationship('Reserva', back_populates='veiculo')