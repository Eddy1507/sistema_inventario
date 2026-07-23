// =====================================
// VARIABLES
// =====================================

let carrito = [];
let total = 0;


// =====================================
// SELECT2
// =====================================

$(document).ready(function () {

    $("#producto").select2({

        placeholder: "Buscar producto...",

        width: "100%"

    });

});


// =====================================
// BOTÓN AGREGAR
// =====================================

document
.getElementById("btnAgregar")
.addEventListener("click", agregarProducto);


// =====================================
// AGREGAR PRODUCTO
// =====================================

function agregarProducto() {

    const producto = document.getElementById("producto");
    const costo = document.getElementById("costo");
    const cantidad = document.getElementById("cantidad");

    const opcion = producto.options[producto.selectedIndex];

    if (!opcion) {

        alert("Seleccione un producto.");

        return;

    }

    const id = opcion.value;

    const texto = opcion.text;

    const partes = texto.split("-");

    const codigo = partes.shift().trim();

    const nombre = partes.join("-").trim();

    const costoNum = parseFloat(costo.value);

    const cantidadNum = parseInt(cantidad.value);

    if (isNaN(costoNum) || costoNum <= 0) {

        alert("Ingrese un costo válido.");

        return;

    }

    if (isNaN(cantidadNum) || cantidadNum <= 0) {

        alert("Ingrese una cantidad válida.");

        return;

    }

    const existente = carrito.find(x => x.id == id);

    if (existente) {

        existente.cantidad += cantidadNum;

        existente.costo = costoNum;

        existente.subtotal =
            existente.cantidad *
            existente.costo;

    } else {

        carrito.push({

            id: id,

            codigo: codigo,

            nombre: nombre,

            costo: costoNum,

            cantidad: cantidadNum,

            subtotal: costoNum * cantidadNum

        });

    }

    dibujarCarrito();

    costo.value = "";

    cantidad.value = 1;

    $("#producto").val(null).trigger("change");

}


// =====================================
// DIBUJAR CARRITO
// =====================================

function dibujarCarrito() {

    const tbody = document.querySelector("#tablaCarrito tbody");

    tbody.innerHTML = "";

    total = 0;

    carrito.forEach((item, index) => {

        total += item.subtotal;

        tbody.innerHTML += `

        <tr>

            <td>${item.codigo}</td>

            <td>${item.nombre}</td>

            <td>$${item.costo.toFixed(2)}</td>

            <td>

                <div class="btn-group">

                    <button
                        class="btn btn-outline-danger btn-sm"
                        onclick="disminuirCantidad(${index})">

                        -

                    </button>

                    <button
                        class="btn btn-light btn-sm"
                        disabled>

                        ${item.cantidad}

                    </button>

                    <button
                        class="btn btn-outline-success btn-sm"
                        onclick="aumentarCantidad(${index})">

                        +

                    </button>

                </div>

            </td>

            <td>

                $${item.subtotal.toFixed(2)}

            </td>

            <td>

                <button
                    class="btn btn-danger btn-sm"
                    onclick="eliminarProducto(${index})">

                    <i class="bi bi-trash"></i>

                </button>

            </td>

        </tr>

        `;

    });

    document.getElementById("totalCompra").innerHTML =
        "$" + total.toFixed(2);

}


// =====================================
// ELIMINAR PRODUCTO
// =====================================

function eliminarProducto(indice) {

    carrito.splice(indice, 1);

    dibujarCarrito();

}


// =====================================
// AUMENTAR CANTIDAD
// =====================================

function aumentarCantidad(indice) {

    carrito[indice].cantidad++;

    carrito[indice].subtotal =
        carrito[indice].cantidad *
        carrito[indice].costo;

    dibujarCarrito();

}


// =====================================
// DISMINUIR CANTIDAD
// =====================================

function disminuirCantidad(indice) {

    carrito[indice].cantidad--;

    if (carrito[indice].cantidad <= 0) {

        carrito.splice(indice, 1);

    } else {

        carrito[indice].subtotal =
            carrito[indice].cantidad *
            carrito[indice].costo;

    }

    dibujarCarrito();

}


// =====================================
// GUARDAR COMPRA
// =====================================

document
.getElementById("btnGuardarCompra")
.addEventListener("click", guardarCompra);


function guardarCompra() {

    if (carrito.length === 0) {

        alert("El carrito está vacío.");

        return;

    }

    const proveedor = document.querySelector(
        "select[name='proveedor']"
    ).value;

    fetch("/compras/guardar", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            proveedor: proveedor,

            carrito: carrito

        })

    })

    .then(res => res.json())

    .then(data => {

        if (data.ok) {

            alert("Compra guardada correctamente.");

            window.location.href = "/compras";

        } else {

            alert(data.error);

        }

    })

    .catch(error => {

        console.error(error);

        alert("Ocurrió un error al guardar la compra.");

    });

}
