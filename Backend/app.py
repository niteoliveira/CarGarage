from app import create_app, db

# Criar a aplicação Flask
app = create_app()

if __name__ == '__main__':
    print("🚀 API CarGarage rodando em http://localhost:5000")
    print("📋 Endpoints Alocação:")
    print("   GET    /api/alocacoes        (Listar todas)")
    print("   POST   /api/alocacoes        (Criar nova)")
    print("   GET    /api/alocacoes/<id>   (Buscar uma)")
    print("   PUT    /api/alocacoes/<id>   (Atualizar)")
    print("   DELETE /api/alocacoes/<id>   (Deletar)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)