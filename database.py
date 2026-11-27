"""Capa de acceso a datos con SQLite.

Este módulo se encarga exclusivamente de la conexión con la base de datos
SQLite y de las operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
Todas las consultas son parametrizadas para prevenir inyecciones SQL.
"""

import os
import sqlite3
from typing import List, Optional

from models import Cliente

# Ruta del archivo de base de datos (se crea automáticamente si no existe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "app.db")

# Esquema de la tabla de clientes
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente    INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT    NOT NULL,
    email         TEXT    NOT NULL,
    telefono      TEXT,
    direccion     TEXT,
    ciudad        TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def obtener_conexion() -> sqlite3.Connection:
    """Abre (y crea si es necesario) la conexión a la base de datos SQLite.

    Returns:
        Objeto de conexión a SQLite.
    Raises:
        sqlite3.Error: Si ocurre un error al conectar.
    """
    # Asegurarse de que el directorio exista
    os.makedirs(DATABASE_DIR, exist_ok=True)

    conexion = sqlite3.connect(DATABASE_PATH)
    conexion.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_base_de_datos() -> None:
    """Crea las tablas necesarias al iniciar la aplicación si no existen."""
    try:
        with obtener_conexion() as conexion:
            conexion.execute(CREATE_TABLE_SQL)
            conexion.commit()
    except sqlite3.Error as error:
        raise RuntimeError(f"No se pudo inicializar la base de datos: {error}")


def insertar_cliente(cliente: Cliente) -> int:
    """Inserta un nuevo cliente en la base de datos.

    Args:
        cliente: Objeto Cliente con los datos a guardar.

    Returns:
        El id_cliente asignado por la base de datos.

    Raises:
        sqlite3.Error: Si ocurre un error al insertar.
    """
    sql = """
        INSERT INTO clientes (nombre, email, telefono, direccion, ciudad)
        VALUES (:nombre, :email, :telefono, :direccion, :ciudad)
    """
    with obtener_conexion() as conexion:
        cursor = conexion.execute(sql, cliente.to_dict())
        conexion.commit()
        return cursor.lastrowid


def obtener_todos_los_clientes() -> List[Cliente]:
    """Recupera todos los clientes ordenados por nombre.

    Returns:
        Lista de objetos Cliente.
    """
    sql = "SELECT id_cliente, nombre, email, telefono, direccion, ciudad FROM clientes ORDER BY nombre"
    with obtener_conexion() as conexion:
        cursor = conexion.execute(sql)
        filas = cursor.fetchall()
    return [_fila_a_cliente(fila) for fila in filas]


def obtener_cliente_por_id(id_cliente: int) -> Optional[Cliente]:
    """Busca un cliente por su identificador.

    Args:
        id_cliente: ID del cliente a buscar.

    Returns:
        Objeto Cliente si se encuentra, None en caso contrario.
    """
    sql = "SELECT id_cliente, nombre, email, telefono, direccion, ciudad FROM clientes WHERE id_cliente = ?"
    with obtener_conexion() as conexion:
        cursor = conexion.execute(sql, (id_cliente,))
        fila = cursor.fetchone()
    return _fila_a_cliente(fila) if fila else None


def buscar_clientes(termino: str) -> List[Cliente]:
    """Busca clientes cuyo nombre, email o ciudad coincidan con el término.

    Args:
        termino: Texto a buscar (búsqueda parcial, insensible a mayúsculas).

    Returns:
        Lista de objetos Cliente que coinciden.
    """
    like = f"%{termino}%"
    sql = """
        SELECT id_cliente, nombre, email, telefono, direccion, ciudad
        FROM clientes
        WHERE nombre LIKE ? OR email LIKE ? OR ciudad LIKE ?
        ORDER BY nombre
    """
    with obtener_conexion() as conexion:
        cursor = conexion.execute(sql, (like, like, like))
        filas = cursor.fetchall()
    return [_fila_a_cliente(fila) for fila in filas]


def actualizar_cliente(cliente: Cliente) -> bool:
    """Actualiza los datos de un cliente existente.

    Args:
        cliente: Objeto Cliente con id_cliente y los nuevos valores.

    Returns:
        True si se actualizó al menos una fila, False si no existe el cliente.

    Raises:
        ValueError: Si el cliente no tiene id_cliente definido.
    """
    if cliente.id_cliente is None:
        raise ValueError("No se puede actualizar un cliente sin id_cliente.")

    sql = """
        UPDATE clientes
        SET nombre = :nombre, email = :email, telefono = :telefono,
            direccion = :direccion, ciudad = :ciudad
        WHERE id_cliente = :id_cliente
    """
    datos = cliente.to_dict()
    datos["id_cliente"] = cliente.id_cliente

    with obtener_conexion() as conexion:
        cursor = conexion.execute(sql, datos)
        conexion.commit()
        return cursor.rowcount > 0


def eliminar_cliente(id_cliente: int) -> bool:
    """Elimina un cliente de la base de datos por su identificador.

    Args:
        id_cliente: ID del cliente a eliminar.

    Returns:
        True si se eliminó una fila, False si no existía.
    """
    sql = "DELETE FROM clientes WHERE id_cliente = ?"
    with obtener_conexion() as conexion:
        cursor = conexion.execute(sql, (id_cliente,))
        conexion.commit()
        return cursor.rowcount > 0


def _fila_a_cliente(fila: sqlite3.Row) -> Cliente:
    """Convierte una fila de la base de datos en un objeto Cliente."""
    return Cliente(
        id_cliente=fila["id_cliente"],
        nombre=fila["nombre"],
        email=fila["email"],
        telefono=fila["telefono"] or "",
        direccion=fila["direccion"] or "",
        ciudad=fila["ciudad"] or "",
    )
