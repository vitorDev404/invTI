import hashlib

def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha, senha_hash):
    return gerar_hash(senha) == senha_hash
