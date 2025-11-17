from flask import Blueprint, request, jsonify
from database import get_db
from utils.auth_middleware import token_required, apenas_admin
import math

racks_bp = Blueprint("racks", __name__, url_prefix="/racks")

def parse_int(name, default):
    try:
        return max(1, int(request.args.get(name, default)))
    except:
        return default

@racks_bp.get("/")
@token_required
def listar():
    db = get_db()

    page = parse_int("page", 1)
    limit = parse_int("limit", 10)

    total = db.execute("SELECT COUNT(*) AS c FROM racks").fetchone()["c"]
    total_paginas = math.ceil(total / limit)

    offset = (page - 1) * limit
    rows = db.execute("""
        SELECT * FROM racks ORDER BY id DESC LIMIT ? OFFSET ?
    """, (limit, offset)).fetchall()

    return jsonify({
        "total": total,
        "pagina": page,
        "limit": limit,
        "total_paginas": total_paginas,
        "dados": [dict(r) for r in rows]
    })

@racks_bp.get("/<int:id>")
@token_required
def buscar(id):
    db = get_db()
    r = db.execute("SELECT * FROM racks WHERE id=?", (id,)).fetchone()
    return dict(r) if r else ({"erro": "Não encontrado"}, 404)

@racks_bp.post("/")
@token_required
@apenas_admin
def criar():
    data = request.json
    db = get_db()
    db.execute("""
        INSERT INTO racks (patrimonio, rack, voltagem)
        VALUES (?, ?, ?)
    """, (data["patrimonio"], data["rack"], data["voltagem"]))
    db.commit()
    return {"mensagem": "Criado com sucesso!"}, 201

@racks_bp.put("/<int:id>")
@token_required
@apenas_admin
def editar(id):
    data = request.json
    db = get_db()
    db.execute("""
        UPDATE racks SET patrimonio=?, rack=?, voltagem=? WHERE id=?
    """, (data["patrimonio"], data["rack"], data["voltagem"], id))
    db.commit()
    return {"mensagem": "Atualizado!"}

@racks_bp.delete("/<int:id>")
@token_required
@apenas_admin
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM racks WHERE id=?", (id,))
    db.commit()
    return {"mensagem": "Removido!"}
