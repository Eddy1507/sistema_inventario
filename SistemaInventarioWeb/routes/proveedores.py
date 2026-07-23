from flask import Blueprint, render_template, request, redirect
from models.database import db, Proveedor

proveedores_bp = Blueprint("proveedores", __name__)

@proveedores_bp.route("/proveedores")
def proveedores():

    lista = Proveedor.query.all()

    return render_template(
        "proveedores.html",
        proveedores=lista
    )


@proveedores_bp.route("/proveedores/nuevo", methods=["GET","POST"])
def nuevo_proveedor():

    if request.method == "POST":

        proveedor = Proveedor(
            nombre=request.form["nombre"],
            telefono=request.form["telefono"],
            correo=request.form["correo"]
        )

        db.session.add(proveedor)
        db.session.commit()

        return redirect("/proveedores")

    return render_template("proveedor_form.html")


@proveedores_bp.route("/proveedores/editar/<int:id>", methods=["GET","POST"])
def editar_proveedor(id):

    proveedor = Proveedor.query.get_or_404(id)

    if request.method == "POST":

        proveedor.nombre = request.form["nombre"]
        proveedor.telefono = request.form["telefono"]
        proveedor.correo = request.form["correo"]

        db.session.commit()

        return redirect("/proveedores")

    return render_template(
        "proveedor_form.html",
        proveedor=proveedor
    )


@proveedores_bp.route("/proveedores/eliminar/<int:id>")
def eliminar_proveedor(id):

    proveedor = Proveedor.query.get_or_404(id)

    db.session.delete(proveedor)
    db.session.commit()

    return redirect("/proveedores")

