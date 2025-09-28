import { useState, useEffect } from 'react';
import Button from './shared/Button';
import Card from './shared/Card';
import Modal from './shared/Modal';
import api from '../services/api';
import useApi from '../hooks/useApi';
import './ClientePortal.css';

function ClientePortal({ user, onLogin, onLogout, onNavigateHome }) {
  const [step, setStep] = useState(user ? 'dashboard' : 'login');
  const [veiculos, setVeiculos] = useState([]);
  const [minhasReservas, setMinhasReservas] = useState([]);
  const [showReservaModal, setShowReservaModal] = useState(false);
  const [veiculoSelecionado, setVeiculoSelecionado] = useState(null);
  const { request, loading, error } = useApi();

  // Estado do formulário de login
  const [loginForm, setLoginForm] = useState({ nome: '', email: '' });
  
  // Estado do formulário de reserva
  const [reservaForm, setReservaForm] = useState({
    data_inicio: '',
    data_fim: '',
  });

  useEffect(() => {
    if (user) {
      carregarDados();
    }
  }, [user]);

  const carregarDados = async () => {
    try {
      // Carregar veículos disponíveis
      const veiculosData = await request(() => api.getVeiculosDisponiveis());
      setVeiculos(veiculosData || []);

      // Carregar minhas reservas
      const reservasData = await request(() => api.getReservasByUsuario(user.id));
      setMinhasReservas(reservasData || []);
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      setVeiculos([]);
      setMinhasReservas([]);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!loginForm.nome || !loginForm.email) {
      alert('Por favor, preencha nome e email');
      return;
    }

    try {
      // Verificar se usuário já existe
      let usuario = await request(() => api.getUsuarioByEmail(loginForm.email));
      
      // Se não existe, criar novo
      if (!usuario) {
        usuario = await request(() => api.createUsuario({
          nome: loginForm.nome,
          email: loginForm.email,
          bloqueado: false
        }));
      }

      onLogin(usuario);
      setStep('dashboard');
    } catch (err) {
      alert('Erro ao fazer login: ' + err.message);
    }
  };

  const handleReservar = (veiculo) => {
    setVeiculoSelecionado(veiculo);
    setShowReservaModal(true);
  };

  const handleConfirmarReserva = async (e) => {
    e.preventDefault();
    if (!reservaForm.data_inicio || !reservaForm.data_fim) {
      alert('Por favor, preencha as datas');
      return;
    }

    try {
      await request(() => api.createReserva({
        usuario_id: user.id,
        veiculo_id: veiculoSelecionado.id,
        inicio_previsto: reservaForm.data_inicio,
        final_previsto: reservaForm.data_fim,
        status: 'ativa'
      }));

      alert('Reserva criada com sucesso!');
      setShowReservaModal(false);
      setReservaForm({ data_inicio: '', data_fim: '' });
      carregarDados(); // Recarregar dados
    } catch (err) {
      alert('Erro ao criar reserva: ' + err.message);
    }
  };

  // Tela de Login
  if (step === 'login') {
    return (
      <div className="cliente-portal">
        <div className="cliente-container">
          <div className="cliente-header">
            <Button variant="secondary" onClick={onNavigateHome}>← Voltar</Button>
            <h1>Portal do Cliente</h1>
          </div>

          <Card className="login-card">
            <h2>Entrar</h2>
            <p>Digite seus dados para acessar o sistema</p>
            
            <form onSubmit={handleLogin} className="login-form">
              <div className="form-group">
                <label className="form-label">Nome:</label>
                <input
                  type="text"
                  className="form-control"
                  value={loginForm.nome}
                  onChange={(e) => setLoginForm({...loginForm, nome: e.target.value})}
                  placeholder="Seu nome completo"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Email:</label>
                <input
                  type="email"
                  className="form-control"
                  value={loginForm.email}
                  onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
                  placeholder="seu@email.com"
                  required
                />
              </div>

              <Button type="submit" disabled={loading} className="login-btn">
                {loading ? 'Entrando...' : 'Entrar'}
              </Button>
            </form>

            {error && <div className="error-message">{error}</div>}
          </Card>
        </div>
      </div>
    );
  }

  // Dashboard do Cliente
  return (
    <div className="cliente-portal">
      <div className="cliente-container">
        <div className="cliente-header">
          <Button variant="secondary" onClick={onNavigateHome}>← Voltar</Button>
          <div>
            <h1>Bem-vindo, {user?.nome}!</h1>
            <Button variant="danger" onClick={onLogout}>Sair</Button>
          </div>
        </div>

        {loading && <div className="loading">Carregando...</div>}
        {error && <div className="error-message">{error}</div>}

        {/* Seção de Veículos Disponíveis */}
        <section className="section">
          <h2>🚗 Veículos Disponíveis</h2>
          <div className="veiculos-grid">
            {veiculos.length === 0 ? (
              <p>Nenhum veículo disponível no momento.</p>
            ) : (
              veiculos.map(veiculo => (
                <Card key={veiculo.id} className="veiculo-card">
                  <h3>{veiculo.modelo}</h3>
                  <p><strong>Placa:</strong> {veiculo.placa}</p>
                  <p><strong>Categoria:</strong> {veiculo.categoria}</p>
                  <Button onClick={() => handleReservar(veiculo)}>
                    Reservar
                  </Button>
                </Card>
              ))
            )}
          </div>
        </section>

        {/* Seção de Minhas Reservas */}
        <section className="section">
          <h2>📋 Minhas Reservas</h2>
          {minhasReservas.length === 0 ? (
            <p>Você ainda não tem reservas.</p>
          ) : (
            <div className="reservas-list">
              {minhasReservas.map(reserva => (
                <Card key={reserva.id} className="reserva-card">
                  <div className="reserva-info">
                    <h4>Reserva #{reserva.id}</h4>
                    <p><strong>Período:</strong> {reserva.inicio_previsto} até {reserva.final_previsto}</p>
                    <p><strong>Status:</strong> 
                      <span className={`status status-${reserva.status}`}>
                        {reserva.status}
                      </span>
                    </p>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </section>

        {/* Modal de Reserva */}
        <Modal 
          isOpen={showReservaModal} 
          onClose={() => setShowReservaModal(false)}
          title={`Reservar ${veiculoSelecionado?.modelo}`}
        >
          <form onSubmit={handleConfirmarReserva}>
            <div className="form-group">
              <label className="form-label">Data de Retirada:</label>
              <input
                type="date"
                className="form-control"
                value={reservaForm.data_inicio}
                onChange={(e) => setReservaForm({...reservaForm, data_inicio: e.target.value})}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Data de Devolução:</label>
              <input
                type="date"
                className="form-control"
                value={reservaForm.data_fim}
                onChange={(e) => setReservaForm({...reservaForm, data_fim: e.target.value})}
                required
              />
            </div>

            <div className="modal-actions">
              <Button type="button" variant="secondary" onClick={() => setShowReservaModal(false)}>
                Cancelar
              </Button>
              <Button type="submit" disabled={loading}>
                {loading ? 'Reservando...' : 'Confirmar Reserva'}
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </div>
  );
}

export default ClientePortal;