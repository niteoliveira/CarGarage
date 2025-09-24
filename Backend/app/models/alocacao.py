from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, Date
from .. import db

class Alocacao(db.Model):
    __tablename__ = 'alocacao'

    id = db.Column(db.Integer, primary_key=True)
    reserva_id = db.Column(db.Integer, db.ForeignKey('reserva.id'), nullable=False)
    km_saida = db.Column(Float, nullable=False)
    km_retorno = db.Column(Float, nullable=True)
    data_saida = db.Column(Date, nullable=False)
    data_retorno = db.Column(Date, nullable=False)

    reserva = db.relationship('Reserva', back_populates='alocacao')
    multas = db.relationship('Multa', back_populates='alocacao', cascade='all, delete-orphan')
