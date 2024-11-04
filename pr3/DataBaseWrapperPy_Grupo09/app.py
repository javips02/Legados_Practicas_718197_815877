import time
from flask import Flask, jsonify, render_template, request
import wrapper
from programa import Programa

app = Flask(__name__)

programas_dummy = [
    Programa(nombre="HONGRP HORACE", tipo="ARCADE", registro="9"),
    Programa(nombre="PSPTRON", tipo="ARCADE", registro="11"),
    Programa(nombre="NISSILE", tipo="ARCADE", registro="1D"),
    Programa(nombre="HIGH NOON", tipo="ARCADE", registro="IO"),
    Programa(nombre="INTERCEPTOR CORALT", tipo="SIMULADOR", registro="14"),
    Programa(nombre="PLANETOIDS", tipo="ARCADE", registro="13"),
    Programa(nombre="SPACE RAIDERS", tipo="ARCADE", registro="12"),
    Programa(nombre="AOTOSTOPISTA GALACTICO", tipo="ARCADE", registro="17"),
    Programa(nombre="TRANZ AN", tipo="ARCADE", registro="16"),
    Programa(nombre="CONRAT ZONE", tipo="ARCADE", registro="15"),
    Programa(nombre="ZAXXAN", tipo="ARCADE", registro="T"),
    Programa(nombre="HONCHRACR", tipo="ARCADE", registro="3"),
    Programa(nombre="OF EVIL", tipo="ARCADE", registro="5"),
    Programa(nombre="THE SPIDERS", tipo="ARCADE", registro="O"),
    Programa(nombre="PAINTBOX", tipo="UTILIDAD", registro="2"),
    Programa(nombre="REVERSI", tipo="JUEGO DE MESA", registro="6"),
    Programa(nombre="MIGSP", tipo="CONVERSACIONAL", registro="1"),
    Programa(nombre="GOES SRIING", tipo="ARCADE", registro="T")
]



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
    texto = request.json.get("campo3")  # Cambiado a `request.json.get`
    print("Texto recibido en listar_cintas:", texto)  # Para ver el valor recibido en el servidor
    cintas = wrapper.main_p3(texto)
    #cintas = programas_dummy
    cintas_dict = [cinta.to_dict() for cinta in cintas]
    print("Cintas enviadas al cliente:", cintas_dict)  # Para verificar el formato en la consola del servidor
    # Enviar la lista de diccionarios como JSON
    return jsonify(cintas=cintas_dict)

if __name__ == '__main__':
    app.run(debug=True)
