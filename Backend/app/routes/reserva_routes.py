from flask import Blueprint, request, jsonify
from datetime import datetime

from app.services.reserva_crud import (
    create_reserva,
    get_reserva_by_id,
    update_reserva,
    delete_reserva,
    get_all_reservas
)

reserva_bp = Blueprint('reserva', __name__)

@reserva_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    """
    GET /api/reservas - Lista todas as reservas
    """
    try:
        reservas = get_all_reservas()
        reservas_json = []
        for reserva in reservas:
            reservas_json.append({
                'id': reserva.id,
                'usuario_id': reserva.usuario_id,
                'veiculo_id': reserva.veiculo_id,
                'inicio_previsto': reserva.inicio_previsto.isoformat(),
                'final_previsto': reserva.final_previsto.isoformat(),
                'status': reserva.status.value
            })
        return jsonify({'success': True, 'count': len(reservas_json), 'data': reservas_json}), 200
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@reserva_bp.route('/reservas', methods=['POST'])
def criar_reserva():
    """
    POST /api/reservas
    Body: {
        "usuario_id": 1,
        "veiculo_id": 2,
        "inicio_previsto": "2024-01-15",
        "final_previsto": "2024-01-20",
        "status": "PENDENTE"
    }
    """
    try:
        data = request.get_json()
        campos_obrigatorios = ['usuario_id', 'veiculo_id', 'inicio_previsto', 'final_previsto', 'status']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({'error': f'Campo {campo} é obrigatório'}), 400

        inicio_previsto = datetime.strptime(data['inicio_previsto'], '%Y-%m-%d').date()
        final_previsto = datetime.strptime(data['final_previsto'], '%Y-%m-%d').date()

        reserva = create_reserva(
            usuario_id=data['usuario_id'],
            veiculo_id=data['veiculo_id'],
            inicio_previsto=inicio_previsto,
            final_previsto=final_previsto,
            status=data['status']
        )

        return jsonify({
            'success': True,
            'message': 'Reserva criada com sucesso',
            'data': {
                'id': reserva.id,
                'usuario_id': reserva.usuario_id,
                'veiculo_id': reserva.veiculo_id,
                'inicio_previsto': reserva.inicio_previsto.isoformat(),
                'final_previsto': reserva.final_previsto.isoformat(),
                'status': reserva.status.value
            }
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@reserva_bp.route('/reservas/<int:reserva_id>', methods=['GET'])
def buscar_reserva(reserva_id):
    """
    GET /api/reservas/1
    """
    try:
        reserva = get_reserva_by_id(reserva_id)
        return jsonify({
            'success': True,
            'data': {
                'id': reserva.id,
                'usuario_id': reserva.usuario_id,
                'veiculo_id': reserva.veiculo_id,
                'inicio_previsto': reserva.inicio_previsto.isoformat(),
                'final_previsto': reserva.final_previsto.isoformat(),
                'status': reserva.status.value
            }
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@reserva_bp.route('/reservas/<int:reserva_id>', methods=['PUT'])
def atualizar_reserva(reserva_id):
    """
    PUT /api/reservas/1
    Body: {
        "final_previsto": "2024-01-21",
        "status": "CONFIRMADA"
    }
    """
    try:
        data = request.get_json()
        if 'inicio_previsto' in data:
            data['inicio_previsto'] = datetime.strptime(data['inicio_previsto'], '%Y-%m-%d').date()
        if 'final_previsto' in data:
            data['final_previsto'] = datetime.strptime(data['final_previsto'], '%Y-%m-%d').date()

        reserva = update_reserva(reserva_id, **data)

        return jsonify({
            'success': True,
            'message': 'Reserva atualizada com sucesso',
            'data': {
                'id': reserva.id,
                'usuario_id': reserva.usuario_id,
                'veiculo_id': reserva.veiculo_id,
                'inicio_previsto': reserva.inicio_previsto.isoformat(),
                'final_previsto': reserva.final_previsto.isoformat(),
                'status': reserva.status.value
            }
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@reserva_bp.route('/reservas/<int:reserva_id>', methods=['DELETE'])
def deletar_reserva(reserva_id):
    """
    DELETE /api/reservas/1
    """
    try:
        delete_reserva(reserva_id)
        return jsonify({'success': True, 'message': 'Reserva deletada com sucesso'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception:
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
