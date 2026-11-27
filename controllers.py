"""Capa de controladores - lógica de negocio.

Este módulo actúa como intermediario entre la interfaz gráfica (vistas)
y la capa de acceso a datos (database). Contiene las reglas de negocio,
validaciones de entrada y coordina las operaciones CRUD.
"""

from typing import List, Optional

from models import Cliente
import database


class ClienteController:
    """Controlador de clientes que encapsula la lógica de negocio.

    Attributes:
        None
    """

    def obtener_todos_los_clientes(self) -> List[Cliente]:
        """Retorna todos los clientes registrados ordenados por nombre."""
        return database.obtener_todos_los_clientes()

    def obtener_cliente_por_id(self, id_cliente: int) -> Optional[Cliente]:
        """Busca y retorna un cliente por su identificador.

        Args:
            id_cliente: ID del cliente a buscar.

        Returns:
            Objeto Cliente si existe, None en caso contrario.
        """
        return database.obtener_cliente_por_id(id_cliente)

    def buscar_clientes(self, termino: str) -> List[Cliente]:
        """Busca clientes que coincidan parcialmente con el término.

        La búsqueda se realiza sobre nombre, email y ciudad.

        Args:
            termino: Texto a buscar.

        Returns:
            Lista de clientes que coinciden con el término.
        """
        if not termino or not termino.strip():
            return self.obtener_todos_los_clientes()
        return database.buscar_clientes(termino.strip())

    def crear_cliente(self, cliente: Cliente) -> int:
        """Valida y registra un nuevo cliente.

        Args:
            cliente: Objeto Cliente con los datos a guardar (id_cliente debe ser None).

        Returns:
            El id_cliente asignado por la base de datos.

        Raises:
            ValueError: Si los datos no son válidos o el cliente ya tiene un ID.
        """
        self._validar_cliente(cliente)

        if cliente.id_cliente is not None:
            raise ValueError("No se puede crear un cliente que ya tiene un identificador.")

        return database.insertar_cliente(cliente)

    def actualizar_cliente(self, cliente: Cliente) -> bool:
        """Valida y actualiza un cliente existente.

        Args:
            cliente: Objeto Cliente con id_cliente y los nuevos valores.

        Returns:
            True si se actualizó al menos una fila.

        Raises:
            ValueError: Si los datos no son válidos o falta el id_cliente.
        """
        self._validar_cliente(cliente)

        if cliente.id_cliente is None:
            raise ValueError("Se requiere un id_cliente para actualizar un registro.")

        return database.actualizar_cliente(cliente)

    def eliminar_cliente(self, id_cliente: int) -> bool:
        """Elimina un cliente por su identificador.

        Args:
            id_cliente: ID del cliente a eliminar.

        Returns:
            True si se eliminó el cliente, False si no existía.
        """
        return database.eliminar_cliente(id_cliente)

    # ------------------------------------------------------------------ #
    # Validaciones
    # ------------------------------------------------------------------ #
    @staticmethod
    def _validar_cliente(cliente: Cliente) -> None:
        """Valida que los campos obligatorios del cliente estén completos.

        Args:
            cliente: Objeto Cliente a validar.

        Raises:
            ValueError: Si nombre o email están vacíos, o si el email
                no tiene un formato básico válido.
        """
        if not cliente.nombre:
            raise ValueError("El campo 'Nombre' es obligatorio.")

        if not cliente.email:
            raise ValueError("El campo 'Email' es obligatorio.")

        if "@" not in cliente.email or "." not in cliente.email.split("@")[-1]:
            raise ValueError("El correo electrónico no tiene un formato válido.")
