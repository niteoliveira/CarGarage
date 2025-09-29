## 🎯 **Objetivo do Sistema**

Projetar e implementar um sistema para **gerenciar a alocação de veículos** por usuários autorizados (funcionários, professores, técnicos, etc) de uma instituição.

O sistema deve controlar o cadastro de carros, usuários, reservas, alocações, devoluções, disponibilidade dos veículos e aplicar regras como limites por perfil, restrições de uso, e penalidades por atrasos.

---

## 🧱 **Entidades principais**

| Entidade                 | Descrição                                                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Usuário**              | Pessoa autorizada a alocar veículos. Pode ser funcionário, professor, técnico, etc.                                        |
| **Veículo**              | Carros disponíveis para alocação. Inclui informações como placa, modelo, ano, categoria, combustível, etc.                 |
| **Reserva**              | Pedido para uso futuro de um veículo em um intervalo de tempo.                                                             |
| **Alocação**             | Evento de uso efetivo de um veículo por um usuário. Pode ser transformado a partir de uma reserva ou iniciado diretamente. |
| **Multa**                | Aplicada por atrasos, não comparecimento ou uso indevido do veículo.                                                       |

---

## 🔒 **Regras de negócio sugeridas**

1. **Multa por atraso**

   * Atrasos na devolução do veículo geram penalidade ou impedem novas alocações por X dias.

2. **Reserva obrigatória antecipada**

   * Algumas categorias de usuário só podem usar um veículo com reserva feita com antecedência mínima (ex: 24h).

3. **Checklist de saída e devolução**

   * Na retirada e devolução do veículo, devem ser registrados quilometragem, nível de combustível, estado geral (avarias, limpeza, etc).

4. **Período válido**

   * Uma alocação ou reserva não podem ter o final previsto antes que o inicio previsto.

---

## 📋 Funcionalidades principais do sistema

### 🔐 Autenticação

* Login para usuários e administradores.
* Sistema de permissões baseado no perfil.

### 🚗 Veículos

* Visualização de veículos disponíveis.

### 👤 Usuários

* Cadastro de usuários com perfil.
* Histórico de alocações e penalidades.

### 📅 Alocação / Reserva

* Criar reservas (com verificação de disponibilidade).
* Iniciar alocação (automática a partir da reserva ou direta).
* Finalizar alocação (devolução).
* Cancelar reserva/alocação (com ou sem penalidade dependendo da antecedência).

### 📊 Administração

* Relatórios de uso por período, por usuário ou por veículo.
* Visualização de reservas pendentes.
* Controle de penalidades.

---

## 🧭 Exemplo de fluxo de uso

1. **Usuário entra no sistema**
2. **Visualiza veículos disponíveis**
3. **Faz uma reserva para um veículo de sua categoria**
4. **No horário agendado, retira o veículo e inicia a alocação**
5. **Após o uso, devolve o carro, registra o checklist**
6. **Sistema registra atraso (se houver), aplica penalidade (se necessário)**

---

## 📦 Stack utilizada

- Python (Linguagem OO)
- Flask (Backend)
- SQLAlchemy (ORM)
- React (frontend)
- SQLite (Banco de Dados)

## 🗂️ Esboço da estrutura de pastas

```bash
/projeto-locadora
│
├─ backend/                      # API em Flask
│  ├─ app/                        # Pacote principal da aplicação
│  │  ├─ __init__.py              # Inicializa a aplicação Flask e o SQLAlchemy
│  │  ├─ models/                  # Modelos do banco de dados (ORM)
│  │  │  ├─ __init__.py
│  │  │  ├─ usuario.py
│  │  │  ├─ veiculo.py
│  │  │  ├─ reserva.py
│  │  │  ├─ alocacao.py
│  │  │  └─ multa.py
│  │  ├─ routes/                  # Rotas (endpoints da API)
│  │  │  ├─ __init__.py
│  │  │  ├─ usuario_routes.py
│  │  │  ├─ veiculo_routes.py
│  │  │  ├─ reserva_routes.py
│  │  │  ├─ alocacao_routes.py
│  │  │  └─ multa_routes.py
│  │  ├─ services/                # Lógica de negócio (opcional, para deixar rotas limpas)
│  │  │  ├─ __init__.py
│  │  │  ├─ reserva_service.py
│  │  │  └─ multa_service.py
│  │  ├─ schemas/                 # (opcional) validação de dados/serialização (pydantic/marshmallow)
│  │  └─ config.py                # Configurações (DB URI, variáveis de ambiente)
│  │
│  ├─ venv/                       # Ambiente virtual (não versionar no Git)
│  ├─ app.py                       # Ponto de entrada (inicia a app)
│  ├─ requirements.txt             # Dependências do Python
│  └─ instance/                    # Arquivos de configuração local (ex.: dev.sqlite)
│
├─ frontend/                       # Aplicação React
│  ├─ public/
│  ├─ src/
│  │  ├─ components/               # Componentes reutilizáveis
│  │  │  ├─ Navbar.jsx
│  │  │  └─ Footer.jsx
│  │  ├─ pages/                    # Páginas principais
│  │  │  ├─ Home.jsx
│  │  │  ├─ Usuarios.jsx
│  │  │  ├─ Veiculos.jsx
│  │  │  └─ Reservas.jsx
│  │  ├─ services/                 # Consumo da API (ex.: axios)
│  │  │  └─ api.js
│  │  ├─ App.jsx
│  │  └─ index.jsx
│  ├─ package.json
│  └─ vite.config.js (ou similar)
│
└─ docs/                           # Documentação
   ├─ DER.pdf                       # Diagrama Entidade-Relacionamento
   ├─ RelatorioTecnico.md
   └─ README.md
```
