from flask import Blueprint, request
from database import get_db

cpus_bp = Blueprint("cpus", __name__, url_prefix="/cpus")

# LISTAR TODAS AS CPUs
@cpus_bp.get("/")
def listar_todas():
    db = get_db()
    rows = db.execute("SELECT * FROM cpus").fetchall()
    return [dict(row) for row in rows]

# BUSCAR CPU POR ID
@cpus_bp.get("/<int:id>")
def buscar(id):
    db = get_db()
    row = db.execute("SELECT * FROM cpus WHERE id = ?", (id,)).fetchone()
    if row:
        return dict(row)
    return {"erro": "CPU não encontrada"}, 404

# CRIAR CPU NOVA
@cpus_bp.post("/")
def criar():
    data = request.json
    db = get_db()

    db.execute("""
        INSERT INTO cpus (cpu_patrimonio, hostname, setor, impressora, ip, local)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["cpu_patrimonio"],
        data["hostname"],
        data["setor"],
        data["impressora"],
        data["ip"],
        data["local"]
    ))

    db.commit()

    return {"mensagem": "CPU cadastrada com sucesso!"}, 201

# ATUALIZAR CPU
@cpus_bp.put("/<int:id>")
def atualizar(id):
    data = request.json
    db = get_db()

    db.execute("""
        UPDATE cpus
        SET cpu_patrimonio = ?, hostname = ?, setor = ?, impressora = ?, ip = ?, local = ?
        WHERE id = ?
    """, (
        data["cpu_patrimonio"],
        data["hostname"],
        data["setor"],
        data["impressora"],
        data["ip"],
        data["local"],
        id
    ))

    db.commit()

    return {"mensagem": "CPU atualizada com sucesso!"}

# DELETAR CPU
@cpus_bp.delete("/<int:id>")
def deletar(id):
    db = get_db()
    db.execute("DELETE FROM cpus WHERE id = ?", (id,))
    db.commit()
    return {"mensagem": "CPU removida com sucesso!"}
