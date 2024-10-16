from py3270 import Emulator
import time

# Fijar host y puerto
host = '155.210.152.51:3270'
tiempo = 2

# Definir emulador
em = Emulator()

#
#   FUNCIONES AUXILIARES DEL PROGRAMA
#

def login():
    em.connect(host)
    print("Conectado, esperando...")
    time.sleep(tiempo)
    em.wait_for_field()
    em.send_enter()
    time.sleep(tiempo)

def logout():
    print("Vamos a desconectar, esperando...")
    time.sleep(tiempo)
    em.terminate()
    print("Desconectado")

def esta_conectado():
    return em.is_connected()

def leerGenerico(fila, columna, numBytes):
    contenido = em.string_get(fila, columna, numBytes)
    return contenido

def escribirLogin(user, password):
    em.fill_field(3, 18, user, 8)
    em.fill_field(5, 18, password, 8)
    em.send_enter()
    em.wait_for_field()
    time.sleep(tiempo)

def mostrarPantalla():
    for linea in range(1, 42):
        contenido = leerGenerico(linea, 1, 80)
        print("Mostrando pantalla: ", contenido)

def clean():
    while em.string_get(43, 71, 7) != 'More...':
        em.send_enter()
        em.wait_for_field()
        time.sleep(tiempo)
    em.send_enter()

def unir_letra_a_palabra(palabra, letra):
    return palabra + letra

def espera():
    em.wait_for_field()
    time.sleep(tiempo)

def reemplazar_espacios_con_guiones(texto):
    return texto.replace(' ', '_')

def reemplazar_guiones_con_espacios(texto):
    return texto.replace('_', ' ')

#
#   FUNCIONES PRINCIPALES DEL PROGRAMA
#

def comprobarLogin(user, password):
    escribirLogin(user, password)
    contenido = leerGenerico(5, 1, 26)
    if contenido == "Press ENTER to continue...":
        em.send_enter()
        em.wait_for_field()
        time.sleep(tiempo)
        return True
    return False

def ejecutarTarea():
    em.fill_field(3, 15, 'tareas.c', 8)
    em.send_enter()
    espera()

def escribirPassword(password):
    em.fill_field(5, 18, password, 8)
    em.send_enter()
    espera()

def menu_opcion(opcion):
    em.send_string(opcion, ypos=None, xpos=None)
    em.send_enter()
    espera()

def anyadirTareaGeneral(fecha, descripcion):
    em.send_string('1', ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_clear()
    fecha = reemplazar_espacios_con_guiones(fecha)
    em.send_string(fecha, ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_clear()
    descripcion = reemplazar_espacios_con_guiones(descripcion)
    em.send_string(descripcion, ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_string('3', ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_clear()

def anyadirTareaEspecifica(fecha, nombre, descripcion):
    em.send_string('2', ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_clear()
    fecha = reemplazar_espacios_con_guiones(fecha)
    em.send_string(fecha, ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_clear()
    nombre = reemplazar_espacios_con_guiones(nombre)
    em.send_string(nombre, ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_clear()
    descripcion = reemplazar_espacios_con_guiones(descripcion)
    em.send_string(descripcion, ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_string('3', ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_clear()

def mostrarTareasGenerales():
    listaTareasGenerales = []
    em.send_clear()
    em.send_string('2', ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_clear()
    em.send_string('1', ypos=None, xpos=None)
    em.send_enter()
    espera()
    
    linea = 42 
    while leerGenerico(linea, 1, 4) != "TASK" and (linea != 1):
        linea -= 1

    comienzo = linea

    if comienzo != 1:
        while leerGenerico(comienzo, 1, 4) == "TASK":
            fecha = em.string_get(comienzo, 17, 4)
            columna_inicial = 28
            while em.string_get(comienzo, columna_inicial, 1) != " ":
                columna_inicial += 1
            columna_final = columna_inicial
            descripcion = em.string_get(comienzo, 28, (columna_final - 1))
            descripcion = reemplazar_guiones_con_espacios(descripcion)
            listaTareasGenerales.append((fecha, descripcion))
            comienzo -= 1

    em.send_string('3', ypos=None, xpos=None)
    em.send_enter()
    espera()
    em.send_clear()
    return listaTareasGenerales

def mostrarTareasEspecificas():
    listaTareasEspecificas = []

    em.send_string('2', ypos=None, xpos=None)
    em.send_enter()
    espera()

    em.send_clear()
    em.send_string('2', ypos=None, xpos=None)
    em.send_enter()
    espera()

    linea = 42 
    while (leerGenerico(linea, 1, 4) != "TASK") and (linea != 1):
        linea -= 1

    comienzo = linea

    mostrarPantalla()

    if comienzo != 1:
        while leerGenerico(comienzo, 1, 4) == "TASK":
            fecha = em.string_get(comienzo, 18, 4)
            letra = ""
            nombre = ""
            columna_inicial_nombre = 23
            while em.string_get(comienzo, columna_inicial_nombre, 1) != " ":
                letra = em.string_get(comienzo, columna_inicial_nombre, 1)
                nombre = unir_letra_a_palabra(nombre, letra)
                columna_inicial_nombre += 1

            nombre = reemplazar_guiones_con_espacios(nombre)
            columna_inicial = columna_inicial_nombre + 1
            col = columna_inicial
            while em.string_get(comienzo, columna_inicial, 1) != " ":
                columna_inicial += 1

            columna_final = columna_inicial
            descripcion = em.string_get(comienzo, col, (columna_final - 1))
            descripcion = reemplazar_guiones_con_espacios(descripcion)
            listaTareasEspecificas.append((fecha, nombre, descripcion))
            comienzo -= 1

    em.send_string('3', ypos=None, xpos=None)
    em.send_enter()
    espera()
    #em.send_clear()
    return listaTareasEspecificas
