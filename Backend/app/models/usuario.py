from flask_sqlalchemy import SQLAlchemy
from .. import db

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    bloqueado = db.Column(db.Boolean, nullable=False, default=False)

    reservas = db.relationship('Reserva', back_populates='usuario', cascade='all, delete-orphan')