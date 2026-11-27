"""Punto de entrada de la aplicación de gestión de clientes.

Inicializa la base de datos SQLite, crea la ventana principal de Tkinter
y lanza el bucle de eventos de la interfaz gráfica.
"""

import sys
import tkinter as tk

from database import inicializar_base_de_datos
from views.main_window import MainWindow
from controllers import ClienteController


def main() -> None:
    """Función principal que arranca la aplicación."""
    # 1. Inicializar la base de datos (crea archivo y tablas si no existen)
    try:
        inicializar_base_de_datos()
    except RuntimeError as error:
        print(f"Error al inicializar la base de datos: {error}")
        sys.exit(1)

    # 2. Crear la ventana raíz de Tkinter
    root = tk.Tk()

    # 3. Instanciar el controlador y la vista principal
    controller = ClienteController()
    MainWindow(root, controller)

    # 4. Iniciar el bucle de eventos
    root.mainloop()


if __name__ == "__main__":
    main()
