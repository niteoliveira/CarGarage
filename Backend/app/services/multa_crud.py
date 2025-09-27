from ..models.multa import Multa
from app import db
from datetime import date

def create_multa(alocacao_id: int, motivo: str, valor: float, data: date):
    from ..models.alocacao import Alocacao
    if not Alocacao.query.get(alocacao_id): raise ValueError("Chave estrangeira não encontrada")

    multa = Multa(alocacao_id=alocacao_id, motivo=motivo, valor=valor, data=data)
    try:
        db.session.add(multa)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return multa

def get_multa_by_id(multa_id: int):
    multa = Multa.query.get(multa_id)
    if not multa: raise ValueError("Multa não encontrada")
    return multa

def update_multa(multa_id: int, **kwargs):
    multa = get_multa_by_id(multa_id)

    for key, value in kwargs.items():
        setattr(multa, key, value)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return multa

def delete_multa(multa_id: int):
    multa = get_multa_by_id(multa_id)

    try:
        db.session.delete(multa)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return True

def get_all_multas():
    multas = Multa.query.all()
    return multas