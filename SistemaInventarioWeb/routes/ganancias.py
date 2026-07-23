from flask import Blueprint, render_template
from models.database import Producto

ganancias_bp = Blueprint("ganancias", __name__)


@ganancias_bp.route("/ganancias")
def ganancias():

    productos = Producto.query.all()

    total_costo = 0
    total_venta = 0
    utilidad_total = 0

    for producto in productos:

        producto.utilidad = producto.precio - producto.costo

        producto.valor_stock = producto.stock * producto.precio

        producto.utilidad_stock = (
            producto.utilidad * producto.stock
        )

        total_costo += producto.costo * producto.stock

        total_venta += producto.precio * producto.stock

        utilidad_total += producto.utilidad_stock

    margen = 0

    if total_venta > 0:

        margen = (utilidad_total / total_venta) * 100

    labels = [producto.nombre for producto in productos]

    datos = [producto.utilidad for producto in productos]

    return render_template(

        "ganancias.html",

        productos=productos,

        total_costo=total_costo,

        total_venta=total_venta,

        utilidad_total=utilidad_total,

        margen=margen,

        labels=labels,

        datos=datos

    )