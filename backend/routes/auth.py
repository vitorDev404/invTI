from flask import Blueprint, request, jsonify
from database import get_db
from utils.hash import gerar_hash, verificar_senha
from utils.auth_middleware import token_required, apenas_admin

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ==============================
# 1) REGISTRAR USUÁRIO (ADMIN)
# ==============================
@auth_bp.post("/register")
@token_required
@apenas_admin
def registrar():
    data = request.json
    db = get_db()

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    nivel = data.get("nivel_acesso", "usuario")

    if not nome or not email or not senha:
        return {"erro": "Nome, email e senha são obrigatórios."}, 400

    senha_hash = gerar_hash(senha)

    try:
        db.execute("""
            INSERT INTO usuarios (nome, email, senha_hash, nivel_acesso)
            VALUES (?, ?, ?, ?)
        """, (nome, email, senha_hash, nivel))
        db.commit()
    except Exception as e:
        return {"erro": f"Erro ao criar usuário: {str(e)}"}, 400

    return {"mensagem": "Usuário registrado com sucesso!"}, 201


# ==============================
# 2) LOGIN (GERA TOKEN)
# ==============================
@auth_bp.post("/login")
def login():
    data = request.json
    db = get_db()

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return {"erro": "Email e senha são obrigatórios."}, 400

    row = db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()

    if not row:
        return {"erro": "Usuário não encontrado!"}, 404

    if not verificar_senha(senha, row["senha_hash"]):
        return {"erro": "Senha incorreta!"}, 401

    # Token = hash(email + senha_hash)
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


# ==============================
# 3) LISTAR USUÁRIOS (APENAS ADMIN)
# ==============================
@auth_bp.get("/usuarios")
@token_required
@apenas_admin
def listar_usuarios():
    db = get_db()
    rows = db.execute("SELECT id, nome, email, nivel_acesso FROM usuarios").fetchall()
    return [dict(row) for row in rows]


# ==============================
# 4) EDITAR USUÁRIO (APENAS ADMIN)
# ==============================
@auth_bp.put("/usuarios/<int:id>")
@token_required
@apenas_admin
def editar_usuario(id):
    data = request.json
    db = get_db()

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")  # opcional
    nivel = data.get("nivel_acesso")

    if not nome or not email:
        return {"erro": "Nome e email são obrigatórios."}, 400

    # Atualiza sem alterar a senha
    if not senha:
        db.execute("""
            UPDATE usuarios
            SET nome = ?, email = ?, nivel_acesso = ?
            WHERE id = ?
        """, (nome, email, nivel, id))

    else:
        senha_hash = gerar_hash(senha)
        db.execute("""
            UPDATE usuarios
            SET nome = ?, email = ?, senha_hash = ?, nivel_acesso = ?
            WHERE id = ?
        """, (nome, email, senha_hash, nivel, id))

    db.commit()

    return {"mensagem": "Usuário atualizado com sucesso!"}


# ==============================
# 5) DELETAR USUÁRIO (APENAS ADMIN)
# ==============================
@auth_bp.delete("/usuarios/<int:id>")
@token_required
@apenas_admin
def deletar_usuario(id):
    db = get_db()
    db.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    db.commit()
    return {"mensagem": "Usuário removido com sucesso!"}
@auth_bp.post("/reset_senha/<int:id>")
@token_required
@apenas_admin
def reset_senha(id):
    db = get_db()
    nova = gerar_hash("123456")  # senha padrão

    db.execute("UPDATE usuarios SET senha_hash = ? WHERE id = ?", (nova, id))
    db.commit()

    return {"mensagem": "Senha redefinida para '123456'!"}
