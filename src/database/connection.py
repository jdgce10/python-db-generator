"""
Manejo de conexión a PostgreSQL.
Pendiente de activar cuando PostgreSQL esté instalado.
"""

from __future__ import annotations
from typing import Optional


class DatabaseConnection:
    """
    Gestiona la conexión a PostgreSQL.
    Usa el patrón singleton para reutilizar la conexión.
    """

    _instance: Optional["DatabaseConnection"] = None

    def __init__(self) -> None:
        self._connection = None
        self._connected: bool = False

    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        """Retorna la instancia única de la conexión."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def connect(self) -> None:
        """
        Establece conexión con PostgreSQL.
        Activar cuando psycopg2 esté instalado.
        """
        # TODO: activar cuando PostgreSQL esté disponible
        #
        # from config.settings import DatabaseConfig
        # import psycopg2
        #
        # self._connection = psycopg2.connect(
        #     host=DatabaseConfig.HOST,
        #     port=DatabaseConfig.PORT,
        #     dbname=DatabaseConfig.NAME,
        #     user=DatabaseConfig.USER,
        #     password=DatabaseConfig.PASSWORD,
        # )
        # self._connected = True
        raise NotImplementedError("PostgreSQL aún no está configurado.")

    def disconnect(self) -> None:
        """Cierra la conexión activa."""
        if self._connection:
            self._connection.close()
            self._connected = False
            self._connection = None

    @property
    def is_connected(self) -> bool:
        return self._connected

    def execute(self, query: str, params: Optional[tuple] = None) -> None:
        """
        Ejecuta una query SQL.
        Pendiente de implementar.
        """
        # TODO: implementar cuando la conexión esté activa
        raise NotImplementedError("PostgreSQL aún no está configurado.")
