from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ARRAY GLOBAL (IMPORTANTE)
arr = [3, 7, 12, 18, 25, 30, 42]

@app.route('/')
def index():
    return render_template('index.html', arreglo=arr)


@app.route('/nuevo_array', methods=['POST'])
def nuevo_array():
    global arr
    data = request.get_json()
    arr = data["array"]
    return jsonify({"ok": True})


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

            pasos.append({
                "index": i,
                "linea": 3,
                "comp": comp
            })

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


@app.route('/binaria', methods=['POST'])
def binaria():
    valor = request.json['valor']
    pasos = []
    comp = 0

    l, r = 0, len(arr) - 1

    while l <= r:
        m = l + (r - l) // 2
        comp += 1

        pasos.append({
            "l": l,
            "r": r,
            "m": m,
            "linea": 4,
            "comp": comp
        })

        if arr[m] == valor:
            return jsonify({"pos": m, "pasos": pasos})

        if arr[m] < valor:
            l = m + 1
        else:
            r = m - 1

    return jsonify({"pos": -1, "pasos": pasos})


@app.route('/exponencial', methods=['POST'])
def exponencial():
    valor = request.json['valor']
    pasos = []
    comp = 0

    if arr[0] == valor:
        return jsonify({"pos": 0, "pasos": pasos})

    i = 1

    while i < len(arr) and arr[i] < valor:
        pasos.append({"index": i, "linea": 5})
        i *= 2

    l = i // 2
    r = min(i, len(arr) - 1)

    while l <= r:
        m = l + (r - l) // 2

        if arr[m] == valor:
            return jsonify({"pos": m, "pasos": pasos})

        elif arr[m] < valor:
            l = m + 1
        else:
            r = m - 1

    return jsonify({"pos": -1, "pasos": pasos})


@app.route('/interpolacion', methods=['POST'])
def interpolacion():
    valor = request.json['valor']
    pasos = []

    low, high = 0, len(arr) - 1

    while low <= high and arr[low] <= valor <= arr[high]:

        if arr[high] == arr[low]:
            break

        pos = low + int(
            (valor - arr[low]) * (high - low) /
            (arr[high] - arr[low])
        )

        pasos.append({
            "low": low,
            "high": high,
            "pos": pos,
            "linea": 5
        })

        if arr[pos] == valor:
            return jsonify({"pos": pos, "pasos": pasos})

        elif arr[pos] < valor:
            low = pos + 1
        else:
            high = pos - 1

    return jsonify({"pos": -1, "pasos": pasos})


if __name__ == '__main__':
    app.run(debug=True)