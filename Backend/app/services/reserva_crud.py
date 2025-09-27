from ..models.reserva import Reserva, StatusReserva
from app import db
from datetime import date

def create_reserva(usuario_id: int, veiculo_id: int, inicio_previsto: date, final_previsto: date, status: StatusReserva | str):
    from ..models.veiculo import Veiculo
    from ..models.usuario import Usuario
    if not Usuario.query.get(usuario_id): raise ValueError("Chave estrangeira de Usuario não encontrada")
    if not Veiculo.query.get(veiculo_id): raise ValueError("Chave estrangeira de Veiculo não encontrada")
    
    if isinstance(status, str):
        try:
            status = StatusReserva(status)
        except ValueError:
            raise ValueError("Status inválido")

    reserva = Reserva(usuario_id=usuario_id, veiculo_id=veiculo_id, inicio_previsto=inicio_previsto, final_previsto=final_previsto, status=status)
    
    try:
        db.session.add(reserva)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return reserva

def get_reserva_by_id(reserva_id: int):
    reserva = Reserva.query.get(reserva_id)
    if not reserva: raise ValueError("Reserva não encontrada")
    return reserva

def update_reserva(reserva_id: int, **kwargs):
    reserva = get_reserva_by_id(reserva_id)

    for key, value in kwargs.items():
        if key == "status" and isinstance(value, str):
            try:
                value = StatusReserva(value)
            except ValueError:
                raise ValueError("Status inválido")
        setattr(reserva, key, value)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return reserva

def delete_reserva(reserva_id: int):
    reserva = get_reserva_by_id(reserva_id)

    try:
        db.session.delete(reserva)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    
    return True

def get_all_reservas():
    reservas = Reserva.query.all()
    return reservas