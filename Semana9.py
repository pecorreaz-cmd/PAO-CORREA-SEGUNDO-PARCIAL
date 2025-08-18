# inventario.py
# ------------------------------------------------------------
# Sistema de Gestión de Inventarios (archivo único, sin librerías externas)
# ------------------------------------------------------------

from typing import List, Optional

class Producto:
    """Representa un producto del inventario."""

    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__id = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # Getters
    def get_id(self) -> int:
        return self.__id

    def get_nombre(self) -> str:
        return self.__nombre

    def get_cantidad(self) -> int:
        return self.__cantidad

    def get_precio(self) -> float:
        return self.__precio

    # Setters
    def set_nombre(self, nombre: str) -> None:
        self.__nombre = nombre

    def set_cantidad(self, cantidad: int) -> None:
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = cantidad

    def set_precio(self, precio: float) -> None:
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = precio

    def __str__(self) -> str:
        return (
            f"ID: {self.__id} | Nombre: {self.__nombre} | "
            f"Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"
        )

class Inventario:
    """Gestiona la colección d
