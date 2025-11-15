from flask import Flask
from flask_cors import CORS

from routes.dispositivos_moveis import dispositivos_bp
from routes.racks import racks_bp
from routes.impressoras import impressoras_bp
from routes.cpus import cpus_bp
from routes.cpu_itens import cpu_itens_bp
from routes.auth import auth_bp

app = Flask(__name__)

# CORS COMPLETO
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

app.register_blueprint(dispositivos_bp)
app.register_blueprint(racks_bp)
app.register_blueprint(impressoras_bp)
app.register_blueprint(cpus_bp)
app.register_blueprint(cpu_itens_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return {"status": "API do Inventário funcionando!"}

if __name__ == "__main__":
    print("Iniciando servidor Flask...")
    app.run(debug=True)
