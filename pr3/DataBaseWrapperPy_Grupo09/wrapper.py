import subprocess
import time
import pyautogui
import pytesseract
from PIL import ImageGrab

# Configuración de la ruta de Tesseract (si es necesario)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ejecutar_dosbox():
    # Ruta completa a DOSBox
    dosbox_path = r"C:\Users\javi\PycharmProjects\Legados_Practicas_718197_815877\pr3\DataBaseWrapperPy_Grupo09\Database-MSDOS\DOSBox-0.74\DOSBox.exe"

    # Ruta completa al archivo .bat
    bat_file_path = r"C:\Users\javi\PycharmProjects\Legados_Practicas_718197_815877\pr3\DataBaseWrapperPy_Grupo09\Database-MSDOS\database.bat"

    # Ejecuta DOSBox con el archivo .bat directamente
    subprocess.Popen([dosbox_path, bat_file_path, '-noconsole'])
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
