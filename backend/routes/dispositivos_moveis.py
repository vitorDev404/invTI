from flask import Blueprint, request
from database import get_db
from utils.auth_middleware import token_required, apenas_admin

dispositivos_bp = Blueprint("dispositivos", __name__, url_prefix="/dispositivos")

# LISTAR TODOS (QUALQUER USUÁRIO LOGADO)
@dispositivos_bp.get("/")
@token_required
def listar_todos():
    db = get_db()
    rows = db.execute("SELECT * FROM dispositivos_moveis").fetchall()
    return [dict(row) for row in rows]

# BUSCAR POR ID
@dispositivos_bp.get("/<int:id>")
@token_required
def buscar(id):
    db = get_db()
    row = db.execute("SELECT * FROM dispositivos_moveis WHERE id = ?", (id,)).fetchone()
    if row:
        return dict(row)
    return {"erro": "Dispositivo não encontrado"}, 404

# CRIAR NOVO (APENAS ADMIN)
@dispositivos_bp.post("/")
@token_required
@apenas_admin
def criar():
    data = request.json
    db = get_db()

    try:
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

    except Exception as e:
        return {"erro": "Patrimônio já existe ou dados inválidos."}, 400

    return {"mensagem": "Dispositivo criado com sucesso!"}, 201

# ATUALIZAR (APENAS ADMIN)
@dispositivos_bp.put("/<int:id>")
@token_required
@apenas_admin
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

# DELETAR (APENAS ADMIN)
@dispositivos_bp.delete("/<int:id>")
@token_required
@apenas_admin
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM dispositivos_moveis WHERE id = ?", (id,))
    db.commit()
    return {"mensagem": "Removido com sucesso!"}
