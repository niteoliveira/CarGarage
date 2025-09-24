PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Usuario (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    bloqueado INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Veiculo (
    id INTEGER PRIMARY KEY,
    modelo TEXT NOT NULL,
    placa TEXT NOT NULL,
    categoria TEXT NOT NULL CHECK(categoria IN ('econômico','luxo','SUV','van')),
    disponivel INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Reserva (
    id INTEGER PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    veiculo_id INTEGER NOT NULL,
    inicio_previsto DATE NOT NULL,
    final_previsto DATE NOT NULL,
    status TEXT NOT NULL DEFAULT 'ativa' CHECK(status IN ('ativa', 'cancelada', 'concluida')),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (veiculo_id) REFERENCES Veiculo(id)
);

CREATE TABLE IF NOT EXISTS Alocacao (
    id INTEGER PRIMARY KEY,
    reserva_id INTEGER NOT NULL,
    km_saida REAL NOT NULL,
    km_retorno REAL,
    data_saida DATE NOT NULL,
    data_retorno DATE NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES Reserva(id)
);

CREATE TABLE IF NOT EXISTS Multa (
    id INTEGER PRIMARY KEY,
    alocacao_id INTEGER NOT NULL,
    motivo TEXT NOT NULL,
    valor REAL NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (alocacao_id) REFERENCES Alocacao(id)
);
