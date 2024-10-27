import os
import subprocess
import sys
import time
import re
import difflib
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
    dosbox_path = r".\Database-MSDOS\DOSBox-0.74\DOSBox.exe"
    # Ruta completa al archivo .bat
    db_file_path = r".\Database-MSDOS\Database\gwbasic.bat"

    # Ejecuta DOSBox con el archivo .bat y guarda el proceso
    process = subprocess.Popen([dosbox_path, db_file_path, '-fullscreen', '-noconsole'])
    time.sleep(8)  # Espera que DOSBox se inicialice completamente
    return process  # Devuelve el proceso para poder terminarlo más tarde

def pulsar_tecla(tecla):
    # Usa PyAutoGUI para pulsar la tecla
    pyautogui.press(tecla)

def capturar_salida():
    # Captura la pantalla y la guarda en un archivo temporal
    image = ImageGrab.grab()  # Captura la pantalla completa
    image.save("captura.png")  # Guarda la imagen capturada
    return "captura.png"

def extraer_texto(imagen):
    # Configure Tesseract path for PyTesseract
    pytesseract.pytesseract.tesseract_cmd = resource_path(r'tesseract\tesseract.exe')

    # Set the TESSDATA_PREFIX environment variable to the path where 'tessdata' is located
    tessdata_dir = resource_path(r'tesseract\tessdata')
    os.environ['TESSDATA_PREFIX'] = tessdata_dir

    # call PyTesseract on the screenshot image, and save the output as a string
    texto = pytesseract.image_to_string(imagen, lang='spa', config='--psm 6 -c preserve_interword_spaces=1').strip()

    return texto


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

# Usa diccionario para encontrar la palabra mas cercana que tenga sentido para el campo de orden
def corregir_campo_orden(campo_ocr, opciones):
    # Usar difflib para encontrar la opción más cercana al texto detectado
    campo_correccion = difflib.get_close_matches(campo_ocr, opciones, n=1, cutoff=0.6)
    if campo_correccion:
        return campo_correccion[0]
    return campo_ocr

def main():
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
        extraer_informacion_flexible_tarea1(texto)

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

if __name__ == "__main__":
    main()
