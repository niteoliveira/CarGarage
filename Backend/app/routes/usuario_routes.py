from flask import Blueprint, request, jsonify

from app.services.usuario_crud import (
    create_usuario,
    get_usuario_by_id,
    update_usuario,
    delete_usuario,
    get_all_usuarios
)

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """
    GET /api/usuarios - Lista todos os usuários
    """
    try:
        usuarios = get_all_usuarios()
        usuarios_json = []
        for usuario in usuarios:
            usuarios_json.append({
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'bloqueado': usuario.bloqueado
            })
        return jsonify({'success': True, 'count': len(usuarios_json), 'data': usuarios_json}), 200
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    """
    POST /api/usuarios
    Body: {
        "nome": "João",
        "email": "joao@email.com",
        "bloqueado": false
    }
    """
    try:
        data = request.get_json()
        campos_obrigatorios = ['nome', 'email']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({'error': f'Campo {campo} é obrigatório'}), 400

        bloqueado = data.get('bloqueado', False)

        usuario = create_usuario(
            nome=data['nome'],
            email=data['email'],
            bloqueado=bloqueado
        )

        return jsonify({
            'success': True,
            'message': 'Usuário criado com sucesso',
            'data': {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'bloqueado': usuario.bloqueado
            }
        }), 201
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
def buscar_usuario(usuario_id):
    """
    GET /api/usuarios/1
    """
    try:
        usuario = get_usuario_by_id(usuario_id)
        return jsonify({
            'success': True,
            'data': {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'bloqueado': usuario.bloqueado
            }
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    """
    PUT /api/usuarios/1
    Body: {
        "nome": "João Silva",
        "bloqueado": true
    }
    """
    try:
        data = request.get_json()
        usuario = update_usuario(usuario_id, **data)
        return jsonify({
            'success': True,
            'message': 'Usuário atualizado com sucesso',
            'data': {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'bloqueado': usuario.bloqueado
            }
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    """
    DELETE /api/usuarios/1
    """
    try:
        delete_usuario(usuario_id)
        return jsonify({'success': True, 'message': 'Usuário deletado com sucesso'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
