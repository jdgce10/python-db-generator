"""
Modelos de datos internos del proyecto.
Representan la estructura de una base de datos antes de generar SQL.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ColumnType(str, Enum):
    """Tipos de columna soportados."""
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    SERIAL = "SERIAL"
    BIGSERIAL = "BIGSERIAL"
    VARCHAR = "VARCHAR"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIMESTAMP = "TIMESTAMP"
    FLOAT = "FLOAT"
    NUMERIC = "NUMERIC"
    UUID = "UUID"


class OnDeleteAction(str, Enum):
    """Acciones al eliminar un registro referenciado."""
    CASCADE = "CASCADE"
    SET_NULL = "SET NULL"
    RESTRICT = "RESTRICT"
    NO_ACTION = "NO ACTION"


@dataclass
class ColumnModel:
    """Representa una columna dentro de una tabla."""
    name: str
    type: ColumnType
    primary_key: bool = False
    nullable: bool = True
    unique: bool = False
    default: Optional[str] = None
    length: Optional[int] = None  # Para VARCHAR

    def __post_init__(self) -> None:
        if self.primary_key:
            self.nullable = False


@dataclass
class ForeignKeyModel:
    """Representa una clave foránea entre tablas."""
    column: str
    references_table: str
    references_column: str
    on_delete: OnDeleteAction = OnDeleteAction.RESTRICT


@dataclass
class TableModel:
    """Representa una tabla completa con sus columnas y relaciones."""
    name: str
    columns: list[ColumnModel] = field(default_factory=list)
    foreign_keys: list[ForeignKeyModel] = field(default_factory=list)
    indexes: list[str] = field(default_factory=list)  # Nombres de columnas a indexar

    def get_primary_key(self) -> Optional[ColumnModel]:
        """Retorna la columna primary key si existe."""
        for col in self.columns:
            if col.primary_key:
                return col
        return None

    def has_column(self, name: str) -> bool:
        """Verifica si una columna existe en la tabla."""
        return any(col.name == name for col in self.columns)


@dataclass
class SchemaModel:
    """Representa el esquema completo de una base de datos."""
    name: str
    tables: list[TableModel] = field(default_factory=list)

    def get_table(self, name: str) -> Optional[TableModel]:
        """Retorna una tabla por nombre."""
        for table in self.tables:
            if table.name == name:
                return table
        return None

    def table_names(self) -> list[str]:
        """Retorna los nombres de todas las tablas."""
        return [table.name for table in self.tables]
