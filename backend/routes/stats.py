from flask import Blueprint
from database import get_db
from utils.auth_middleware import token_required

stats_bp = Blueprint("stats", __name__, url_prefix="/stats")

@stats_bp.get("/totais")
@token_required
def totais():
    db = get_db()

    dispositivos = db.execute("SELECT COUNT(*) AS total FROM dispositivos_moveis").fetchone()["total"]
    racks = db.execute("SELECT COUNT(*) AS total FROM racks").fetchone()["total"]
    impressoras = db.execute("SELECT COUNT(*) AS total FROM impressoras").fetchone()["total"]
    cpus = db.execute("SELECT COUNT(*) AS total FROM cpus").fetchone()["total"]
    itens_cpu = db.execute("SELECT COUNT(*) AS total FROM cpu_itens").fetchone()["total"]

    return {
        "dispositivos": dispositivos,
        "racks": racks,
        "impressoras": impressoras,
        "cpus": cpus,
        "itens_cpu": itens_cpu
    }
