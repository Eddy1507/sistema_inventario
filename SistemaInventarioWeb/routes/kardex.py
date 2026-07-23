from flask import Blueprint, render_template
from models.database import MovimientoInventario


kardex_bp = Blueprint("kardex", __name__)


# ==========================
# KARDEX
# ==========================

@kardex_bp.route("/kardex")
def kardex():

    movimientos = MovimientoInventario.query.order_by(
        MovimientoInventario.fecha.desc()
    ).all()


    return render_template(
        "kardex.html",
        movimientos=movimientos
    )

