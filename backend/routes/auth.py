from flask import Blueprint, request
from database import get_db
from utils.hash import gerar_hash, verificar_senha

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# CRIAR USUÁRIO
@auth_bp.post("/register")
def registrar():
    data = request.json
    db = get_db()

    senha_hash = gerar_hash(data["senha"])

    try:
        db.execute("""
            INSERT INTO usuarios (nome, email, senha_hash, nivel_acesso)
            VALUES (?, ?, ?, ?)
        """, (
            data["nome"],
            data["email"],
            senha_hash,
            data.get("nivel_acesso", "usuario")
        ))
        db.commit()
    except Exception as e:
        return {"erro": "Email já cadastrado ou erro ao criar usuário."}, 400

    return {"mensagem": "Usuário registrado com sucesso!"}, 201


# LOGIN
@auth_bp.post("/login")
def login():
    data = request.json
    db = get_db()

    row = db.execute("SELECT * FROM usuarios WHERE email = ?", (data["email"],)).fetchone()

    if not row:
        return {"erro": "Usuário não encontrado!"}, 404

    if not verificar_senha(data["senha"], row["senha_hash"]):
        return {"erro": "Senha incorreta!"}, 401

    # Criar um token simples (não para produção)
    token = gerar_hash(row["email"] + row["senha_hash"])

    return {
        "mensagem": "Login bem-sucedido!",
        "token": token,
        "usuario": {
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "nivel_acesso": row["nivel_acesso"]
        }
    }
