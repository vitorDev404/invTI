from flask import Blueprint, request
from database import get_db
from utils.auth_middleware import token_required, apenas_admin

racks_bp = Blueprint("racks", __name__, url_prefix="/racks")

# LISTAR TODOS (QUALQUER USUÁRIO LOGADO)
@racks_bp.get("/")
@token_required
def listar_todos():
    db = get_db()
    rows = db.execute("SELECT * FROM racks").fetchall()
    return [dict(row) for row in rows]

# BUSCAR POR ID (QUALQUER USUÁRIO LOGADO)
@racks_bp.get("/<int:id>")
@token_required
def buscar(id):
    db = get_db()
    row = db.execute("SELECT * FROM racks WHERE id = ?", (id,)).fetchone()
    if row:
        return dict(row)
    return {"erro": "Rack não encontrado"}, 404

# CRIAR NOVO (APENAS ADMIN)
@racks_bp.post("/")
@token_required
@apenas_admin
def criar():
    data = request.json
    db = get_db()

    db.execute("""
        INSERT INTO racks (patrimonio, rack, voltagem)
        VALUES (?, ?, ?)
    """, (
        data["patrimonio"],
        data["rack"],
        data["voltagem"]
    ))

    db.commit()
    return {"mensagem": "Rack criado com sucesso!"}, 201

# ATUALIZAR (APENAS ADMIN)
@racks_bp.put("/<int:id>")
@token_required
@apenas_admin
def atualizar(id):
    data = request.json
    db = get_db()

    db.execute("""
        UPDATE racks
        SET patrimonio = ?, rack = ?, voltagem = ?
        WHERE id = ?
    """, (
        data["patrimonio"],
        data["rack"],
        data["voltagem"],
        id
    ))

    db.commit()
    return {"mensagem": "Rack atualizado com sucesso!"}

# DELETAR (APENAS ADMIN)
@racks_bp.delete("/<int:id>")
@token_required
@apenas_admin
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM racks WHERE id = ?", (id,))
    db.commit()
    return {"mensagem": "Rack removido com sucesso!"}
