from flask import Blueprint, request, jsonify
from app.services.veiculo_crud import (
    create_veiculo,
    get_veiculo_by_id,
    update_veiculo,
    delete_veiculo,
    get_all_veiculos
)
from app.models.veiculo import CategoriaVeiculo

veiculo_bp = Blueprint('veiculo', __name__)

@veiculo_bp.route('/veiculos', methods=['GET'])
def listar_veiculos():
    """
    GET /api/veiculos - Lista todos os veículos
    """
    try:
        veiculos = get_all_veiculos()
        
        # Converter lista de objetos para JSON
        veiculos_json = []
        for veiculo in veiculos:
            veiculos_json.append({
                'id': veiculo.id,
                'modelo': veiculo.modelo,
                'placa': veiculo.placa,
                'categoria': veiculo.categoria.value,
                'disponivel': veiculo.disponivel
            })
        
        return jsonify({
            'success': True,
            'count': len(veiculos_json),
            'data': veiculos_json
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@veiculo_bp.route('/veiculos', methods=['POST'])
def criar_veiculo():
    """
    POST /api/veiculos
    Body: {
        "modelo": "Civic 2024",
        "placa": "ABC-1234",
        "categoria": "economico",
        "disponivel": true
    }
    """
    try:
        data = request.get_json()
        
        campos_obrigatorios = ['modelo', 'placa', 'categoria']
        for campo in campos_obrigatorios:
            if campo not in data:
                return jsonify({'error': f'Campo {campo} é obrigatório'}), 400
        
        # Validar categoria
        try:
            categoria = CategoriaVeiculo(data['categoria'])
        except ValueError:
            return jsonify({'error': 'Categoria inválida. Opções: economico, luxo, SUV, van'}), 400
        
        veiculo = create_veiculo(
            modelo=data['modelo'],
            placa=data['placa'],
            categoria=categoria,
            dispoinvel=data.get('disponivel', True)
        )
        
        return jsonify({
            'success': True,
            'message': 'Veículo criado com sucesso',
            'data': {
                'id': veiculo.id,
                'modelo': veiculo.modelo,
                'placa': veiculo.placa,
                'categoria': veiculo.categoria.value,
                'disponivel': veiculo.disponivel
            }
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@veiculo_bp.route('/veiculos/<int:veiculo_id>', methods=['GET'])
def buscar_veiculo(veiculo_id):
    """
    GET /api/veiculos/1
    """
    try:
        veiculo = get_veiculo_by_id(veiculo_id)
        
        return jsonify({
            'success': True,
            'data': {
                'id': veiculo.id,
                'modelo': veiculo.modelo,
                'placa': veiculo.placa,
                'categoria': veiculo.categoria.value,
                'disponivel': veiculo.disponivel
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

@veiculo_bp.route('/veiculos/<int:veiculo_id>', methods=['PUT'])
def atualizar_veiculo(veiculo_id):
    """
    PUT /api/veiculos/1
    Body: {
        "modelo": "Civic 2025",
        "disponivel": false
    }
    """
    try:
        data = request.get_json()
        
        # Validar categoria se fornecida
        if 'categoria' in data:
            try:
                CategoriaVeiculo(data['categoria'])
            except ValueError:
                return jsonify({'error': 'Categoria inválida. Opções: economico, luxo, SUV, van'}), 400
        
        veiculo = update_veiculo(veiculo_id, **data)
        
        return jsonify({
            'success': True,
            'message': 'Veículo atualizado com sucesso',
            'data': {
                'id': veiculo.id,
                'modelo': veiculo.modelo,
                'placa': veiculo.placa,
                'categoria': veiculo.categoria.value,
                'disponivel': veiculo.disponivel
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

@veiculo_bp.route('/veiculos/<int:veiculo_id>', methods=['DELETE'])
def deletar_veiculo(veiculo_id):
    """
    DELETE /api/veiculos/1
    """
    try:
        delete_veiculo(veiculo_id)
        
        return jsonify({
            'success': True,
            'message': 'Veículo deletado com sucesso'
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
