import subprocess
import time
import pyautogui
import pytesseract
from PIL import ImageGrab

# Configuración de la ruta de Tesseract (si es necesario)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ejecutar_dosbox():
    # Ruta completa a DOSBox
    dosbox_path = r".\Database-MSDOS\DOSBox-0.74\DOSBox.exe"
    # Ruta completa al archivo .bat
    db_file_path = r".\Database-MSDOS\Database\gwbasic.bat"

    # Ejecuta DOSBox con el archivo .bat y guarda el proceso
    process = subprocess.Popen([dosbox_path, db_file_path, '-fullscreen', '-noconsole'])
    time.sleep(5)  # Espera que DOSBox se inicialice completamente
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
    # Usa pytesseract para extraer texto de la imagen
    texto = pytesseract.image_to_string(imagen)
    return texto

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

        # Paso 4: Extraer texto de la imagen
        print("Extrayendo texto...")
        texto = extraer_texto(imagen)
        print("Texto extraído:")
        print(texto)

    finally:
        # Paso 5: Matar el proceso de DOSBox
        print("Cerrando DOSBox...")
        dosbox_process.terminate()

if __name__ == "__main__":
    main()
