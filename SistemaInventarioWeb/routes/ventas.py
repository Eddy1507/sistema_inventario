from flask import Blueprint, render_template, request, jsonify

from models.database import (
    db,
    Cliente,
    Producto,
    Venta,
    DetalleVenta,
    MovimientoInventario,
    Empresa

)


ventas_bp = Blueprint("ventas", __name__)


# ==========================
# NUEVA VENTA
# ==========================

@ventas_bp.route("/ventas")
def ventas():

    clientes = Cliente.query.all()

    productos = Producto.query.all()

    historial = Venta.query.order_by(
        Venta.fecha.desc()
    ).all()


    return render_template(
        "ventas.html",
        clientes=clientes,
        productos=productos,
        historial=historial
    )



# ==========================
# GUARDAR VENTA
# ==========================

@ventas_bp.route("/ventas/guardar", methods=["POST"])
def guardar_venta():

    datos = request.get_json()


    cliente_id = datos["cliente"]

    carrito = datos["carrito"]


    if len(carrito) == 0:

        return jsonify({
            "ok": False,
            "error": "El carrito está vacío."
        })


    total = 0


    # Validar productos y stock

    for item in carrito:

        producto = Producto.query.get(item["id"])


        if producto is None:

            return jsonify({
                "ok": False,
                "error": "Producto no encontrado."
            })


        if item["cantidad"] > producto.stock:

            return jsonify({
                "ok": False,
                "error": f"No hay suficiente stock de {producto.nombre}"
            })


        total += item["subtotal"]



    # Crear venta

    venta = Venta(

        cliente_id=cliente_id,

        total=total

    )


    db.session.add(venta)

    db.session.commit()



    # Crear detalles + Kardex

    for item in carrito:


        producto = Producto.query.get(item["id"])



        detalle = DetalleVenta(

            venta_id=venta.id,

            producto_id=producto.id,

            cantidad=item["cantidad"],

            precio=item["precio"],

            subtotal=item["subtotal"]

        )


        db.session.add(detalle)



        # Guardar movimiento Kardex

        stock_anterior = producto.stock


        producto.stock -= item["cantidad"]



        movimiento = MovimientoInventario(

            producto_id=producto.id,

            tipo="Salida",

            cantidad=item["cantidad"],

            stock_anterior=stock_anterior,

            stock_nuevo=producto.stock,

            referencia=f"Venta #{venta.id}"

        )


        db.session.add(movimiento)



    db.session.commit()



    return jsonify({
        "ok": True
    })




# ==========================
# DETALLE DE VENTA
# ==========================

@ventas_bp.route("/ventas/detalle/<int:id>")
def detalle_venta(id):

    venta = Venta.query.get_or_404(id)


    return render_template(
        "detalle_venta.html",
        venta=venta
    )

# ==========================
# TICKET DE VENTA
# ==========================

@ventas_bp.route("/ventas/ticket/<int:id>")
def ticket_venta(id):

    venta = Venta.query.get_or_404(id)

    empresa = Empresa.query.first()


    return render_template(

        "ticket_venta.html",

        venta=venta,

        empresa=empresa

    )
