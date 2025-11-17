from flask import Blueprint, request, jsonify
from database import get_db
from utils.auth_middleware import token_required, apenas_admin
import math

cpu_itens_bp = Blueprint("cpu_itens", __name__, url_prefix="/cpu_itens")

def p(name, default):
    try:
        return max(1, int(request.args.get(name, default)))
    except:
        return default

# LISTAR ITENS DE UMA CPU (paginado)
@cpu_itens_bp.get("/cpu/<int:cpu_id>")
@token_required
def listar_por_cpu(cpu_id):
    db = get_db()

    page = p("page", 1)
    limit = p("limit", 10)

    total = db.execute("SELECT COUNT(*) AS c FROM cpu_itens WHERE cpu_id=?", (cpu_id,)).fetchone()["c"]
    total_paginas = math.ceil(total / limit)

    offset = (page - 1) * limit

    rows = db.execute("""
        SELECT * FROM cpu_itens
        WHERE cpu_id = ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (cpu_id, limit, offset)).fetchall()

    return jsonify({
        "total": total,
        "pagina": page,
        "limit": limit,
        "total_paginas": total_paginas,
        "dados": [dict(r) for r in rows]
    })

@cpu_itens_bp.get("/<int:id>")
@token_required
def buscar(id):
    db = get_db()
    r = db.execute("SELECT * FROM cpu_itens WHERE id=?", (id,)).fetchone()
    return dict(r) if r else ({"erro": "Não encontrado"}, 404)

@cpu_itens_bp.post("/")
@token_required
@apenas_admin
def criar():
    data = request.json
    db = get_db()

    db.execute("""
        INSERT INTO cpu_itens (cpu_id, tipo, patrimonio, descricao)
        VALUES (?, ?, ?, ?)
    """, (data["cpu_id"], data["tipo"], data["patrimonio"], data.get("descricao", "")))
    db.commit()

    return {"mensagem": "Item criado!"}, 201

@cpu_itens_bp.put("/<int:id>")
@token_required
@apenas_admin
def editar(id):
    data = request.json
    db = get_db()
    db.execute("""
        UPDATE cpu_itens SET tipo=?, patrimonio=?, descricao=? WHERE id=?
    """, (data["tipo"], data["patrimonio"], data.get("descricao", ""), id))
    db.commit()

    return {"mensagem": "Atualizado!"}

@cpu_itens_bp.delete("/<int:id>")
@token_required
@apenas_admin
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM cpu_itens WHERE id=?", (id,))
    db.commit()
    return {"mensagem": "Removido!"}
