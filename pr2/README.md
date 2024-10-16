# Sistemas legados: Pŕactica 2
## Programa gráfico de acceso a un mainframe TN3270

## Instrucciones del proyecto

Este proyecto ha sido implementado en python con un enfoque portable, por lo que no es necesario disponer de ninguna dependencai en el PC para poder ejecutarlo.

### Elementos del programa 

- **api.py:** implementación de las funciones de la API que se utilizan en el proyecto.
- **gui.py:** Implementación de la interfaz gráfica de usuario (GUI).
- **requirements.txt:** Lista de las dependencias necesarias para ejecutar el proyecto (las cogerá el ejecutable de forma automática).
- **ws3270** El emulador que servirá como entorno de trabajo. Lo proporciona la librería py3270.

### Cómo ejecutar el programa

Para ejecutar el programa, lanzar el ejecutable "ejecutar.bat desde una terminal windows cmd, powershell o haciendo doble click sobre él. 

También se puede ejecutar con wine en un entorno linux con el comando "wine ejecutar.bat".


## Pasos de ejecución deseados (flujo de eventos)

### 1. Conexión con el mainframe e inicio de sesión:
 - Conectar (aparece pantalla MUSIC/SP)
 - Enter para mostrar pantalla inicio sesión (un poco de delay para esto)
 - Meter usuario y pulsar enter (GRUPO_06)
 - Meter contraseña y pulsar enter (secreto6)
 - Aparece pantalla command

 ### 2. Abrir tareas e interactuar con él:

 ### 3. Logout y desconexión:
 - Necesario usar las funciones de ws3270 para desconexión
