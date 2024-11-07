import os
import subprocess
import sys
import time
import re
import difflib
from programa import Programa
import pyautogui
import pytesseract
from PIL import ImageGrab

# Setup resource path, a relative path for use with PyInstaller
# When the output .exe from PyInstaller runs, it will extract all files to a temp folder (sys._MEIPASS) in Windows
# The 'resource_path' function sets the file path to the sys._MEIPASS location if it was created by PyInstaller
# For development (i.e., not using a .exe output from PyInstaller), this sets up the file path normally
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def ejecutar_dosbox():
    # Ruta completa a DOSBox
    dosbox_path = r"Database-MSDOS\DOSBox-0.74\DOSBox.exe"
    # Ruta completa al archivo .bat
    db_file_path = r"Database-MSDOS\Database\gwbasic.bat"

    # Ejecuta DOSBox con el archivo .bat y guarda el proceso
    process = subprocess.Popen([dosbox_path, db_file_path, '-fullscreen', '-noconsole'])
    time.sleep(5)  # Espera que DOSBox se inicialice completamente
    return process  # Devuelve el proceso para poder terminarlo más tarde

def pulsar_tecla(tecla):
    # Usa PyAutoGUI para pulsar la tecla
    pyautogui.press(tecla)

def capturar_salida(ruta="captura.png"):
    # Captura la pantalla y la guarda en la ruta especificada
    image = ImageGrab.grab()  # Captura la pantalla completa
    image.save(ruta)          # Guarda la imagen en la ruta dada
    return ruta

def extraer_texto(imagen):
    # Configure Tesseract path for PyTesseract
    pytesseract.pytesseract.tesseract_cmd = resource_path(r'tesseract\tesseract.exe')

    # Set the TESSDATA_PREFIX environment variable to the path where 'tessdata' is located
    tessdata_dir = resource_path(r'tesseract\tessdata')
    os.environ['TESSDATA_PREFIX'] = tessdata_dir

    # call PyTesseract on the screenshot image, and save the output as a string
    texto = pytesseract.image_to_string(imagen, lang='spa', config='--psm 6 -c preserve_interword_spaces=1').strip()

    return texto


def obtener_categoria_mas_parecida(categoria_ingresada):
    # Lista de categorías posibles
    categorias = [
        "UTILIDAD", "ARCADE", "CONVERSACIONAL", "VIDEOAVENTURA",
        "SIMULADOR", "JUEGO DE MESA", "S. DEPORTIVO", "ESTRATEGIA"
    ]

    # Obtener la categoría más parecida con un mínimo de similitud de 0.5
    coincidencias = difflib.get_close_matches(categoria_ingresada, categorias, n=1, cutoff=0.5)

    # Retornar la coincidencia más cercana o un mensaje en caso de que no haya coincidencias
    if coincidencias:
        return coincidencias[0]
    else:
        return "Categoría no encontrada"


def extraer_informacion_flexible_tarea1(texto_extraido):

    # Buscar el número de registros con flexibilidad (de momento he puesto confusion entre N y M, y para I y L
    numero_registros_match = re.search(r'(CO[M|N]T[I|L][E][M|N]E)\s+(\d+)\s+ARCHIVOS', texto_extraido)
    if numero_registros_match:
        numero_registros = numero_registros_match.group(2)
    else:
        numero_registros = "Desconocido"

    # Buscar el campo de ordenación con flexibilidad
    campo_orden_match = re.search(r'(ORDENADA|ORDEMADA) (SEGUN|SEGUM) EL CAMPO (\w+)', texto_extraido)
    if campo_orden_match:
        campo_orden = campo_orden_match.group(3)
        # Usar difflib para corregir el campo de orden si está mal
        campo_orden = corregir_campo_orden(campo_orden, ["ANTIGUEDAD", "NOMBRE", "FECHA", "ID"])
    else:
        campo_orden = "Desconocido"

    # Imprimir la información filtrada
    print(f"Numero de registros en la base de datos: {numero_registros}")
    print(f"Ordenacion segun el campo: {campo_orden}")
    return numero_registros,campo_orden

# Usa diccionario para encontrar la palabra mas cercana que tenga sentido para el campo de orden
def corregir_campo_orden(campo_ocr, opciones):
    # Usar difflib para encontrar la opción más cercana al texto detectado
    campo_correccion = difflib.get_close_matches(campo_ocr, opciones, n=1, cutoff=0.6)
    if campo_correccion:
        return campo_correccion[0]
    return campo_ocr

