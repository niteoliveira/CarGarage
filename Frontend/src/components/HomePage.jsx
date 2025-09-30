import Card from './shared/Card';
import './HomePage.css';

function HomePage({ onNavigate }) {
  return (
    <div className="homepage">
      <div className="homepage-container">
        <header className="homepage-header">
          <h1>CarGarage</h1>
          <p>Sistema de Locação de Veículos</p>
        </header>
        
        <div className="homepage-cards">
          <Card
            title="Sou Cliente"
            description="Fazer reservas de veículos e consultar meus agendamentos"
            onClick={() => onNavigate('cliente')}
            className="homepage-card"
          />
          
          <Card
            title="Sou Funcionário"
            description="Gerenciar alocações, devoluções e sistema administrativo"
            onClick={() => onNavigate('funcionario')}
            className="homepage-card"
          />
        </div>
        
        <footer className="homepage-footer">
          <p>Desenvolvido por ADS_4</p>
        </footer>
      </div>
    </div>
  );
}

export default HomePage;