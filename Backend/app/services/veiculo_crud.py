from ..models.veiculo import Veiculo, CategoriaVeiculo
from app import db

def create_veiculo(modelo: str, placa: str, categoria: CategoriaVeiculo | str, disponivel: bool):
    if isinstance(categoria, str):
        try:
            categoria = CategoriaVeiculo(categoria)
        except ValueError:
            raise ValueError("Categoria inválida")

    veiculo = Veiculo(modelo=modelo, placa=placa, categoria=categoria, disponivel=disponivel)

    try:
        db.session.add(veiculo)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return veiculo

def get_veiculo_by_id(veiculo_id: int):
    veiculo = Veiculo.query.get(veiculo_id)
    if not veiculo: raise ValueError("Veiculo não encontrado")
    return veiculo

def update_veiculo(veiculo_id: int, **kwargs):
    veiculo = get_veiculo_by_id(veiculo_id)

    for key, value in kwargs.items():
        if key == "status" and isinstance(value, str):
            try:
                value = CategoriaVeiculo(value)
            except ValueError:
                raise ValueError("Status inválido")
        setattr(veiculo, key, value)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return veiculo

def delete_veiculo(veiculo_id: int):
    veiculo = get_veiculo_by_id(veiculo_id)

    try:
        db.session.delete(veiculo)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    
    return True

def get_all_veiculos():
    veiculos = Veiculo.query.all()
    return veiculos