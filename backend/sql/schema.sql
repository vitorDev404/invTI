PRAGMA foreign_keys = ON;

-- Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    nivel_acesso TEXT DEFAULT 'usuario'
);

-- Dispositivos Móveis
CREATE TABLE IF NOT EXISTS dispositivos_moveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patrimonio TEXT UNIQUE NOT NULL,
    modelo TEXT,
    usuario TEXT,
    cargo_unidade_setor TEXT
);

-- Racks
CREATE TABLE IF NOT EXISTS racks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patrimonio TEXT UNIQUE NOT NULL,
    rack TEXT,
    voltagem TEXT
);

-- Impressoras
CREATE TABLE IF NOT EXISTS impressoras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT,
    unidade TEXT,
    local TEXT,
    numero_serie TEXT,
    ip_equipamento TEXT,
    nome_impressora_servidor TEXT,
    ndd TEXT,
    mac TEXT,
    observacoes TEXT
);

-- CPU (pai)
CREATE TABLE IF NOT EXISTS cpus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu_patrimonio TEXT UNIQUE NOT NULL,
    hostname TEXT,
    setor TEXT,
    impressora TEXT,
    ip TEXT,
    local TEXT
);

-- Itens vinculados a uma CPU (filhos)
CREATE TABLE IF NOT EXISTS cpu_itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu_id INTEGER NOT NULL,
    tipo TEXT NOT NULL, -- monitor, tv, nobreak, zebra, etc.
    patrimonio TEXT,
    descricao TEXT,
    FOREIGN KEY (cpu_id) REFERENCES cpus(id) ON DELETE CASCADE
);

-- Logs (opcional)
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    acao TEXT,
    tabela TEXT,
    registro_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
