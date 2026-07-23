from flask import Flask

from models.database import db, Empresa

from routes.dashboard import dashboard_bp
from routes.productos import productos_bp
from routes.clientes import clientes_bp
from routes.proveedores import proveedores_bp
from routes.ventas import ventas_bp
from routes.compras import compras_bp
from routes.reportes import reportes_bp
from routes.kardex import kardex_bp
from routes.respaldo import respaldo_bp
from routes.ganancias import ganancias_bp
from routes.empresa import empresa_bp


app = Flask(__name__)


@app.context_processor
def datos_empresa():

    empresa = Empresa.query.first()

    return {
        "empresa": empresa
    }


app.config["SECRET_KEY"] = "inventario2026"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(dashboard_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint (proveedores_bp)
app.register_blueprint (ventas_bp)
app.register_blueprint(compras_bp)
app.register_blueprint(reportes_bp)
app.register_blueprint(kardex_bp)
app.register_blueprint(respaldo_bp)
app.register_blueprint(ganancias_bp)
app.register_blueprint(empresa_bp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)


    
