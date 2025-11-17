from flask import Flask
from flask_cors import CORS
# imports das blueprints...
from routes.dispositivos_moveis import dispositivos_bp
from routes.racks import racks_bp
from routes.impressoras import impressoras_bp
from routes.cpus import cpus_bp
from routes.cpu_itens import cpu_itens_bp
from routes.auth import auth_bp
from routes.usuarios import usuarios_bp  # se existir

app = Flask(__name__)

# 1) Habilita CORS (em dev: origens abertas)
CORS(app, resources={r"/*": {"origins": "*"}})

# 2) Evita redirect automático por slash (resolve o erro de preflight)
app.url_map.strict_slashes = False

# Registrar blueprints
app.register_blueprint(dispositivos_bp)
app.register_blueprint(racks_bp)
app.register_blueprint(impressoras_bp)
app.register_blueprint(cpus_bp)
app.register_blueprint(cpu_itens_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)  

@app.route("/")
def home():
    return {"status": "API do Inventário funcionando!"}

if __name__ == "__main__":
    print("Iniciando servidor Flask...")
    app.run(debug=True)
