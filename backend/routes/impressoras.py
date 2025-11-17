from flask import Blueprint, request, jsonify
from database import get_db
from utils.auth_middleware import token_required, apenas_admin
import math

impressoras_bp = Blueprint("impressoras", __name__, url_prefix="/impressoras")

def num(name, default):
    try:
        return max(1, int(request.args.get(name, default)))
    except:
        return default

@impressoras_bp.get("/")
@token_required
def listar():
    db = get_db()

    page = num("page", 1)
    limit = num("limit", 10)

    total = db.execute("SELECT COUNT(*) AS c FROM impressoras").fetchone()["c"]
    total_paginas = math.ceil(total / limit)

    offset = (page - 1) * limit

    rows = db.execute("""
        SELECT * FROM impressoras ORDER BY id DESC LIMIT ? OFFSET ?
    """, (limit, offset)).fetchall()

    return jsonify({
        "total": total,
        "pagina": page,
        "limit": limit,
        "total_paginas": total_paginas,
        "dados": [dict(r) for r in rows]
    })

@impressoras_bp.get("/<int:id>")
@token_required
def buscar(id):
    db = get_db()
    r = db.execute("SELECT * FROM impressoras WHERE id=?", (id,)).fetchone()
    return dict(r) if r else ({"erro": "Não encontrada"}, 404)

@impressoras_bp.post("/")
@token_required
@apenas_admin
def criar():
    data = request.json
    db = get_db()

    db.execute("""
        INSERT INTO impressoras (modelo, unidade, local, numero_serie, ip_equipamento,
                                 nome_impressora_servidor, ndd, mac, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["modelo"], data["unidade"], data["local"], data["numero_serie"],
        data["ip_equipamento"], data["nome_impressora_servidor"],
        data["ndd"], data["mac"], data.get("observacoes", "")
    ))
    db.commit()

    return {"mensagem": "Criada!"}, 201

@impressoras_bp.put("/<int:id>")
@token_required
@apenas_admin
def editar(id):
    data = request.json
    db = get_db()
    db.execute("""
        UPDATE impressoras SET modelo=?, unidade=?, local=?, numero_serie=?, 
            ip_equipamento=?, nome_impressora_servidor=?, ndd=?, mac=?, observacoes=?
        WHERE id=?
    """, (
        data["modelo"], data["unidade"], data["local"], data["numero_serie"],
        data["ip_equipamento"], data["nome_impressora_servidor"],
        data["ndd"], data["mac"], data.get("observacoes", ""), id
    ))
    db.commit()

    return {"mensagem": "Atualizada!"}

@impressoras_bp.delete("/<int:id>")
@token_required
@apenas_admin
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM impressoras WHERE id=?", (id,))
    db.commit()
    return {"mensagem": "Removida!"}
