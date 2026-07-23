from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


# ==========================
# PRODUCTOS
# ==========================

class Producto(db.Model):

    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    categoria = db.Column(
        db.String(80)
    )

    precio = db.Column(
        db.Float,
        nullable=False
    )

    costo = db.Column(
        db.Float,
        default=0
    )

    stock = db.Column(
        db.Integer,
        default=0
    )

# ==========================
# CLIENTES
# ==========================

class Cliente(db.Model):

    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    telefono = db.Column(db.String(20))

    correo = db.Column(db.String(100))


# ==========================
# PROVEEDORES
# ==========================

class Proveedor(db.Model):

    __tablename__ = "proveedores"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    telefono = db.Column(db.String(20))

    correo = db.Column(db.String(100))


# ==========================
# VENTAS
# ==========================

from datetime import datetime

class Venta(db.Model):

    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.DateTime, default=datetime.now) 

    total = db.Column(db.Float)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id")
    )

    cliente = db.relationship(
        "Cliente",
        backref="ventas"
    )
    



# ==========================
# DETALLE DE VENTAS
# ==========================

class DetalleVenta(db.Model):

    __tablename__ = "detalle_ventas"

    id = db.Column(db.Integer, primary_key=True)

    venta_id = db.Column(
        db.Integer,
        db.ForeignKey("ventas.id")
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id")
    )

    cantidad = db.Column(db.Integer)

    precio = db.Column(db.Float)

    subtotal = db.Column(db.Float)

    venta = db.relationship(
        "Venta",
        backref="detalles"
    )

    producto = db.relationship("Producto")

    # ==========================
# COMPRAS
# ==========================

class Compra(db.Model):

    __tablename__ = "compras"

    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(
        db.DateTime,
        default=datetime.now
    )

    total = db.Column(db.Float, default=0)

    proveedor_id = db.Column(
        db.Integer,
        db.ForeignKey("proveedores.id")
    )

    proveedor = db.relationship(
        "Proveedor",
        backref="compras"
    )


# ==========================
# DETALLE DE COMPRAS
# ==========================

class DetalleCompra(db.Model):

    __tablename__ = "detalle_compras"

    id = db.Column(db.Integer, primary_key=True)

    compra_id = db.Column(
        db.Integer,
        db.ForeignKey("compras.id")
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id")
    )

    cantidad = db.Column(db.Integer)

    costo = db.Column(db.Float)

    subtotal = db.Column(db.Float)

    compra = db.relationship(
        "Compra",
        backref="detalles"
    )

    producto = db.relationship(
        "Producto"
    )

class MovimientoInventario(db.Model):

    __tablename__ = "movimientos"

    id = db.Column(db.Integer, primary_key=True)

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id"),
        nullable=False
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    tipo = db.Column(db.String(20), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)

    stock_anterior = db.Column(db.Integer, nullable=False)

    stock_nuevo = db.Column(db.Integer, nullable=False)

    referencia = db.Column(db.String(100))

    producto = db.relationship(
        "Producto",
        backref="movimientos"
    )


class Empresa(db.Model):

    __tablename__ = "empresa"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(150), nullable=False)

    direccion = db.Column(db.String(250))

    telefono = db.Column(db.String(30))

    correo = db.Column(db.String(120))

    rfc = db.Column(db.String(30))

    sitio_web = db.Column(db.String(120))

    logo = db.Column(db.String(200))

    