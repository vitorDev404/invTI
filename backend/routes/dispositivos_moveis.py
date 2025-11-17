from flask import Blueprint, request, jsonify
from database import get_db
from utils.auth_middleware import token_required, apenas_admin
import math

dispositivos_bp = Blueprint("dispositivos", __name__, url_prefix="/dispositivos")

def parse_int_query(name, default, minimum=1):
    v = request.args.get(name, None)
    if not v:
        return default
    try:
        i = int(v)
        return i if i >= minimum else default
    except:
        return default

# LISTAR (com paginação)
@dispositivos_bp.get("/")
@token_required
def listar():
    db = get_db()

    page = parse_int_query("page", 1)
    limit = parse_int_query("limit", 10)

    total = db.execute("SELECT COUNT(*) AS c FROM dispositivos_moveis").fetchone()["c"]
    total_paginas = max(1, math.ceil(total / limit))

    offset = (page - 1) * limit
    rows = db.execute("""
        SELECT * FROM dispositivos_moveis
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (limit, offset)).fetchall()

    return jsonify({
        "total": total,
        "pagina": page,
        "limit": limit,
        "total_paginas": total_paginas,
        "dados": [dict(r) for r in rows]
    })

# BUSCAR POR ID
@dispositivos_bp.get("/<int:id>")
@token_required
def buscar(id):
    db = get_db()
    r = db.execute("SELECT * FROM dispositivos_moveis WHERE id=?", (id,)).fetchone()
    return dict(r) if r else ({"erro": "Não encontrado"}, 404)

# CRIAR
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
        """, (data["patrimonio"], data["modelo"], data["usuario"], data["cargo_unidade_setor"]))
        db.commit()
        return {"mensagem": "Criado com sucesso!"}, 201
    except Exception as e:
        return {"erro": str(e)}, 400

# EDITAR
@dispositivos_bp.put("/<int:id>")
@token_required
@apenas_admin
def editar(id):
    data = request.json
    db = get_db()
    db.execute("""
        UPDATE dispositivos_moveis
        SET patrimonio=?, modelo=?, usuario=?, cargo_unidade_setor=?
        WHERE id=?
    """, (data["patrimonio"], data["modelo"], data["usuario"], data["cargo_unidade_setor"], id))
    db.commit()
    return {"mensagem": "Atualizado!"}

# DELETAR
@dispositivos_bp.delete("/<int:id>")
@token_required
@apenas_admin
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM dispositivos_moveis WHERE id=?", (id,))
    db.commit()
    return {"mensagem": "Removido!"}
