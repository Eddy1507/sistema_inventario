from flask import Blueprint, render_template
from sqlalchemy import func

from models.database import (
    db,
    Producto,
    Cliente,
    Proveedor,
    Venta,
    Compra
)


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():


    # ==========================
    # CONTADORES
    # ==========================

    total_productos = Producto.query.count()

    total_clientes = Cliente.query.count()

    total_proveedores = Proveedor.query.count()

    total_ventas = Venta.query.count()

    total_compras = Compra.query.count()



    # ==========================
    # INVENTARIO
    # ==========================

    inventario_total = db.session.query(
        func.sum(Producto.stock)
    ).scalar() or 0



    valor_inventario = sum(
        producto.precio * producto.stock
        for producto in Producto.query.all()
    )



    # ==========================
    # STOCK BAJO
    # ==========================

    productos_stock_bajo = Producto.query.filter(
        Producto.stock <= 10
    ).order_by(
        Producto.stock.asc()
    ).all()



    productos_bajo_cantidad = Producto.query.filter(
        Producto.stock <= 10
    ).count()



    # ==========================
    # TOTALES DINERO
    # ==========================

    dinero_ventas = db.session.query(
        func.sum(Venta.total)
    ).scalar() or 0



    dinero_compras = db.session.query(
        func.sum(Compra.total)
    ).scalar() or 0




    # ==========================
    # ÚLTIMAS VENTAS
    # ==========================

    ultimas_ventas = Venta.query.order_by(
        Venta.fecha.desc()
    ).limit(5).all()



    # ==========================
    # ÚLTIMAS COMPRAS
    # ==========================

    ultimas_compras = Compra.query.order_by(
        Compra.fecha.desc()
    ).limit(5).all()



    return render_template(

        "dashboard.html",


        total_productos=total_productos,

        total_clientes=total_clientes,

        total_proveedores=total_proveedores,

        total_ventas=total_ventas,

        total_compras=total_compras,


        inventario_total=inventario_total,

        valor_inventario=valor_inventario,


        productos_stock_bajo=productos_stock_bajo,

        productos_bajo_cantidad=productos_bajo_cantidad,


        dinero_ventas=dinero_ventas,

        dinero_compras=dinero_compras,


        ultimas_ventas=ultimas_ventas,

        ultimas_compras=ultimas_compras,



        # Datos para gráficas

        ventas=total_ventas,

        compras=total_compras,

        productos=total_productos,

        clientes=total_clientes

    )
