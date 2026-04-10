from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

arr = [3, 7, 12, 18, 25, 30, 42]


# ==========================
# HOME
# ==========================
@app.route('/')
def index():
    return render_template('index.html', arreglo=arr)


# ==========================
# LINEAL
# ==========================
@app.route('/lineal', methods=['POST'])
def lineal():
    valor = request.json['valor']
    pasos = []
    comp = 0

    for i in range(len(arr)):
        comp += 1

        pasos.append({
            "index": i,
            "linea": 2,
            "comp": comp
        })

        if arr[i] == valor:
            comp += 1

            # if true
            pasos.append({
                "index": i,
                "linea": 3,
                "comp": comp
            })

            # RETURN (IMPORTANTE)
            pasos.append({
                "index": i,
                "linea": 4,
                "comp": comp
            })

            return jsonify({
                "pos": i,
                "pasos": pasos,
                "compFinal": comp,
                "complejidad": "O(n)"
            })

    pasos.append({
        "index": -1,
        "linea": 5,
        "comp": comp
    })

    return jsonify({
        "pos": -1,
        "pasos": pasos,
        "compFinal": comp,
        "complejidad": "O(n)"
    })


# ==========================
# BINARIA (MEJOR CLARIDAD VISUAL)
# ==========================
@app.route('/binaria', methods=['POST'])
def binaria():
    valor = request.json['valor']
    pasos = []
    comp = 0

    l, r = 0, len(arr) - 1

    while l <= r:
        m = l + (r - l) // 2
        comp += 1

        # calcular m
        pasos.append({
            "l": l,
            "r": r,
            "m": m,
            "linea": 4,
            "fase": "calcular_m",
            "comp": comp
        })

        comp += 1
        if arr[m] == valor:
            pasos.append({
                "l": l,
                "r": r,
                "m": m,
                "linea": 5,
                "fase": "encontrado",
                "comp": comp
            })

            return jsonify({
                "pos": m,
                "pasos": pasos,
                "complejidad": "O(log n)"
            })

        comp += 1
        if arr[m] < valor:
            pasos.append({
                "l": l,
                "r": r,
                "m": m,
                "linea": 6,
                "fase": "derecha",
                "comp": comp
            })
            l = m + 1

        else:
            pasos.append({
                "l": l,
                "r": r,
                "m": m,
                "linea": 7,
                "fase": "izquierda",
                "comp": comp
            })
            r = m - 1

    return jsonify({
        "pos": -1,
        "pasos": pasos,
        "complejidad": "O(log n)"
    })


# ==========================
# EXPONENCIAL (PASO A PASO LIMPIO)
# ==========================
@app.route('/exponencial', methods=['POST'])
def exponencial():
    valor = request.json['valor']
    pasos = []
    comp = 0

    if arr[0] == valor:
        pasos.append({
            "index": 0,
            "linea": 3,
            "fase": "check_0",
            "comp": 1
        })
        return jsonify({"pos": 0, "pasos": pasos})

    i = 1

    # expansión
    while i < len(arr) and arr[i] < valor:
        comp += 1

        pasos.append({
            "index": i,
            "linea": 5,
            "fase": "expansion",
            "comp": comp
        })

        i *= 2

    l = i // 2
    r = min(i, len(arr) - 1)

    pasos.append({
        "l": l,
        "r": r,
        "linea": 6,
        "fase": "rango",
        "comp": comp
    })

    # binaria interna
    while l <= r:
        m = l + (r - l) // 2
        comp += 1

        pasos.append({
            "l": l,
            "r": r,
            "m": m,
            "linea": 8,
            "fase": "binaria",
            "comp": comp
        })

        if arr[m] == valor:
            pasos.append({
                "l": l,
                "r": r,
                "m": m,
                "linea": 9,
                "fase": "encontrado",
                "comp": comp
            })

            return jsonify({
                "pos": m,
                "pasos": pasos,
                "complejidad": "O(log n)"
            })

        elif arr[m] < valor:
            pasos.append({
                "l": l,
                "r": r,
                "m": m,
                "linea": 10,
                "fase": "derecha",
                "comp": comp
            })
            l = m + 1

        else:
            pasos.append({
                "l": l,
                "r": r,
                "m": m,
                "linea": 11,
                "fase": "izquierda",
                "comp": comp
            })
            r = m - 1

    return jsonify({
        "pos": -1,
        "pasos": pasos,
        "complejidad": "O(log n)"
    })


# ==========================
# INTERPOLACIÓN (FIX DIV/0 + ESTABILIDAD)
# ==========================
@app.route('/interpolacion', methods=['POST'])
def interpolacion():
    valor = request.json['valor']
    pasos = []
    comp = 0

    low, high = 0, len(arr) - 1

    while low <= high and arr[low] <= valor <= arr[high]:

        if arr[high] == arr[low]:
            pasos.append({
                "low": low,
                "high": high,
                "linea": 4,
                "fase": "igual",
                "comp": comp
            })
            break

        pos = low + int(
            (valor - arr[low]) * (high - low) /
            (arr[high] - arr[low])
        )

        comp += 1

        pasos.append({
            "low": low,
            "high": high,
            "pos": pos,
            "linea": 5,
            "fase": "pos",
            "comp": comp
        })

        if pos < 0 or pos >= len(arr):
            break

        comp += 1

        if arr[pos] == valor:
            pasos.append({
                "low": low,
                "high": high,
                "pos": pos,
                "linea": 7,
                "fase": "encontrado",
                "comp": comp
            })

            return jsonify({
                "pos": pos,
                "pasos": pasos,
                "complejidad": "O(log log n)"
            })

        elif arr[pos] < valor:
            pasos.append({
                "low": low,
                "high": high,
                "pos": pos,
                "linea": 8,
                "fase": "derecha",
                "comp": comp
            })
            low = pos + 1

        else:
            pasos.append({
                "low": low,
                "high": high,
                "pos": pos,
                "linea": 9,
                "fase": "izquierda",
                "comp": comp
            })
            high = pos - 1

    return jsonify({
        "pos": -1,
        "pasos": pasos,
        "complejidad": "O(log log n)"
    })


# ==========================
# RUN
# ==========================
if __name__ == '__main__':
    app.run(debug=True)