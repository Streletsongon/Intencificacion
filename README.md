# Sistema de Gestión de Clientes

Aplicación de escritorio completa y modular para gestionar información de clientes mediante una interfaz gráfica intuitiva y una base de datos persistente en SQLite. Permite realizar operaciones CRUD (Crear, Consultar, Modificar y Eliminar) de forma sencilla.

## Tecnologías utilizadas

- **Lenguaje:** Python 3
- **Interfaz gráfica:** Tkinter (incluyendo `ttk`)
- **Base de datos:** SQLite (vía la biblioteca `sqlite3` de Python)
- **Patrón de diseño:** Separación de responsabilidades en capas (Modelo, Controlador, Vista, Acceso a datos)

## Requisitos necesarios

- Python 3 instalado (no se requieren librerías externas; Tkinter y sqlite3 vienen incluidas en la distribución estándar de Python).
- Visual Studio Code (recomendado como entorno de desarrollo).
- Extensión Cline (asistente de programación, opcional).

## Estructura de carpetas

```
clinebot/
├── main.py              # Punto de entrada de la aplicación
├── database.py          # Conexión y operaciones con SQLite
├── models.py            # Representación y estructura de los datos (Cliente)
├── controllers.py       # Lógica de negocio y validaciones
├── views/
│   ├── __init__.py      # Paquete de vistas
│   └── main_window.py   # Ventana principal con Tkinter/ttk
├── database/
│   └── app.db           # Base de datos SQLite (se crea automáticamente)
├── assets/              # Recursos estáticos (imágenes, iconos, etc.)
└── README.md            # Documentación e instrucciones de ejecución
```

## Instalación y configuración

1. Clona o descarga este repositorio en tu máquina local.
2. Abre la carpeta del proyecto en Visual Studio Code.
3. No es necesario instalar dependencias externas: solo se usan módulos de la biblioteca estándar de Python (`tkinter`, `ttk`, `sqlite3`, `dataclasses`).
4. Ejecuta la aplicación (ver sección siguiente).

## Cómo ejecutar la aplicación

Desde la terminal, sitúate en la carpeta del proyecto y ejecuta:

```bash
python main.py
```

Al iniciar:
1. Se crea automáticamente el archivo `database/app.db` si no existe.
2. Se crean las tablas necesarias (`clientes`).
3. Se abre la ventana principal con la lista de clientes (vacía la primera vez).

## Funcionamiento de cada módulo

### main.py
Punto de entrada de la aplicación. Inicializa la base de datos, crea la ventana raíz de Tkinter, instancia el controlador y la vista principal, y lanza el bucle de eventos.

### database.py
Capa de acceso a datos. Se encarga exclusivamente de:
- Crear la conexión a SQLite (y el archivo de base de datos si no existe).
- Crear la tabla `clientes` al iniciar (clave primaria `id_cliente` con autoincremento).
- Ejecutar consultas parametrizadas para prevenir inyecciones SQL.
- Operaciones CRUD: insertar, consultar todos, consultar por ID, buscar, actualizar y eliminar.
- Manejo de errores de conexión y consultas.

### models.py
Representa la estructura de los datos. Define la clase `Cliente` (dataclass) con los campos: `id_cliente`, `nombre`, `email`, `telefono`, `direccion` y `ciudad`. Incluye métodos para validar integridad básica y convertir a diccionario.

### controllers.py
Lógica de negocio. Actúa como intermediario entre la vista y la base de datos. Contiene:
- Validaciones de campos obligatorios y formato de correo electrónico.
- Coordinación de operaciones CRUD delegando en `database.py`.
- Métodos de búsqueda de clientes.

### views/main_window.py
Interfaz gráfica con Tkinter y ttk. Incluye:
- Ventana principal con título personalizado.
- Barra de menú de navegación (Archivo, Clientes, Ayuda).
- Barra de herramientas con botones: Agregar, Modificar, Eliminar, Limpiar, Refrescar.
- Formulario de entrada de datos del cliente.
- Tabla de datos (`ttk.Treeview`) con scrollbar.
- Campo de búsqueda y filtrado en tiempo real.
- Mensajes de confirmación, advertencia y error.
- Validaciones antes de guardar información.
- Doble clic en una fila para cargar el cliente en el formulario.

### views/__init__.py
Archivo que convierte a `views` en un paquete de Python.

## Flujo de uso

1. Ejecuta `python main.py`.
2. Completa el formulario (Nombre y Email son obligatorios) y presiona **Agregar**.
3. El registro se guarda en SQLite y se muestra automáticamente en la tabla.
4. Para editar, haz doble clic en una fila de la tabla, modifica los campos y presiona **Modificar**.
5. Para eliminar, selecciona un cliente y presiona **Eliminar** (se pide confirmación).
6. Usa el campo **Buscar** para filtrar registros por nombre, email o ciudad.
7. Los datos persisten aunque se cierre la aplicación (se almacenan en `database/app.db`).
