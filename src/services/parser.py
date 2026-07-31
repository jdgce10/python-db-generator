"""
Parser de archivos YAML.
Convierte la definición del usuario en modelos internos.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any

import yaml

from src.models.schema import (
    ColumnModel,
    ColumnType,
    ForeignKeyModel,
    OnDeleteAction,
    SchemaModel,
    TableModel,
)
from src.services.validator import validate_schema, ValidationError


class ParserError(Exception):
    """Error durante el parseo de un archivo YAML."""
    pass


def parse_yaml_file(path: str | Path) -> SchemaModel:
    """
    Lee un archivo YAML y retorna un SchemaModel validado.

    Args:
        path: Ruta al archivo YAML de definición.

    Returns:
        SchemaModel con todas las tablas y columnas.

    Raises:
        ParserError: Si el archivo no existe, no es YAML válido
                     o no pasa la validación.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise ParserError(f"Archivo no encontrado: {file_path}")

    if file_path.suffix not in {".yaml", ".yml"}:
        raise ParserError("El archivo debe tener extensión .yaml o .yml")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ParserError(f"Error al leer el YAML: {e}")

    if not isinstance(data, dict):
        raise ParserError("El archivo YAML debe contener un objeto en la raíz.")

    try:
        validate_schema(data)
    except ValidationError as e:
        raise ParserError(f"Error de validación: {e}")

    return _build_schema(data)


def _build_schema(data: dict[str, Any]) -> SchemaModel:
    """Construye un SchemaModel desde el dict del YAML."""
    tables = [_build_table(t) for t in data["tables"]]
    return SchemaModel(name=data["name"], tables=tables)


def _build_table(data: dict[str, Any]) -> TableModel:
    """Construye un TableModel desde el dict de una tabla."""
    columns = [_build_column(c) for c in data["columns"]]

    foreign_keys = [
        _build_foreign_key(fk)
        for fk in data.get("foreign_keys", [])
    ]

    indexes = data.get("indexes", [])

    return TableModel(
        name=data["name"],
        columns=columns,
        foreign_keys=foreign_keys,
        indexes=indexes,
    )


def _build_column(data: dict[str, Any]) -> ColumnModel:
    """Construye un ColumnModel desde el dict de una columna."""
    return ColumnModel(
        name=data["name"],
        type=ColumnType(str(data["type"]).upper()),
        primary_key=data.get("primary_key", False),
        nullable=data.get("nullable", True),
        unique=data.get("unique", False),
        default=data.get("default"),
        length=data.get("length"),
    )


def _build_foreign_key(data: dict[str, Any]) -> ForeignKeyModel:
    """Construye un ForeignKeyModel desde el dict de una FK."""
    on_delete_raw = str(data.get("on_delete", "RESTRICT")).upper()
    return ForeignKeyModel(
        column=data["column"],
        references_table=data["references_table"],
        references_column=data["references_column"],
        on_delete=OnDeleteAction(on_delete_raw),
    )