def extraer_informacion_flexible_tarea2(texto_extraido, nombreProg):
    patternErr = r"PULSA [E|R][R|N|M]TER"  # Flexible ante errores OCR comunes en "ENTER"
    error_busqueda_match = re.search(patternErr, texto_extraido)
    if error_busqueda_match:
        return "Error: no hay ningun programa con el nombre ", 0, 0, 0

    # Buscar el número de registros con flexibilidad (de momento he puesto confusion entre N y M, y para I y L

    pattern = r'\b(\d+)\s+\S*\s+(UTILIDAD|ARCADE|CONVERSACIO[N|M]AL|VIDEOAVENTURA|SIMULADOR|JUEGO DE MESA|S\.\s?[DEPORTIVO|DEPORTI[L|I]VO]|ESTRATEGIA)\b.*CINT[A|E][E|:]\W?([A-Z]|\d+)'

    datos_programa_match = re.search(pattern, texto_extraido)

    if datos_programa_match:
        pulsar_tecla('S') #Confirmar registro correcto
        pulsar_tecla('enter')
        time.sleep(0.5)
        pulsar_tecla('N') # Confirmar no alterar datos del registro
        pulsar_tecla('enter')
        time.sleep(0.5)
        pulsar_tecla('N') # Confirmar no quieor buscar mas
        pulsar_tecla('enter')
        # Extraer los datos si se encuentra coincidencia
        numero_registro = datos_programa_match.group(1)  # Puede ser None si no hay un número
        categoria = obtener_categoria_mas_parecida(datos_programa_match.group(2))
        numero_cinta = datos_programa_match.group(3)
        print("Número de registro:", numero_registro)
        print("Categoría:", categoria)
        print("Número de cinta:", numero_cinta)
        return  "Número de registro:"+numero_registro+"Categoría:"+categoria+"Número de cinta:"+numero_cinta, numero_registro, categoria, numero_cinta
    else:
        return "Error desconocido o de OCR", 0, 0, 0

def main_p1():
    # Paso 1: Ejecutar DOSBox
    print("Ejecutando DOSBox...")
    dosbox_process = ejecutar_dosbox()

    try:
        # Paso 2: Pulsar la tecla 4 (info BD)
        print("Pulsando la tecla 4 para obtener información de la base de datos...")
        pulsar_tecla('4')
        time.sleep(2)  # Espera un momento para que aparezca la información en pantalla

        # Paso 3: Capturar la salida
        print("Capturando salida...")
        imagen = capturar_salida()
        pulsar_tecla('enter')

        # Paso 4: Extraer texto de la imagen
        print("Extrayendo texto...")
        texto = extraer_texto(imagen)
        print("Texto extraído:")
        print(texto)

        print("Datos filtrados:")
        numRegistros, campoOrden =extraer_informacion_flexible_tarea1(texto)
        return numRegistros, campoOrden

    finally:
        # Paso 5: Matar el proceso de DOSBox
        print("Cerrando DOSBox...")
        pulsar_tecla('8')
        time.sleep(0.5)
        pulsar_tecla('S')
        time.sleep(0.5)
        pulsar_tecla('enter')
        time.sleep(0.5)
        dosbox_process.terminate()


def main_p2(nombreprog="MUGSY"):
    # Paso 1: Ejecutar DOSBox
    print("Ejecutando DOSBox...")
    dosbox_process = ejecutar_dosbox()

    try:
        # Paso 2: Pulsar la tecla 4 (info BD)
        print("Pulsando la tecla 7 para obtener información de un registor concreto en la base de datos...")
        pulsar_tecla('7')
        time.sleep(1)  # Espera un momento para que aparezca la información en pantalla
        pulsar_tecla('N') # no sabemos el num registro que queremos (opciones gui)
        pulsar_tecla('enter')
        # Introducir el nombre del programa a buscar
        for letra in nombreprog:
            pulsar_tecla(letra)
        pulsar_tecla('enter')
        time.sleep(3)

        # Capturar la salida
        print("Capturando resultado busqueda programa y extrayendo texto con OCR...")
        imagen = capturar_salida()
        # Extraer texto de la imagen
        texto = extraer_texto(imagen)
        print("Texto extraído:")
        print(texto)

        print("Datos filtrados:")
        info, numreg, cat, numcinta = extraer_informacion_flexible_tarea2(texto,nombreprog)
        if info == "Error desconocido o de OCR" or info == "Error: no hay ningun programa con el nombre ": # pulsar enter y salir
            pulsar_tecla("enter")  # aceptar not found
            pulsar_tecla("N") # no buscar más
            pulsar_tecla("enter")

        print(info+nombreprog)
        return info, numreg, cat, numcinta

    finally:
        # Paso 5: Matar el proceso de DOSBox
        print("Cerrando DOSBox...")
        dosbox_process.terminate()
