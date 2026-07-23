import os
import shutil

from datetime import datetime

from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    render_template,
    request
)


respaldo_bp = Blueprint("respaldo", __name__)



# ==========================
# CREAR RESPALDO
# ==========================

@respaldo_bp.route("/respaldo")
def crear_respaldo():

    try:

        origen = "instance/database.db"


        if not os.path.exists(origen):

            flash(
                "No se encontró la base de datos.",
                "danger"
            )

            return redirect(
                url_for("dashboard.dashboard")
            )



        carpeta = "backups"


        if not os.path.exists(carpeta):

            os.makedirs(carpeta)



        fecha = datetime.now().strftime(
            "%d-%m-%Y_%H-%M"
        )


        destino = os.path.join(

            carpeta,

            f"backup_{fecha}.db"

        )


        shutil.copy2(
            origen,
            destino
        )


        flash(
            "Respaldo creado correctamente.",
            "success"
        )


    except Exception as e:


        flash(
            f"Error al crear respaldo: {e}",
            "danger"
        )



    return redirect(
        url_for("dashboard.dashboard")
    )




# ==========================
# PAGINA RESTAURAR
# ==========================

@respaldo_bp.route("/restaurar")
def restaurar():

    carpeta = "backups"


    if not os.path.exists(carpeta):

        os.makedirs(carpeta)



    archivos = []


    for archivo in os.listdir(carpeta):

        if archivo.endswith(".db"):

            ruta = os.path.join(carpeta, archivo)

            fecha = os.path.getmtime(ruta)

            archivos.append({

                "nombre": archivo,

                "fecha": datetime.fromtimestamp(fecha)

            })



    archivos = sorted(
        archivos,
        key=lambda x: x["fecha"],
        reverse=True
    )



    return render_template(
        "restaurar.html",
        archivos=archivos
    )




# ==========================
# PROCESAR RESTAURACION
# ==========================

@respaldo_bp.route("/restaurar/ejecutar", methods=["POST"])
def ejecutar_restaurar():

    try:


        archivo = request.form["archivo"]



        origen = os.path.join(
            "backups",
            archivo
        )



        destino = "instance/database.db"



        if not os.path.exists(origen):

            flash(
                "El archivo de respaldo no existe.",
                "danger"
            )

            return redirect(
                url_for("respaldo.restaurar")
            )



        shutil.copy2(

            origen,

            destino

        )



        flash(

            "Base de datos restaurada correctamente. Reinicia el sistema.",

            "success"

        )



    except Exception as e:


        flash(

            f"Error al restaurar: {e}",

            "danger"

        )



    return redirect(
        url_for("respaldo.restaurar")
    )

