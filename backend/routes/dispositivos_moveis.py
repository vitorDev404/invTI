from flask import Blueprint, request
from database import get_db

# Blueprint do módulo
dispositivos_bp = Blueprint("dispositivos", __name__, url_prefix="/dispositivos")

# LISTAR TODOS
@dispositivos_bp.get("/")
def listar_todos():
    db = get_db()
    rows = db.execute("SELECT * FROM dispositivos_moveis").fetchall()
    return [dict(row) for row in rows]

# BUSCAR POR ID
@dispositivos_bp.get("/<int:id>")
def buscar(id):
    db = get_db()
    row = db.execute("SELECT * FROM dispositivos_moveis WHERE id = ?", (id,)).fetchone()
    if row:
        return dict(row)
    return {"erro": "Dispositivo não encontrado"}, 404

# CRIAR NOVO
@dispositivos_bp.post("/")
def criar():
    data = request.json
    db = get_db()

    db.execute("""
        INSERT INTO dispositivos_moveis (patrimonio, modelo, usuario, cargo_unidade_setor)
        VALUES (?, ?, ?, ?)
    """, (
        data["patrimonio"],
        data["modelo"],
        data["usuario"],
        data["cargo_unidade_setor"]
    ))

    db.commit()

    return {"mensagem": "Dispositivo criado com sucesso!"}, 201

# ATUALIZAR
@dispositivos_bp.put("/<int:id>")
def atualizar(id):
    data = request.json
    db = get_db()

    db.execute("""
        UPDATE dispositivos_moveis
        SET patrimonio = ?, modelo = ?, usuario = ?, cargo_unidade_setor = ?
        WHERE id = ?
    """, (
        data["patrimonio"],
        data["modelo"],
        data["usuario"],
        data["cargo_unidade_setor"],
        id
    ))

    db.commit()

    return {"mensagem": "Atualizado com sucesso!"}

# DELETAR
@dispositivos_bp.delete("/<int:id>")
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM dispositivos_moveis WHERE id = ?", (id,))
    db.commit()

    return {"mensagem": "Removido com sucesso!"}
