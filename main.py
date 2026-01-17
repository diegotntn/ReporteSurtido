from dotenv import load_dotenv
load_dotenv()

from ui.app.main_window import MainWindow


def main():
    """
    Punto de entrada de la aplicación.

    RESPONSABILIDADES:
    - Cargar variables de entorno
    - Crear la ventana principal
    - Arrancar el mainloop de Tkinter
    """

    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
