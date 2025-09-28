from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services.alocacao_crud import (
    create_alocacao, 
    get_alocacao_by_id, 
    update_alocacao, 
    delete_alocacao,
    get_all_alocacoes
)
alocacao_bp = Blueprint('alocacao',__name__)

@alocacao_bp.route('/alocacoes', methods=['GET'])
def listar_alocacoes():
    """
    GET /api/alocacoes - Lista todas as alocações
    """
    try:
        alocacoes = get_all_alocacoes()
        
        # Converter lista de objetos para JSON
        alocacoes_json = []
        for alocacao in alocacoes:
            alocacoes_json.append({
                'id': alocacao.id,
                'reserva_id': alocacao.reserva_id,
                'km_saida': alocacao.km_saida,
                'km_retorno': alocacao.km_retorno,
                'data_saida': alocacao.data_saida.isoformat(),
                'data_retorno': alocacao.data_retorno.isoformat()
            })
        
        return jsonify({
            'success': True,
            'count': len(alocacoes_json),
            'data': alocacoes_json
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@alocacao_bp.route('/alocacoes', methods=['POST'])
def criar_alocacao():
    """
    POST /api/alocacoes
    Body: {
        "reserva_id": 1,
        "km_saida": 50000.5,
        "km_retorno": 50200.0,
        "data_saida": "2024-01-15",
        "data_retorno": "2024-01-20"
    }
    """
    try:
        data = request.get_json()
        
        campos_obrigatorios = ['reserva_id', 'km_saida', 'km_retorno', 'data_saida', 'data_retorno']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({'error': f'Campo {campo} é obrigatório'}), 400
        
        # Converter strings de data para objetos date
        data_saida = datetime.strptime(data['data_saida'], '%Y-%m-%d').date()
        data_retorno = datetime.strptime(data['data_retorno'], '%Y-%m-%d').date()
        
        alocacao = create_alocacao(
            reserva_id=data['reserva_id'],
            km_saida=data['km_saida'],
            km_retorno=data['km_retorno'],
            data_saida=data_saida,
            data_retorno=data_retorno
        )
        
        return jsonify({
            'success': True,
            'message': 'Alocação criada com sucesso',
            'data': {
                'id': alocacao.id,
                'reserva_id': alocacao.reserva_id,
                'km_saida': alocacao.km_saida,
                'km_retorno': alocacao.km_retorno,
                'data_saida': alocacao.data_saida.isoformat(),
                'data_retorno': alocacao.data_retorno.isoformat()
            }
        }), 201
        
    except ValueError as e:
        # Erro de validação (ex: reserva não encontrada)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500
    
@alocacao_bp.route('/alocacoes/<int:alocacao_id>', methods=['GET'])
def buscar_alocacao(alocacao_id):
    """
    GET /api/alocacoes/1
    """
    try:
        # Chamar SEU service existente
        alocacao = get_alocacao_by_id(alocacao_id)
        
        return jsonify({
            'success': True,
            'data': {
                'id': alocacao.id,
                'reserva_id': alocacao.reserva_id,
                'km_saida': alocacao.km_saida,
                'km_retorno': alocacao.km_retorno,
                'data_saida': alocacao.data_saida.isoformat(),
                'data_retorno': alocacao.data_retorno.isoformat()
            }
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@alocacao_bp.route('/alocacoes/<int:alocacao_id>', methods=['PUT'])
def atualizar_alocacao(alocacao_id):
    """
    PUT /api/alocacoes/1
    Body: {
        "km_retorno": 50300.0,
        "data_retorno": "2024-01-21"
    }
    """
    try:
        data = request.get_json()
        
        # Converter datas se fornecidas
        if 'data_saida' in data:
            data['data_saida'] = datetime.strptime(data['data_saida'], '%Y-%m-%d').date()
        if 'data_retorno' in data:
            data['data_retorno'] = datetime.strptime(data['data_retorno'], '%Y-%m-%d').date()
        
        # Chamar SEU service existente
        alocacao = update_alocacao(alocacao_id, **data)
        
        return jsonify({
            'success': True,
            'message': 'Alocação atualizada com sucesso',
            'data': {
                'id': alocacao.id,
                'reserva_id': alocacao.reserva_id,
                'km_saida': alocacao.km_saida,
                'km_retorno': alocacao.km_retorno,
                'data_saida': alocacao.data_saida.isoformat(),
                'data_retorno': alocacao.data_retorno.isoformat()
            }
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@alocacao_bp.route('/alocacoes/<int:alocacao_id>', methods=['DELETE'])
def deletar_alocacao(alocacao_id):
    """
    DELETE /api/alocacoes/1
    """
    try:
        # Chamar SEU service existente
        delete_alocacao(alocacao_id)
        
        return jsonify({
            'success': True,
            'message': 'Alocação deletada com sucesso'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500