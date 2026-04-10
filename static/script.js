async function buscar(tipo) {
    limpiarTodo();
    limpiarTabla();
    mostrarCodigo(tipo);

    let valor = parseInt(document.getElementById("valor").value);
    let salida = document.getElementById("salida");
    let tiempoEl = document.getElementById("tiempo");

    salida.innerText = "...";

    let inicio = performance.now();

    let res = await fetch("/" + tipo, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ valor: valor })
    });

    let data = await res.json();

    let pasoNum = 1;

    for (let paso of data.pasos) {

        limpiarArray();
        limpiarIndices();

        if (tipo === "lineal") {
            resaltarLineal(paso.index);
        }

        if (tipo === "binaria") {
            resaltarBinaria(paso);
        }

        if (tipo === "interpolacion") {
            resaltarInterpolacion(paso);
        }

        if (tipo === "exponencial") {
            resaltarLineal(paso.index);
        }

        resaltarCodigo(tipo, paso.linea);

        agregarFila(
            tipo,
            pasoNum++,
            paso,
            paso.valor,
            "-"
        );

        let ms = performance.now() - inicio;
        tiempoEl.innerText = `${ms.toFixed(2)} ms | ${(ms / 1000).toFixed(4)} s`;

        await esperar(350);
    }

    let msFinal = performance.now() - inicio;
    tiempoEl.innerText = `${msFinal.toFixed(2)} ms | ${(msFinal / 1000).toFixed(4)} s`;

    if (data.pos != -1) {
        marcar(data.pos);
        salida.innerText = valor;
    } else {
        resaltarNoEncontrado(tipo);
        salida.innerText = -1;
    }
}


// ==========================
// UTILIDADES
// ==========================
function safeCaja(i) {
    let cajas = document.getElementsByClassName("caja");
    return (i >= 0 && i < cajas.length) ? cajas[i] : null;
}

function safeIndice(i) {
    let indices = document.getElementsByClassName("indice");
    return (i >= 0 && i < indices.length) ? indices[i] : null;
}

function moverPointer(id, index) {
    let columnas = document.querySelectorAll(".columna");

    if (!columnas[index]) return;

    let el = columnas[index];
    let container = document.getElementById("array");

    let rect = el.getBoundingClientRect();
    let parent = container.getBoundingClientRect();

    let x = rect.left - parent.left + rect.width / 2 - 12;

    document.getElementById(id).style.transform =
        `translateX(${x}px)`;
}


// ==========================
// RESALTADO
// ==========================
function resaltarLineal(i) {
    let cajas = document.getElementsByClassName("caja");

    for (let j = 0; j < cajas.length; j++) {
        cajas[j].classList.remove("activo", "descartado");
    }

    let actual = safeCaja(i);
    if (actual) actual.classList.add("activo");
}

function resaltarBinaria(paso) {
    limpiarIndices();

    if (paso.l != null) {
        moverPointer("ptrL", paso.l);
        safeIndice(paso.l)?.classList.add("descartado");
    }

    if (paso.r != null) {
        moverPointer("ptrR", paso.r);
        safeIndice(paso.r)?.classList.add("descartado");
    }

    if (paso.m != null) {
        moverPointer("ptrM", paso.m);
        safeIndice(paso.m)?.classList.add("activo");
    }
}

function resaltarInterpolacion(paso) {
    limpiarIndices();

    if (paso.low != null) {
        moverPointer("ptrL", paso.low);
        safeIndice(paso.low)?.classList.add("descartado");
    }

    if (paso.high != null) {
        moverPointer("ptrR", paso.high);
        safeIndice(paso.high)?.classList.add("descartado");
    }

    if (paso.pos != null) {
        moverPointer("ptrM", paso.pos);
        safeIndice(paso.pos)?.classList.add("activo");
    }
}

function marcar(i) {
    let c = safeCaja(i);
    if (c) c.classList.add("encontrado");
}


// ==========================
// LIMPIEZA
// ==========================
function limpiarArray() {
    document.querySelectorAll(".caja")
        .forEach(c => c.classList.remove("activo", "encontrado", "descartado"));
}

function limpiarIndices() {
    document.querySelectorAll(".indice")
        .forEach(i => i.classList.remove("activo", "descartado"));
}

function limpiarTodo() {
    limpiarArray();
    limpiarIndices();
}

function limpiarTabla() {
    document.querySelector("#tabla tbody").innerHTML = "";
}


// ==========================
// TIEMPO
// ==========================
function esperar(ms) {
    return new Promise(resolve => {
        setTimeout(() => requestAnimationFrame(resolve), ms);
    });
}


// ==========================
// CODIGO
// ==========================
function resaltarCodigo(tipo, linea) {
    limpiarCodigo();

    let pref = {
        lineal: "l",
        binaria: "b",
        exponencial: "e",
        interpolacion: "i"
    };

    let el = document.getElementById(pref[tipo] + linea);
    if (el) el.classList.add("activa");
}

function limpiarCodigo() {
    document.querySelectorAll(".codigo span")
        .forEach(l => l.classList.remove("activa", "resaltado"));
}

function resaltarNoEncontrado(tipo) {
    let pref = {
        lineal: "l5",
        binaria: "b9",
        exponencial: "e13",
        interpolacion: "i11"
    };

    let el = document.getElementById(pref[tipo]);
    if (el) el.classList.add("resaltado");
}


// ==========================
// TABLA
// ==========================
function agregarFila(tipo, paso, datos, valor, resultado) {

    let tabla = document.querySelector("#tabla tbody");

    let fila = document.createElement("tr");

    if (tipo === "binaria") {
        fila.innerHTML = `
            <td>${paso}</td>
            <td>${datos.l ?? "-"}</td>
            <td>${datos.m ?? "-"}</td>
            <td>${datos.r ?? "-"}</td>
            <td>${valor ?? "-"}</td>
            <td>${resultado ?? "-"}</td>
        `;
    }

    else if (tipo === "interpolacion") {
        fila.innerHTML = `
            <td>${paso}</td>
            <td>${datos.low ?? "-"}</td>
            <td>${datos.pos ?? "-"}</td>
            <td>${datos.high ?? "-"}</td>
            <td>${valor ?? "-"}</td>
            <td>${resultado ?? "-"}</td>
        `;
    }

    else {
        fila.innerHTML = `
            <td>${paso}</td>
            <td>${datos.index ?? "-"}</td>
            <td>-</td>
            <td>-</td>
            <td>${valor ?? "-"}</td>
            <td>${resultado ?? "-"}</td>
        `;
    }

    tabla.appendChild(fila);
}


// ==========================
// GENERAR ARRAY (🔥 ARREGLADO)
// ==========================
function generarArray(n) {
    let nuevo = [];

    for (let i = 0; i < n; i++) {
        nuevo.push(Math.floor(Math.random() * 100));
    }

    nuevo.sort((a, b) => a - b);

    fetch("/nuevo_array", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ array: nuevo })
    })
    .then(res => {
        if (!res.ok) throw new Error("Error en servidor");
        return res.json();
    })
    .then(() => {
        location.reload(); // recarga con nuevo array
    })
    .catch(err => console.error("Error:", err));
}


// ==========================
// MOSTRAR CODIGO
// ==========================
function mostrarCodigo(tipo) {
    document.querySelectorAll(".bloque")
        .forEach(b => b.classList.remove("activo"));

    document.getElementById("codigo-" + tipo)
        .classList.add("activo");
}