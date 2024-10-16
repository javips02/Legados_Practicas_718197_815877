import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QMessageBox, QLineEdit, QListWidget, QInputDialog
import API_group6 as api

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mainframe Task Manager")
        self.layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()

        self.login_page = self.init_login_page()
        self.menu = self.init_menu()
        self.create_task_page = QWidget()  # Inicializar como QWidget
        self.show_task_page = QWidget()  # Inicializar como QWidget

        self.stacked_widget.addWidget(self.login_page)  # Agrega la página de login
        self.stacked_widget.addWidget(self.menu)
        self.stacked_widget.addWidget(self.create_task_page)
        self.stacked_widget.addWidget(self.show_task_page)

        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

        self.init_create_task_page()  # Inicializa la página de crear tareas
        self.init_show_task_page()  # Inicializa la página de mostrar tareas

    def init_login_page(self):
        login_widget = QWidget()
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Iniciar Sesión")
        login_button.clicked.connect(self.login)

        exit_button = QPushButton("Salir")
        exit_button.clicked.connect(self.exit_app)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(exit_button)

        login_widget.setLayout(layout)
        return login_widget

    def init_menu(self):
        menu = QWidget()
        menu_layout = QVBoxLayout()

        self.show_tasks_button = QPushButton("Mostrar Tareas")
        self.create_tasks_button = QPushButton("Crear Tareas")
        self.exit_button = QPushButton("Salir")

        self.show_tasks_button.clicked.connect(self.show_tasks)  # Llama a show_tasks
        self.create_tasks_button.clicked.connect(self.create_tasks)
        self.exit_button.clicked.connect(self.logout_and_exit)  # Conecta a logout_and_exit

        menu_layout.addWidget(self.show_tasks_button)
        menu_layout.addWidget(self.create_tasks_button)
        menu_layout.addWidget(self.exit_button)  # Agrega el botón de salida
        menu.setLayout(menu_layout)
        return menu

    def init_create_task_page(self):
        create_layout = QVBoxLayout()

        self.general_task_button = QPushButton("Crear Tareas Generales")
        self.specific_task_button = QPushButton("Crear Tareas Específicas")
        back_button = QPushButton("Volver al Menú Principal")

        self.general_task_button.clicked.connect(self.create_general_task)
        self.specific_task_button.clicked.connect(self.create_specific_task)
        back_button.clicked.connect(self.back_to_menu)

        create_layout.addWidget(self.general_task_button)
        create_layout.addWidget(self.specific_task_button)
        create_layout.addWidget(back_button)
        self.create_task_page.setLayout(create_layout)

    def init_show_task_page(self):
        show_layout = QVBoxLayout()

        self.general_tasks_button = QPushButton("Mostrar Tareas Generales")
        self.specific_tasks_button = QPushButton("Mostrar Tareas Específicas")
        back_button = QPushButton("Volver al Menú Principal")

        self.general_tasks_button.clicked.connect(self.display_general_tasks)
        self.specific_tasks_button.clicked.connect(self.display_specific_tasks)
        back_button.clicked.connect(self.back_to_menu)

        self.task_list = QListWidget()  # Lista para mostrar tareas
        show_layout.addWidget(self.task_list)
        show_layout.addWidget(self.general_tasks_button)
        show_layout.addWidget(self.specific_tasks_button)
        show_layout.addWidget(back_button)
        self.show_task_page.setLayout(show_layout)

    def login(self):
        # Aquí podrías agregar la lógica para verificar el usuario y contraseña
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username and password:  # Comprobación simple (debes implementar lógica real)
            QMessageBox.information(self, "Inicio de Sesión", "Inicio de sesión exitoso.")
            self.stacked_widget.setCurrentWidget(self.menu)  # Cambia a la página de menú
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un usuario y una contraseña válidos.")

    def show_tasks(self):
        self.stacked_widget.setCurrentWidget(self.show_task_page)  # Cambia a la página de mostrar tareas

    def create_tasks(self):
        self.stacked_widget.setCurrentWidget(self.create_task_page)  # Cambia a la página de crear tareas

    def create_general_task(self):
        #QMessageBox.information(self, "Crear Tarea General", "Funcionalidad para crear tareas generales.")
        try:
            # Pedir fecha
            fecha, ok = QInputDialog.getText(self, "Fecha", "Introduce la fecha (dd-mm-yyyy):")
            if not ok or not fecha:
                return  # Si el usuario cancela o no introduce la fecha, salir

            # Pedir descripción
            descripcion, ok = QInputDialog.getText(self, "Descripción", "Introduce la descripción:")
            if not ok or not descripcion:
                return  # Si el usuario cancela o no introduce la descripción, salir

            # Llamar a la función de la API con los valores proporcionados por el usuario
            api.anyadirTareaGeneral(fecha, descripcion)
            QMessageBox.information(self, "Éxito", "Tarea general creada exitosamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear tarea general: {str(e)}")


    def create_specific_task(self):
        #QMessageBox.information(self, "Crear Tarea Específica", "Funcionalidad para crear tareas específicas.")
        try:
            # Pedir fecha
            fecha, ok = QInputDialog.getText(self, "Fecha", "Introduce la fecha (dd-mm-yyyy):")
            if not ok or not fecha:
                return  # Si el usuario cancela o no introduce la fecha, salir

            # Pedir descripción
            descripcion, ok = QInputDialog.getText(self, "Descripción", "Introduce la descripción:")
            if not ok or not descripcion:
                return  # Si el usuario cancela o no introduce la descripción, salir

            # Llamar a la función de la API con los valores proporcionados por el usuario
            api.anyadirTareaGeneral(fecha, descripcion)
            QMessageBox.information(self, "Éxito", "Tarea específica creada exitosamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear tarea específica: {str(e)}")

    def display_general_tasks(self):
        self.task_list.clear()  # Limpiar la lista antes de mostrar nuevas tareas
        try:
            # Llamar a la función de la API para obtener las tareas
            tareas = api.mostrarTareasGenerales()
            if tareas:
                for fecha, descripcion in tareas:
                    self.task_list.addItem(f"{fecha}: {descripcion}")  # Agregar a la lista
            else:
                self.task_list.addItem("No hay tareas generales disponibles.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener tareas generales: {str(e)}")

    def display_specific_tasks(self):
        #QMessageBox.information(self, "Mostrar Tareas Específicas", "Funcionalidad para mostrar tareas específicas.")
        self.task_list.clear()  # Limpiar la lista antes de mostrar nuevas tareas
        try:
            # Llamar a la función de la API para obtener las tareas
            tareas = api.mostrarTareasEspecificas()
            if tareas:
                for fecha, descripcion in tareas:
                    self.task_list.addItem(f"{fecha}: {descripcion}")  # Agregar a la lista
            else:
                self.task_list.addItem("No hay tareas específicas disponibles.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener tareas especificas: {str(e)}")

    def back_to_menu(self):
        self.stacked_widget.setCurrentWidget(self.menu)

    def logout_and_exit(self):
        # Aquí puedes incluir la lógica de desconexión si es necesario
        api.logout()  # Asegúrate de que este método esté definido en tu API para manejar la desconexión
        #QMessageBox.information(self, "Logout", "Desconexión exitosa.") # Para debug
        self.close()  # Cierra la aplicación

    def exit_app(self):
        self.close()  # Cierra la aplicación

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
