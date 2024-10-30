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
    texto = request.form.get("sombratexto1")
    resultado = wrapper.main_p2(texto)
    return jsonify(resultado=resultado)

@app.route('/listar_cintas', methods=['POST'])
def listar_cintas():
    texto = request.form.get("campo3")
    cintas = wrapper.main_p3(texto)
    return jsonify(cintas=cintas)

if __name__ == '__main__':
    app.run(debug=True)
