import { useState, useEffect } from 'react';
import Button from './shared/Button';
import Card from './shared/Card';
import Modal from './shared/Modal';
import api from '../services/api';
import useApi from '../hooks/useApi';
import './FuncionarioPortal.css';

function FuncionarioPortal({ onNavigateHome }) {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [reservas, setReservas] = useState([]);
  const [alocacoes, setAlocacoes] = useState([]);
  const [veiculos, setVeiculos] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState('');
  const [itemSelecionado, setItemSelecionado] = useState(null);
  const { request, loading, error } = useApi();

  // Estados dos formulários
  const [alocacaoForm, setAlocacaoForm] = useState({
    km_saida: '',
    data_saida: new Date().toISOString().split('T')[0],
  });

  const [devolucaoForm, setDevolucaoForm] = useState({
    km_retorno: '',
    data_retorno: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      const [reservasData, alocacoesData, veiculosData, usuariosData] = await Promise.all([
        request(() => api.getReservas()),
        request(() => api.getAlocacoes()),
        request(() => api.getVeiculos()),
        request(() => api.getUsuarios()),
      ]);

      setReservas(reservasData || []);
      setAlocacoes(alocacoesData || []);
      setVeiculos(veiculosData || []);
      setUsuarios(usuariosData || []);
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      setReservas([]);
      setAlocacoes([]);
      setVeiculos([]);
      setUsuarios([]);
    }
  };

  const handleCriarAlocacao = (reserva) => {
    setItemSelecionado(reserva);
    setModalType('criar-alocacao');
    setShowModal(true);
  };

  const handleFinalizarAlocacao = (alocacao) => {
    setItemSelecionado(alocacao);
    setModalType('finalizar-alocacao');
    setShowModal(true);
  };

  const confirmarCriarAlocacao = async (e) => {
    e.preventDefault();
    if (!alocacaoForm.km_saida) {
      alert('Por favor, informe a quilometragem de saída');
      return;
    }

    try {
      await request(() => api.createAlocacao({
        reserva_id: itemSelecionado.id,
        km_saida: parseFloat(alocacaoForm.km_saida),
        km_retorno: null,
        data_saida: alocacaoForm.data_saida,
        data_retorno: itemSelecionado.final_previsto,
      }));

      alert('Alocação criada com sucesso!');
      setShowModal(false);
      setAlocacaoForm({ km_saida: '', data_saida: new Date().toISOString().split('T')[0] });
      carregarDados();
    } catch (err) {
      alert('Erro ao criar alocação: ' + err.message);
    }
  };

  const confirmarFinalizarAlocacao = async (e) => {
    e.preventDefault();
    if (!devolucaoForm.km_retorno) {
      alert('Por favor, informe a quilometragem de retorno');
      return;
    }

    try {
      await request(() => api.updateAlocacao(itemSelecionado.id, {
        km_retorno: parseFloat(devolucaoForm.km_retorno),
        data_retorno: devolucaoForm.data_retorno,
      }));

      alert('Alocação finalizada com sucesso!');
      setShowModal(false);
      setDevolucaoForm({ km_retorno: '', data_retorno: new Date().toISOString().split('T')[0] });
      carregarDados();
    } catch (err) {
      alert('Erro ao finalizar alocação: ' + err.message);
    }
  };

  const getUsuarioNome = (usuarioId) => {
    const usuario = usuarios.find(u => u.id === usuarioId);
    return usuario ? usuario.nome : 'Usuário não encontrado';
  };

  const getVeiculoInfo = (veiculoId) => {
    const veiculo = veiculos.find(v => v.id === veiculoId);
    return veiculo ? `${veiculo.modelo} - ${veiculo.placa}` : 'Veículo não encontrado';
  };

  const reservasAtivas = Array.isArray(reservas) ? reservas.filter(r => r.status === 'ativa') : [];
  const alocacoesPendentes = Array.isArray(alocacoes) ? alocacoes.filter(a => a.km_retorno === null) : [];
  const veiculosDisponiveis = Array.isArray(veiculos) ? veiculos.filter(v => v.disponivel) : [];

  return (
    <div className="funcionario-portal">
      <div className="funcionario-container">
        {/* Header */}
        <div className="funcionario-header">
          <Button variant="secondary" onClick={onNavigateHome}>← Voltar</Button>
          <h1>👔 Portal do Funcionário</h1>
        </div>

        {/* Navegação */}
        <nav className="funcionario-nav">
          <Button 
            variant={activeTab === 'dashboard' ? 'primary' : 'secondary'}
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Dashboard
          </Button>
          <Button 
            variant={activeTab === 'reservas' ? 'primary' : 'secondary'}
            onClick={() => setActiveTab('reservas')}
          >
            📋 Reservas
          </Button>
          <Button 
            variant={activeTab === 'alocacoes' ? 'primary' : 'secondary'}
            onClick={() => setActiveTab('alocacoes')}
          >
            🚗 Alocações
          </Button>
        </nav>

        {loading && <div className="loading">Carregando...</div>}
        {error && <div className="error-message">{error}</div>}

        {/* Dashboard */}
        {activeTab === 'dashboard' && (
          <div className="dashboard">
            <div className="stats-grid">
              <Card className="stat-card">
                <h3>📋 Reservas Ativas</h3>
                <div className="stat-number">{reservasAtivas.length}</div>
              </Card>
              <Card className="stat-card">
                <h3>🚗 Alocações Pendentes</h3>
                <div className="stat-number">{alocacoesPendentes.length}</div>
              </Card>
              <Card className="stat-card">
                <h3>✅ Veículos Disponíveis</h3>
                <div className="stat-number">{veiculosDisponiveis.length}</div>
              </Card>
              <Card className="stat-card">
                <h3>👥 Total Clientes</h3>
                <div className="stat-number">{usuarios.length}</div>
              </Card>
            </div>
          </div>
        )}

        {/* Reservas */}
        {activeTab === 'reservas' && (
          <div className="reservas-section">
            <h2>📋 Gerenciar Reservas</h2>
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Cliente</th>
                    <th>Veículo</th>
                    <th>Período</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {reservas.map(reserva => (
                    <tr key={reserva.id}>
                      <td>#{reserva.id}</td>
                      <td>{getUsuarioNome(reserva.usuario_id)}</td>
                      <td>{getVeiculoInfo(reserva.veiculo_id)}</td>
                      <td>{reserva.inicio_previsto} até {reserva.final_previsto}</td>
                      <td>
                        <span className={`status status-${reserva.status}`}>
                          {reserva.status}
                        </span>
                      </td>
                      <td>
                        {reserva.status === 'ativa' && (
                          <Button 
                            variant="success" 
                            onClick={() => handleCriarAlocacao(reserva)}
                          >
                            Criar Alocação
                          </Button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Alocações */}
        {activeTab === 'alocacoes' && (
          <div className="alocacoes-section">
            <h2>🚗 Gerenciar Alocações</h2>
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Reserva</th>
                    <th>KM Saída</th>
                    <th>KM Retorno</th>
                    <th>Data Saída</th>
                    <th>Data Retorno</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {alocacoes.map(alocacao => (
                    <tr key={alocacao.id}>
                      <td>#{alocacao.id}</td>
                      <td>#{alocacao.reserva_id}</td>
                      <td>{alocacao.km_saida}</td>
                      <td>{alocacao.km_retorno || '-'}</td>
                      <td>{alocacao.data_saida}</td>
                      <td>{alocacao.data_retorno}</td>
                      <td>
                        <span className={`status ${alocacao.km_retorno ? 'status-concluida' : 'status-ativa'}`}>
                          {alocacao.km_retorno ? 'Finalizada' : 'Em Andamento'}
                        </span>
                      </td>
                      <td>
                        {!alocacao.km_retorno && (
                          <Button 
                            variant="success" 
                            onClick={() => handleFinalizarAlocacao(alocacao)}
                          >
                            Finalizar
                          </Button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Modal para Criar Alocação */}
        <Modal 
          isOpen={showModal && modalType === 'criar-alocacao'} 
          onClose={() => setShowModal(false)}
          title="Criar Alocação"
        >
          <div className="modal-info">
            <p><strong>Cliente:</strong> {getUsuarioNome(itemSelecionado?.usuario_id)}</p>
            <p><strong>Veículo:</strong> {getVeiculoInfo(itemSelecionado?.veiculo_id)}</p>
          </div>
          
          <form onSubmit={confirmarCriarAlocacao}>
            <div className="form-group">
              <label className="form-label">Quilometragem de Saída:</label>
              <input
                type="number"
                className="form-control"
                value={alocacaoForm.km_saida}
                onChange={(e) => setAlocacaoForm({...alocacaoForm, km_saida: e.target.value})}
                placeholder="Ex: 50000"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Data de Saída:</label>
              <input
                type="date"
                className="form-control"
                value={alocacaoForm.data_saida}
                onChange={(e) => setAlocacaoForm({...alocacaoForm, data_saida: e.target.value})}
                required
              />
            </div>

            <div className="modal-actions">
              <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>
                Cancelar
              </Button>
              <Button type="submit" disabled={loading}>
                {loading ? 'Criando...' : 'Criar Alocação'}
              </Button>
            </div>
          </form>
        </Modal>

        {/* Modal para Finalizar Alocação */}
        <Modal 
          isOpen={showModal && modalType === 'finalizar-alocacao'} 
          onClose={() => setShowModal(false)}
          title="Finalizar Alocação"
        >
          <div className="modal-info">
            <p><strong>Alocação:</strong> #{itemSelecionado?.id}</p>
            <p><strong>KM Saída:</strong> {itemSelecionado?.km_saida}</p>
          </div>
          
          <form onSubmit={confirmarFinalizarAlocacao}>
            <div className="form-group">
              <label className="form-label">Quilometragem de Retorno:</label>
              <input
                type="number"
                className="form-control"
                value={devolucaoForm.km_retorno}
                onChange={(e) => setDevolucaoForm({...devolucaoForm, km_retorno: e.target.value})}
                placeholder="Ex: 50300"
                min={itemSelecionado?.km_saida}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Data de Retorno:</label>
              <input
                type="date"
                className="form-control"
                value={devolucaoForm.data_retorno}
                onChange={(e) => setDevolucaoForm({...devolucaoForm, data_retorno: e.target.value})}
                required
              />
            </div>

            <div className="modal-actions">
              <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>
                Cancelar
              </Button>
              <Button type="submit" disabled={loading}>
                {loading ? 'Finalizando...' : 'Finalizar Alocação'}
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </div>
  );
}

export default FuncionarioPortal;