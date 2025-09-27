from flask import Blueprint, request, jsonify
from datetime import datetime

from app.services.multa_crud import (
    create_multa,
    get_multa_by_id,
    update_multa,
    delete_multa,
    get_all_multas
)

multa_bp = Blueprint('multa', __name__)

@ multa_bp.route('/multas', methods=['GET'])
def listar_multas():
    """
    GET /api/multas - Lista todas as multas
    """
    try:
        multas = get_all_multas()
        multas_json = []
        for multa in multas:
            multas_json.append({
                'id': multa.id,
                'alocacao_id': multa.alocacao_id,
                'motivo': multa.motivo,
                'valor': multa.valor,
                'data': multa.data.isoformat()
            })
        return jsonify({
            'success': True,
            'count': len(multas_json),
            'data': multas_json
        }), 200
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@ multa_bp.route('/multas', methods=['POST'])
def criar_multa():
    """
    POST /api/multas
    Body: {
        "alocacao_id": 1,
        "motivo": "Atraso",
        "valor": 150.0,
        "data": "2024-01-20"
    }
    """
    try:
        data = request.get_json()
        campos_obrigatorios = ['alocacao_id', 'motivo', 'valor', 'data']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({'error': f'Campo {campo} é obrigatório'}), 400

        # Converter string de data para date
        data_obj = datetime.strptime(data['data'], '%Y-%m-%d').date()

        multa = create_multa(
            alocacao_id=data['alocacao_id'],
            motivo=data['motivo'],
            valor=data['valor'],
            data=data_obj
        )

        return jsonify({
            'success': True,
            'message': 'Multa criada com sucesso',
            'data': {
                'id': multa.id,
                'alocacao_id': multa.alocacao_id,
                'motivo': multa.motivo,
                'valor': multa.valor,
                'data': multa.data.isoformat()
            }
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@ multa_bp.route('/multas/<int:multa_id>', methods=['GET'])
def buscar_multa(multa_id):
    """
    GET /api/multas/1
    """
    try:
        multa = get_multa_by_id(multa_id)
        return jsonify({
            'success': True,
            'data': {
                'id': multa.id,
                'alocacao_id': multa.alocacao_id,
                'motivo': multa.motivo,
                'valor': multa.valor,
                'data': multa.data.isoformat()
            }
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@ multa_bp.route('/multas/<int:multa_id>', methods=['PUT'])
def atualizar_multa(multa_id):
    """
    PUT /api/multas/1
    Body: {
        "valor": 200.0,
        "data": "2024-01-21"
    }
    """
    try:
        data = request.get_json()
        if 'data' in data:
            data['data'] = datetime.strptime(data['data'], '%Y-%m-%d').date()

        multa = update_multa(multa_id, **data)

        return jsonify({
            'success': True,
            'message': 'Multa atualizada com sucesso',
            'data': {
                'id': multa.id,
                'alocacao_id': multa.alocacao_id,
                'motivo': multa.motivo,
                'valor': multa.valor,
                'data': multa.data.isoformat()
            }
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@ multa_bp.route('/multas/<int:multa_id>', methods=['DELETE'])
def deletar_multa(multa_id):
    """
    DELETE /api/multas/1
    """
    try:
        delete_multa(multa_id)
        return jsonify({'success': True, 'message': 'Multa deletada com sucesso'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
