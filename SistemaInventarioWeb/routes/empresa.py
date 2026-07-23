from flask import Blueprint, render_template, request, redirect, url_for
from models.database import db, Empresa

empresa_bp = Blueprint("empresa", __name__)


@empresa_bp.route("/empresa", methods=["GET", "POST"])
def empresa():

    empresa = Empresa.query.first()

    if empresa is None:

        empresa = Empresa(
            nombre="EMYE CUU",
            logo="img/logo.png"
        )

        db.session.add(empresa)
        db.session.commit()


    if request.method == "POST":

        empresa.nombre = request.form["nombre"]

        empresa.direccion = request.form["direccion"]

        empresa.telefono = request.form["telefono"]

        empresa.correo = request.form["correo"]

        empresa.rfc = request.form["rfc"]

        empresa.sitio_web = request.form["sitio_web"]


        # Solo asigna logo si todavía no existe
        if not empresa.logo:

            empresa.logo = "img/logo.png"


        db.session.commit()


        return redirect(
            url_for("empresa.empresa")
        )


    return render_template(
        "empresa.html",
        empresa=empresa
    )
