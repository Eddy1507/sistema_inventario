from flask import Blueprint, render_template, request, jsonify

from models.database import (
    db,
    Producto,
    Proveedor,
    Compra,
    DetalleCompra,
    MovimientoInventario
)


compras_bp = Blueprint("compras", __name__)


# =====================================
# VENTANA DE COMPRAS
# =====================================

@compras_bp.route("/compras")
def compras():

    proveedores = Proveedor.query.all()

    productos = Producto.query.all()

    historial = Compra.query.order_by(
        Compra.fecha.desc()
    ).all()


    return render_template(
        "compras.html",
        proveedores=proveedores,
        productos=productos,
        historial=historial
    )



# =====================================
# GUARDAR COMPRA
# =====================================

@compras_bp.route("/compras/guardar", methods=["POST"])
def guardar_compra():

    try:

        datos = request.get_json()


        proveedor_id = datos["proveedor"]

        carrito = datos["carrito"]



        if len(carrito) == 0:

            return jsonify({

                "ok": False,

                "error": "El carrito está vacío."

            })



        total = 0



        # Validar productos

        for item in carrito:


            producto = Producto.query.get(item["id"])



            if producto is None:

                return jsonify({

                    "ok": False,

                    "error": "Producto no encontrado."

                })



            total += item["subtotal"]




        # Crear compra

        compra = Compra(

            proveedor_id=proveedor_id,

            total=total

        )


        db.session.add(compra)

        db.session.commit()




        # Crear detalle + Kardex

        for item in carrito:


            producto = Producto.query.get(item["id"])



            detalle = DetalleCompra(

                compra_id=compra.id,

                producto_id=producto.id,

                cantidad=item["cantidad"],

                costo=item["costo"],

                subtotal=item["subtotal"]

            )


            db.session.add(detalle)




            # Movimiento Kardex

            stock_anterior = producto.stock



            producto.stock += item["cantidad"]

            # Actualizar costo del producto
            producto.costo = item["costo"]




            movimiento = MovimientoInventario(

                producto_id=producto.id,

                tipo="Entrada",

                cantidad=item["cantidad"],

                stock_anterior=stock_anterior,

                stock_nuevo=producto.stock,

                referencia=f"Compra #{compra.id}"

            )


            db.session.add(movimiento)




        db.session.commit()



        return jsonify({

            "ok": True

        })



    except Exception as e:


        db.session.rollback()


        return jsonify({

            "ok": False,

            "error": str(e)

        })




# =====================================
# DETALLE DE COMPRA
# =====================================

@compras_bp.route("/compras/detalle/<int:id>")
def detalle_compra(id):

    compra = Compra.query.get_or_404(id)


    return render_template(

        "detalle_compra.html",

        compra=compra

    )

