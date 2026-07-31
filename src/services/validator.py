"""
Validación de definiciones YAML antes de parsear.
Detecta errores y los reporta con mensajes claros.
"""

from __future__ import annotations
from typing import Any
from src.models.schema import ColumnType, OnDeleteAction


REQUIRED_SCHEMA_KEYS = {"name", "tables"}
REQUIRED_TABLE_KEYS = {"name", "columns"}
REQUIRED_COLUMN_KEYS = {"name", "type"}
VALID_COLUMN_TYPES = {t.value for t in ColumnType}
VALID_ON_DELETE = {a.value for a in OnDeleteAction}


class ValidationError(Exception):
    """Error de validación con mensaje descriptivo."""
    pass


def validate_schema(data: dict[str, Any]) -> None:
    """
    Valida la estructura completa del YAML de entrada.
    Lanza ValidationError si encuentra algún problema.
    """
    _check_required_keys(data, REQUIRED_SCHEMA_KEYS, context="schema")

    if not isinstance(data["name"], str) or not data["name"].strip():
        raise ValidationError("El nombre del schema debe ser un texto no vacío.")

    if not isinstance(data["tables"], list) or len(data["tables"]) == 0:
        raise ValidationError("El schema debe tener al menos una tabla.")

    table_names: list[str] = []

    for table in data["tables"]:
        _validate_table(table, table_names)
        table_names.append(table["name"])


def _validate_table(table: dict[str, Any], existing_tables: list[str]) -> None:
    """Valida una tabla individual."""
    _check_required_keys(table, REQUIRED_TABLE_KEYS, context="tabla")

    name = table["name"]

    if not isinstance(name, str) or not name.strip():
        raise ValidationError("El nombre de la tabla debe ser un texto no vacío.")

    if name in existing_tables:
        raise ValidationError(f"Tabla duplicada: '{name}'.")

    if not isinstance(table["columns"], list) or len(table["columns"]) == 0:
        raise ValidationError(f"La tabla '{name}' debe tener al menos una columna.")

    column_names: list[str] = []

    for column in table["columns"]:
        _validate_column(column, table_name=name, existing_columns=column_names)
        column_names.append(column["name"])

    if "foreign_keys" in table:
        for fk in table["foreign_keys"]:
            _validate_foreign_key(fk, table_name=name, column_names=column_names)

    if "indexes" in table:
        for index_col in table["indexes"]:
            if index_col not in column_names:
                raise ValidationError(
                    f"Índice en '{name}' referencia columna inexistente: '{index_col}'."
                )


def _validate_column(
    column: dict[str, Any],
    table_name: str,
    existing_columns: list[str],
) -> None:
    """Valida una columna individual."""
    _check_required_keys(column, REQUIRED_COLUMN_KEYS, context=f"columna en '{table_name}'")

    name = column["name"]

    if not isinstance(name, str) or not name.strip():
        raise ValidationError(f"Nombre de columna inválido en tabla '{table_name}'.")

    if name in existing_columns:
        raise ValidationError(f"Columna duplicada '{name}' en tabla '{table_name}'.")

    col_type = str(column["type"]).upper()
    if col_type not in VALID_COLUMN_TYPES:
        raise ValidationError(
            f"Tipo inválido '{col_type}' en columna '{name}' de tabla '{table_name}'. "
            f"Tipos válidos: {', '.join(sorted(VALID_COLUMN_TYPES))}."
        )


def _validate_foreign_key(
    fk: dict[str, Any],
    table_name: str,
    column_names: list[str],
) -> None:
    """Valida una clave foránea."""
    required = {"column", "references_table", "references_column"}
    _check_required_keys(fk, required, context=f"foreign_key en '{table_name}'")

    if fk["column"] not in column_names:
        raise ValidationError(
            f"Foreign key en '{table_name}' referencia columna inexistente: '{fk['column']}'."
        )

    if "on_delete" in fk:
        on_delete = str(fk["on_delete"]).upper()
        if on_delete not in VALID_ON_DELETE:
            raise ValidationError(
                f"on_delete inválido '{on_delete}' en '{table_name}'. "
                f"Valores válidos: {', '.join(VALID_ON_DELETE)}."
            )


def _check_required_keys(
    data: dict[str, Any],
    required: set[str],
    context: str,
) -> None:
    """Verifica que un dict tenga todas las claves requeridas."""
    missing = required - set(data.keys())
    if missing:
        raise ValidationError(
            f"Faltan campos requeridos en {context}: {', '.join(sorted(missing))}."
        )
