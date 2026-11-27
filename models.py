"""Modelos de datos de la aplicación.

Este módulo define las clases de representación de los datos que se
gestionan en la base de datos SQLite. Se utiliza una clase de datos
simple (dataclass) para mantener la estructura de un cliente.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    """Representa a un cliente registrado en el sistema.

    Attributes:
        id_cliente: Identificador único de la base de datos (None si aún no se guarda).
        nombre: Nombre completo del cliente.
        email: Correo electrónico del cliente.
        telefono: Número de teléfono del cliente.
        direccion: Dirección del cliente.
        ciudad: Ciudad del cliente.
    """

    id_cliente: Optional[int] = None
    nombre: str = ""
    email: str = ""
    telefono: str = ""
    direccion: str = ""
    ciudad: str = ""

    def esta_completo(self) -> bool:
        """Retorna True si los campos obligatorios tienen valor."""
        return bool(self.nombre.strip() and self.email.strip())

    def to_dict(self) -> dict:
        """Convierte la instancia en un diccionario (sin el id)."""
        return {
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
        }
