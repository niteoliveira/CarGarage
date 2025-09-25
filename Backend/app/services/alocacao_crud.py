from ..models.alocacao import Alocacao
from app import db
from datetime import date

def create_alocacao(reserva_id: int, km_saida: float, km_retorno: float, data_saida: date, data_retorno: date):
    from ..models.reserva import Reserva
    if not Reserva.query.get(reserva_id): raise ValueError("Chave estrangeira de Reserva não encontrada")
    
    alocacao = Alocacao(reserva_id=reserva_id, km_saida=km_saida, km_retorno=km_retorno, data_saida=data_saida, data_retorno=data_retorno)
    
    try:
        db.session.add(alocacao)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return alocacao

def get_alocacao_by_id(alocacao_id: int):
    alocacao = Alocacao.query.get(alocacao_id)
    if not alocacao: raise ValueError("Alocação não encontrada")
    return alocacao

def update_alocacao(alocacao_id: int, **kwargs):
    alocacao = get_alocacao_by_id(alocacao_id)
    
    for key, value in kwargs.items():
        setattr(alocacao, key, value)
    
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return alocacao

def delete_alocacao(alocacao_id: int):
    alocacao = get_alocacao_by_id(alocacao_id)
    
    try:
        db.session.delete(alocacao)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    
    return True