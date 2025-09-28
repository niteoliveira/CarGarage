const API_BASE_URL = 'http://localhost:5000';

// Função helper para fazer requisições
const apiRequest = async (url, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// API endpoints
export const api = {
  // Usuários
  getUsuarios: async () => {
    const response = await apiRequest('/usuarios');
    return response.data || response;
  },
  createUsuario: async (data) => {
    const response = await apiRequest('/usuarios', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    return response.data || response;
  },
  getUsuarioByEmail: async (email) => {
    try {
      const usuarios = await api.getUsuarios();
      return usuarios.find(user => user.email === email);
    } catch (error) {
      console.error('Erro ao buscar usuário por email:', error);
      return null;
    }
  },

  // Veículos
  getVeiculos: async () => {
    const response = await apiRequest('/veiculos');
    return response.data || response;
  },
  getVeiculosDisponiveis: async () => {
    try {
      const veiculos = await api.getVeiculos();
      return veiculos.filter(veiculo => veiculo.disponivel);
    } catch (error) {
      console.error('Erro ao buscar veículos disponíveis:', error);
      return [];
    }
  },

  // Reservas
  getReservas: async () => {
    const response = await apiRequest('/reservas');
    return response.data || response;
  },
  createReserva: async (data) => {
    const response = await apiRequest('/reservas', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    return response.data || response;
  },
  getReservasByUsuario: async (usuarioId) => {
    try {
      const reservas = await api.getReservas();
      return reservas.filter(reserva => reserva.usuario_id === usuarioId);
    } catch (error) {
      console.error('Erro ao buscar reservas do usuário:', error);
      return [];
    }
  },

  // Alocações
  getAlocacoes: async () => {
    const response = await apiRequest('/alocacoes');
    return response.data || response;
  },
  createAlocacao: async (data) => {
    const response = await apiRequest('/alocacoes', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    return response.data || response;
  },
  updateAlocacao: async (id, data) => {
    const response = await apiRequest(`/alocacoes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
    return response.data || response;
  },
  deleteAlocacao: async (id) => {
    const response = await apiRequest(`/alocacoes/${id}`, {
      method: 'DELETE',
    });
    return response.data || response;
  },

  // Multas
  getMultas: async () => {
    const response = await apiRequest('/multas');
    return response.data || response;
  },
};

export default api;