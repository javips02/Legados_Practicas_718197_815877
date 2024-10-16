import subprocess
import time
import pyautogui
import pytesseract
from PIL import ImageGrab


# Asegúrate de que pytesseract esté configurado correctamente con la ruta de Tesseract-OCR
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Descomenta y configura la ruta si es necesario

def ejecutar_dosbox():
    # Ejecuta el archivo .bat que inicia DOSBox con Wine
    subprocess.Popen(["wine", "./Database-MSDOS/database.bat"])
    time.sleep(5)  # Espera que DOSBox se inicialice completamente

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
    ejecutar_dosbox()

    # Paso 2: Pulsar la tecla 4 (info BD)
    print("Pulsando la tecla 4 para obtener información de la base de datos...")
    pulsar_tecla('4')

    time.sleep(2)  # Espera un momento para que aparezca la información en pantalla

    # Paso 3: Capturar la salida
    print("Capturando salida...")
    imagen = capturar_salida()

    # Paso 4: Extraer texto de la imagen
    texto = extraer_texto(imagen)
    print("Texto extraído:")
    print(texto)

if __name__ == "__main__":
    main()
