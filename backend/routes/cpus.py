from flask import Blueprint, request, jsonify
from database import get_db
from utils.auth_middleware import token_required, apenas_admin
import math

cpus_bp = Blueprint("cpus", __name__, url_prefix="/cpus")

def parse(name, default):
    try:
        return max(1, int(request.args.get(name, default)))
    except:
        return default

@cpus_bp.get("/")
@token_required
def listar():
    db = get_db()

    page = parse("page", 1)
    limit = parse("limit", 10)

    total = db.execute("SELECT COUNT(*) AS c FROM cpus").fetchone()["c"]
    total_paginas = math.ceil(total / limit)

    offset = (page - 1) * limit

    rows = db.execute("""
        SELECT * FROM cpus ORDER BY id DESC LIMIT ? OFFSET ?
    """, (limit, offset)).fetchall()

    return jsonify({
        "total": total,
        "pagina": page,
        "limit": limit,
        "total_paginas": total_paginas,
        "dados": [dict(r) for r in rows]
    })

@cpus_bp.get("/<int:id>")
@token_required
def buscar(id):
    db = get_db()
    r = db.execute("SELECT * FROM cpus WHERE id=?", (id,)).fetchone()
    return dict(r) if r else ({"erro": "Não encontrado"}, 404)

@cpus_bp.post("/")
@token_required
@apenas_admin
def criar():
    data = request.json
    db = get_db()

    db.execute("""
        INSERT INTO cpus (cpu_patrimonio, hostname, setor, impressora, ip, local)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["cpu_patrimonio"], data["hostname"], data["setor"],
        data["impressora"], data["ip"], data["local"]
    ))
    db.commit()

    return {"mensagem": "Criado!"}, 201

@cpus_bp.put("/<int:id>")
@token_required
@apenas_admin
def editar(id):
    data = request.json
    db = get_db()
    db.execute("""
        UPDATE cpus SET cpu_patrimonio=?, hostname=?, setor=?, impressora=?, ip=?, local=?
        WHERE id=?
    """, (
        data["cpu_patrimonio"], data["hostname"], data["setor"],
        data["impressora"], data["ip"], data["local"], id
    ))
    db.commit()

    return {"mensagem": "Atualizado!"}

@cpus_bp.delete("/<int:id>")
@token_required
@apenas_admin
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM cpus WHERE id=?", (id,))
    db.commit()
    return {"mensagem": "Removido!"}
