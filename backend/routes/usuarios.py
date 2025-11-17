from flask import Blueprint, request, jsonify
from database import get_db
from utils.hash import gerar_hash, verificar_senha
from utils.auth_middleware import token_required, apenas_admin
import math

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

def q(name, default):
    try:
        return max(1, int(request.args.get(name, default)))
    except:
        return default

@usuarios_bp.get("/")
@token_required
@apenas_admin
def listar():
    db = get_db()

    page = q("page", 1)
    limit = q("limit", 10)

    total = db.execute("SELECT COUNT(*) AS c FROM usuarios").fetchone()["c"]
    total_paginas = math.ceil(total / limit)

    offset = (page - 1) * limit

    rows = db.execute("""
        SELECT id, nome, email, nivel_acesso 
        FROM usuarios 
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

# CRIAR USUÁRIO
@usuarios_bp.post("/")
@token_required
@apenas_admin
def criar():
    data = request.json
    db = get_db()

    senha_hash = gerar_hash(data["senha"])

    try:
        db.execute("""
            INSERT INTO usuarios (nome, email, senha_hash, nivel_acesso)
            VALUES (?, ?, ?, ?)
        """, (data["nome"], data["email"], senha_hash, data.get("nivel_acesso", "usuario")))
        db.commit()
        return {"mensagem": "Usuário criado!"}, 201
    except Exception as e:
        return {"erro": str(e)}, 400

# EDITAR USUÁRIO
@usuarios_bp.put("/<int:id>")
@token_required
@apenas_admin
def editar(id):
    data = request.json
    db = get_db()

    if "senha" in data and data["senha"].strip():
        senha_hash = gerar_hash(data["senha"])
        db.execute("""
            UPDATE usuarios SET nome=?, email=?, nivel_acesso=?, senha_hash=? WHERE id=?
        """, (data["nome"], data["email"], data["nivel_acesso"], senha_hash, id))
    else:
        db.execute("""
            UPDATE usuarios SET nome=?, email=?, nivel_acesso=? WHERE id=?
        """, (data["nome"], data["email"], data["nivel_acesso"], id))

    db.commit()
    return {"mensagem": "Atualizado!"}

# DELETAR
@usuarios_bp.delete("/<int:id>")
@token_required
@apenas_admin
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM usuarios WHERE id=?", (id,))
    db.commit()
    return {"mensagem": "Removido!"}
