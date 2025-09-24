from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, Date
from .. import db

class Multa(db.Model):
    __tablename__ = 'multa'

    id = db.Column(db.Integer, primary_key=True)
    alocacao_id = db.Column(db.Integer, db.ForeignKey('alocacao.id'), nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    valor = db.Column(Float, nullable=False)
    data = db.Column(Date, nullable=False)

    alocacao = db.relationship('Alocacao', back_populates='multas')