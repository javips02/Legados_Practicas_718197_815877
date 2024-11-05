import time
from flask import Flask, jsonify, render_template, request
import wrapper  # Asume que `wrapper` contiene las funciones necesarias

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obtener_registros', methods=['GET'])
def obtener_registros():
    numRegistros, campoOrden = wrapper.main_p1()
    return jsonify(numRegistros=numRegistros, campoOrden=campoOrden)


@app.route('/listar_datos_programa', methods=['POST'])
def listar_datos_programa():
    data = request.get_json()
    if data is None or "nombreProgJS" not in data:
        return jsonify(error="No se recibió el nombre del programa"), 400  # Error 400 para Bad Request

    texto = data.get("nombreProgJS")
    info, numReg, cat, numCinta = wrapper.main_p2(texto)  # Supongamos que esto retorna info, numReg, cat, numCinta

    # Crea una respuesta combinada
    resultado = f"Información: {info}\nNúmero de registro: {numReg}\nCategoría: {cat}\nNúmero de cinta: {numCinta}"
    return jsonify(resultado=resultado)


@app.route('/listar_cintas', methods=['POST'])
def listar_cintas():
    texto = request.form.get("campo3")
    cintas = wrapper.main_p3(texto)
    return jsonify(cintas=cintas)

if __name__ == '__main__':
    app.run(debug=True)
