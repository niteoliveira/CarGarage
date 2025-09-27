from ..models.usuario import Usuario
from app import db

def create_usuario(nome: str, email: str, bloqueado: bool = False):
    usuario = Usuario(nome=nome, email=email, bloqueado=bloqueado)
    
    try:
        db.session.add(usuario)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return usuario

def get_usuario_by_id(usuario_id: int):
    usuario = Usuario.query.get(usuario_id)
    if not usuario: raise ValueError("Usuario não encontrado")
    return usuario

def update_usuario(usuario_id: int, **kwargs):
    usuario = get_usuario_by_id(usuario_id)

    for key, value in kwargs.items():
        setattr(usuario, key, value)
    
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return usuario

def delete_usuario(usuario_id: int):
    usuario = get_usuario_by_id(usuario_id)

    try:
        db.session.delete(usuario)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return True

def get_all_usuarios():
    usuarios = Usuario.query.all()
    return usuarios