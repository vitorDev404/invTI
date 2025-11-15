from functools import wraps
from flask import request, jsonify
from database import get_db
from utils.hash import gerar_hash

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"erro": "Token não fornecido"}), 401

        try:
            token = auth_header.split(" ")[1]
        except:
            return jsonify({"erro": "Formato de token inválido. Use 'Bearer <token>'"}), 401

        db = get_db()
        usuarios = db.execute("SELECT * FROM usuarios").fetchall()

        usuario_encontrado = None

        for usuario in usuarios:
            token_gerado = gerar_hash(usuario["email"] + usuario["senha_hash"])
            if token == token_gerado:
                usuario_encontrado = usuario
                break

        if not usuario_encontrado:
            return jsonify({"erro": "Token inválido"}), 401

        request.usuario = usuario_encontrado

        return f(*args, **kwargs)

    return decorated


def apenas_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        usuario = request.usuario

        if usuario["nivel_acesso"] != "admin":
            return jsonify({"erro": "Acesso restrito: apenas administradores podem realizar esta ação."}), 403

        return f(*args, **kwargs)

    return decorated
