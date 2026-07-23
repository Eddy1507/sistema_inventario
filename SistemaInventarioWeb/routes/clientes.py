from flask import Blueprint, render_template, request, redirect
from models.database import db, Cliente

clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.route("/clientes")
def clientes():

    lista = Cliente.query.all()

    return render_template(
        "clientes.html",
        clientes=lista
    )


@clientes_bp.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    if request.method == "POST":

        cliente = Cliente(
            nombre=request.form["nombre"],
            telefono=request.form["telefono"],
            correo=request.form["correo"]
        )

        db.session.add(cliente)
        db.session.commit()

        return redirect("/clientes")

    return render_template("cliente_form.html")


@clientes_bp.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    if request.method == "POST":

        cliente.nombre = request.form["nombre"]
        cliente.telefono = request.form["telefono"]
        cliente.correo = request.form["correo"]

        db.session.commit()

        return redirect("/clientes")

    return render_template(
        "cliente_form.html",
        cliente=cliente
    )


@clientes_bp.route("/clientes/eliminar/<int:id>")
def eliminar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)

    db.session.commit()

    return redirect("/clientes")
