from flask import Blueprint, render_template, request, redirect, url_for
from models.database import db, Producto

productos_bp = Blueprint("productos", __name__)


@productos_bp.route("/productos")
def listar():

    productos = Producto.query.all()

    return render_template(
        "productos.html",
        productos=productos
    )


@productos_bp.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo():

    if request.method == "POST":

        producto = Producto(

            codigo=request.form["codigo"],

            nombre=request.form["nombre"],

            categoria=request.form["categoria"],

            costo=float(request.form["costo"]),

            precio=float(request.form["precio"]),

            stock=int(request.form["stock"])

        )

        db.session.add(producto)

        db.session.commit()

        return redirect(url_for("productos.listar"))

    return render_template("nuevo_producto.html")


@productos_bp.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    producto = Producto.query.get_or_404(id)

    if request.method == "POST":

        producto.codigo = request.form["codigo"]

        producto.nombre = request.form["nombre"]

        producto.categoria = request.form["categoria"]

        producto.costo = float(request.form["costo"])

        producto.precio = float(request.form["precio"])

        producto.stock = int(request.form["stock"])

        db.session.commit()

        return redirect(url_for("productos.listar"))

    return render_template(
        "editar_producto.html",
        producto=producto
    )


@productos_bp.route("/productos/eliminar/<int:id>")
def eliminar(id):

    producto = Producto.query.get_or_404(id)

    db.session.delete(producto)

    db.session.commit()

    return redirect(url_for("productos.listar"))
