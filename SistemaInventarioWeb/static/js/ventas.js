$(document).ready(function () {

    $("#producto").select2({

        placeholder: "Buscar producto",

        width: "100%"

    });

});

let carrito = [];

let total = 0;

document
.getElementById("btnAgregar")
.addEventListener("click", agregarProducto);

function agregarProducto(){

    const producto=document.getElementById("producto");

    const cantidad=document.querySelector("input[name='cantidad']");

    const opcion=producto.options[producto.selectedIndex];

    const id=opcion.value;

    const texto=opcion.text;

    const stock=parseInt(opcion.dataset.stock);

    const precio=parseFloat(

        texto.substring(

            texto.lastIndexOf("$")+1,

            texto.lastIndexOf(")")

        )

    );

    const codigo=texto.split("-")[0].trim();

    const nombre=texto.split("-")[1].split("(")[0].trim();

    const cantidadNum=parseInt(cantidad.value);

    if(cantidadNum>stock){

        alert("Stock insuficiente");

        return;

    }

    const existente=carrito.find(p=>p.id==id);

    if(existente){

        if(existente.cantidad+cantidadNum>stock){

            alert("No hay suficiente stock");

            return;

        }

        existente.cantidad+=cantidadNum;

        existente.subtotal=existente.cantidad*existente.precio;

    }

    else{

        carrito.push({

            id:id,

            codigo:codigo,

            nombre:nombre,

            precio:precio,

            stock:stock,

            cantidad:cantidadNum,

            subtotal:precio*cantidadNum

        });

    }

    dibujarCarrito();

    cantidad.value=1;

}

function dibujarCarrito(){

    const tbody=document.querySelector("#tablaCarrito tbody");

    tbody.innerHTML="";

    total=0;

    carrito.forEach((item,index)=>{

        total+=item.subtotal;

        let color="success";

        if(item.stock<=5){

            color="danger";

        }

        else if(item.stock<=10){

            color="warning";

        }

        tbody.innerHTML+=`

        <tr>

        <td>${item.codigo}</td>

        <td>${item.nombre}</td>

        <td>$${item.precio.toFixed(2)}</td>

        <td>

        <span class="badge bg-${color}">

        ${item.stock}

        </span>

        </td>

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

    document.getElementById("totalVenta").innerHTML="$"+total.toFixed(2);

}

function eliminarProducto(indice){

    carrito.splice(indice,1);

    dibujarCarrito();

}

function aumentarCantidad(indice){

    if(carrito[indice].cantidad>=carrito[indice].stock){

        alert("No hay más stock.");

        return;

    }

    carrito[indice].cantidad++;

    carrito[indice].subtotal=

    carrito[indice].cantidad*

    carrito[indice].precio;

    dibujarCarrito();

}

function disminuirCantidad(indice){

    carrito[indice].cantidad--;

    if(carrito[indice].cantidad<=0){

        carrito.splice(indice,1);

    }

    else{

        carrito[indice].subtotal=

        carrito[indice].cantidad*

        carrito[indice].precio;

    }

    dibujarCarrito();

}


// ==============================
// GUARDAR VENTA
// ==============================

document.getElementById("btnGuardarVenta").addEventListener("click", function () {

    if (carrito.length == 0) {

        alert("El carrito está vacío.");

        return;

    }

    const cliente = document.querySelector("select[name='cliente']").value;

    fetch("/ventas/guardar", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            cliente: cliente,

            carrito: carrito

        })

    })

    .then(response => response.json())

    .then(data => {

        if (data.ok) {

            alert("Venta registrada correctamente.");

            location.reload();

        } else {

            alert(data.error);

        }

    })

    .catch(error => {

        console.error(error);

        alert("Error al guardar la venta.");

    });

});