def main_p3(cinta="A"):
    # Paso 1: Ejecutar DOSBox
    print("Extrayendo texto con OCR... de la cinta " + cinta)
    print("Ejecutando DOSBox...")
    dosbox_process = ejecutar_dosbox()
    programas = []
    try:
        cambiarConfiguracionOrdenacion()
        time.sleep(1)
        pulsar_tecla('6')
        time.sleep(1)
        for letra in cinta:
            pulsar_tecla(letra)
        pulsar_tecla('enter')
        time.sleep(3)
        # Llamamos a extraer_informacion_flexible_tarea3, que ahora maneja el bucle `while`
        programas = extraer_informacion_flexible_tarea3(cinta)

        # Imprimimos los programas encontrados
        printProgramas(programas)

        pulsar_tecla('enter')
        time.sleep(2)
        return programas
    finally:
        # Paso 5: Matar el proceso de DOSBox
        print("Cerrando DOSBox...")
        pulsar_tecla('8')
        dosbox_process.terminate()


def printProgramas(programas):
    print("Programas encontrados en el bucle:------")
    for programa in programas:
        print(programa)


#Lee todas las cintas que se llamen cinta y devuelve la lista de programas
# Devuelve una lista de programas encontrados
def extraer_informacion_flexible_tarea3(cintas):
    programas = []
    final = True
    letraMatchAuxiliar = None
    while final:
        # Captura de pantalla de DOSBox
        capturar_salida("captura.png")

        # Extraer texto de la imagen
        texto_extraido = extraer_texto("captura.png")
        pattern = ('(\w{3})\s+(\S+\s?\S*)\s+([U|O]TILIDAD|ARCADE|CONVERSACIO[N|M]AL|VIDEOAVENTURA|SIM[U|I]LADOR|JUEGO DE [N|M]ESA|S\.\s?[DEPORTIVO|DEPORTI[L|I]VO]|ESTRATEGIA)'
                   '\s+([A-Z]|\d+)\s+(.*)')

        for line in texto_extraido.strip().split('\n'):
            datos_programa_match = re.search(pattern, line)
            print(line)
            if datos_programa_match:
                if letraMatchAuxiliar is None:
                    letraMatchAuxiliar = datos_programa_match.group(4) # Guarda la primera letra encontrada

                if not (datos_programa_match.group(4).startswith(cintas)
                        or datos_programa_match.group(4).startswith(letraMatchAuxiliar)):
                    # Termina el bucle si encuentra una cinta diferente
                    final = False
                    break

                # Procesa el programa si cumple las condiciones
                print("Datos del programa:")
                print("Número de registro:", datos_programa_match.group(1))
                print("Nombre del programa:", datos_programa_match.group(2))
                print("Categoría:", obtener_categoria_mas_parecida(datos_programa_match.group(3)))
                print("Número de cinta:", datos_programa_match.group(4))
                print("Información adicional:", datos_programa_match.group(5))
                print("-----------------------------")

                # Crear instancia de Programa y añadirla a la lista
                programa = Programa(datos_programa_match.group(2),
                                    obtener_categoria_mas_parecida(datos_programa_match.group(3)),
                                    datos_programa_match.group(5))
                programas.append(programa)

        # Pulsar tecla 'space' para avanzar si `final` aún es True
        if final:
            pulsar_tecla('space')
        time.sleep(3)

    return programas

def cambiarConfiguracionOrdenacion():
    print("Pulsando la tecla 3 para cambiar la configuracion de ordenacion de la base de datos...")
    pulsar_tecla('3')
    pulsar_tecla('enter')
    time.sleep(1)
    pulsar_tecla('3')
    pulsar_tecla('enter')
    print("Para que lo ordene por cintas")
    time.sleep(25)
    pulsar_tecla('enter')
    print("Configurado ordenacion por cinta")


if __name__ == "__main__":
    #main_p1() # descomentar para ejecutar funcion 1
    #main_p2() # descomanetar para ejecutar funcion 2
    main_p2("PAINTBOX")
    #main_p2("NONEXISTENT")
    main_p3("B")


