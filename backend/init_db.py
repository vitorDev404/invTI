import sqlite3
from pathlib import Path

# Caminho da pasta atual (backend/)
BASE_DIR = Path(__file__).resolve().parent

# Caminho do arquivo SQL
SQL_FILE = BASE_DIR / "sql" / "schema.sql"

# Caminho do banco que será criado
DB_FILE = BASE_DIR / "inventario.db"

def init_db():
    print("🔍 Lendo schema SQL...")

    if not SQL_FILE.exists():
        print("ERRO: arquivo schema.sql não encontrado.")
        return

    schema_sql = SQL_FILE.read_text(encoding="utf-8")

    print("Criando banco SQLite...")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.executescript(schema_sql)
        conn.commit()
        print(f" Banco criado/atualizado com sucesso!")
        print(f"Local do banco: {DB_FILE}")
    except Exception as e:
        print(" Erro ao executar o script SQL:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
