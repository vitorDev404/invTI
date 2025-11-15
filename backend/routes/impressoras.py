from flask import Blueprint, request
from database import get_db
from utils.auth_middleware import token_required, apenas_admin

impressoras_bp = Blueprint("impressoras", __name__, url_prefix="/impressoras")

# LISTAR TODAS (QUALQUER USUÁRIO LOGADO)
@impressoras_bp.get("/")
@token_required
def listar_todas():
    db = get_db()
    rows = db.execute("SELECT * FROM impressoras").fetchall()
    return [dict(row) for row in rows]

# BUSCAR POR ID
@impressoras_bp.get("/<int:id>")
@token_required
def buscar(id):
    db = get_db()
    row = db.execute("SELECT * FROM impressoras WHERE id = ?", (id,)).fetchone()
    if row:
        return dict(row)
    return {"erro": "Impressora não encontrada"}, 404

# CRIAR NOVA (APENAS ADMIN)
@impressoras_bp.post("/")
@token_required
@apenas_admin
def criar():
    data = request.json
    db = get_db()

    db.execute("""
        INSERT INTO impressoras 
        (modelo, unidade, local, numero_serie, ip_equipamento, nome_impressora_servidor, ndd, mac, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["modelo"],
        data["unidade"],
        data["local"],
        data["numero_serie"],
        data["ip_equipamento"],
        data["nome_impressora_servidor"],
        data["ndd"],
        data["mac"],
        data.get("observacoes", "")
    ))

    db.commit()
    return {"mensagem": "Impressora cadastrada com sucesso!"}, 201

# ATUALIZAR (APENAS ADMIN)
@impressoras_bp.put("/<int:id>")
@token_required
@apenas_admin
def atualizar(id):
    data = request.json
    db = get_db()

    db.execute("""
        UPDATE impressoras
        SET modelo = ?, unidade = ?, local = ?, numero_serie = ?, ip_equipamento = ?, 
            nome_impressora_servidor = ?, ndd = ?, mac = ?, observacoes = ?
        WHERE id = ?
    """, (
        data["modelo"],
        data["unidade"],
        data["local"],
        data["numero_serie"],
        data["ip_equipamento"],
        data["nome_impressora_servidor"],
        data["ndd"],
        data["mac"],
        data.get("observacoes", ""),
        id
    ))

    db.commit()
    return {"mensagem": "Impressora atualizada com sucesso!"}

# DELETAR (APENAS ADMIN)
@impressoras_bp.delete("/<int:id>")
@token_required
@apenas_admin
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM impressoras WHERE id = ?", (id,))
    db.commit()
    return {"mensagem": "Impressora removida com sucesso!"}
