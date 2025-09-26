from app import create_app, db
from flask_cors import CORS

# Criar a aplicação Flask
app = create_app()
CORS(app)#esse CORS é para a instancia app conseguir receber requisicoes de qualquer lugar

if __name__ == '__main__':
    print("🚀 API CarGarage rodando em http://localhost:5000")
    print("📋 Endpoints Alocação:")
    print("   GET    /api/alocacoes        (Listar todas)")
    print("   POST   /api/alocacoes        (Criar nova)")
    print("   GET    /api/alocacoes/<id>   (Buscar uma)")
    print("   PUT    /api/alocacoes/<id>   (Atualizar)")
    print("   DELETE /api/alocacoes/<id>   (Deletar)")
    print("")
    print("🚗 Endpoints Veículos:")
    print("   GET    /api/veiculos         (Listar todos)")
    print("   POST   /api/veiculos         (Criar novo)")
    print("   GET    /api/veiculos/<id>    (Buscar um)")
    print("   PUT    /api/veiculos/<id>    (Atualizar)")
    print("   DELETE /api/veiculos/<id>    (Deletar)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)