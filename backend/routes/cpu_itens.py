from flask import Blueprint, request
from database import get_db

cpu_itens_bp = Blueprint("cpu_itens", __name__, url_prefix="/cpu_itens")

# LISTAR TODOS OS ITENS DE UMA CPU
@cpu_itens_bp.get("/cpu/<int:cpu_id>")
def listar_por_cpu(cpu_id):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM cpu_itens WHERE cpu_id = ?", 
        (cpu_id,)
    ).fetchall()
    return [dict(row) for row in rows]


# BUSCAR UM ITEM ESPECÍFICO
@cpu_itens_bp.get("/<int:id>")
def buscar(id):
    db = get_db()
    row = db.execute("SELECT * FROM cpu_itens WHERE id = ?", (id,)).fetchone()
    if row:
        return dict(row)
    return {"erro": "Item não encontrado"}, 404


# ADICIONAR ITEM VINCULADO À CPU
@cpu_itens_bp.post("/")
def criar():
    data = request.json
    db = get_db()

    db.execute("""
        INSERT INTO cpu_itens (cpu_id, tipo, patrimonio, descricao)
        VALUES (?, ?, ?, ?)
    """, (
        data["cpu_id"],
        data["tipo"],
        data["patrimonio"],
        data.get("descricao", "")
    ))

    db.commit()
    return {"mensagem": "Item vinculado com sucesso!"}, 201


# ATUALIZAR ITEM
@cpu_itens_bp.put("/<int:id>")
def atualizar(id):
    data = request.json
    db = get_db()

    db.execute("""
        UPDATE cpu_itens
        SET tipo = ?, patrimonio = ?, descricao = ?
        WHERE id = ?
    """, (
        data["tipo"],
        data["patrimonio"],
        data.get("descricao", ""),
        id
    ))

    db.commit()
    return {"mensagem": "Item atualizado com sucesso!"}


# REMOVER ITEM VINCULADO
@cpu_itens_bp.delete("/<int:id>")
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM cpu_itens WHERE id = ?", (id,))
    db.commit()
    
    return {"mensagem": "Item removido com sucesso!"}
