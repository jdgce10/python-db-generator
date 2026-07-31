"""
Generador de SQL.
Convierte modelos internos en sentencias SQL para PostgreSQL.
"""

from __future__ import annotations
from pathlib import Path

from src.models.schema import (
    ColumnModel,
    ColumnType,
    ForeignKeyModel,
    SchemaModel,
    TableModel,
)


class GeneratorError(Exception):
    """Error durante la generación de SQL."""
    pass


def generate_sql(schema: SchemaModel) -> str:
    """
    Genera el SQL completo para un SchemaModel.

    Args:
        schema: El modelo del schema a generar.

    Returns:
        String con el SQL completo listo para ejecutar.
    """
    parts: list[str] = []

    parts.append(f"-- Schema: {schema.name}")
    parts.append(f"-- Generado por python-db-generator\n")

    for table in schema.tables:
        parts.append(_generate_table(table))

    for table in schema.tables:
        if table.indexes:
            parts.append(_generate_indexes(table))

    return "\n".join(parts)


def export_sql_file(schema: SchemaModel, output_dir: str | Path) -> Path:
    """
    Genera el SQL y lo exporta a un archivo .sql en output_dir.

    Args:
        schema: El modelo del schema.
        output_dir: Carpeta donde guardar el archivo.

    Returns:
        Path del archivo generado.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    sql = generate_sql(schema)
    file_path = output_path / f"{schema.name}.sql"

    file_path.write_text(sql, encoding="utf-8")
    return file_path


def _generate_table(table: TableModel) -> str:
    """Genera el CREATE TABLE para una tabla."""
    lines: list[str] = []

    lines.append(f"CREATE TABLE IF NOT EXISTS {table.name} (")

    column_lines = [_generate_column(col) for col in table.columns]

    if table.foreign_keys:
        fk_lines = [_generate_foreign_key_constraint(table.name, fk) for fk in table.foreign_keys]
        column_lines.extend(fk_lines)

    for i, line in enumerate(column_lines):
        comma = "," if i < len(column_lines) - 1 else ""
        lines.append(f"    {line}{comma}")

    lines.append(");\n")

    return "\n".join(lines)


def _generate_column(col: ColumnModel) -> str:
    """Genera la definición SQL de una columna."""
    col_type = _resolve_type(col)

    parts = [col.name, col_type]

    if col.primary_key:
        parts.append("PRIMARY KEY")

    if not col.nullable and not col.primary_key:
        parts.append("NOT NULL")

    if col.unique and not col.primary_key:
        parts.append("UNIQUE")

    if col.default is not None:
        parts.append(f"DEFAULT {col.default}")

    return " ".join(parts)


def _resolve_type(col: ColumnModel) -> str:
    """Resuelve el tipo SQL de una columna."""
    if col.type == ColumnType.VARCHAR:
        length = col.length or 255
        return f"VARCHAR({length})"

    if col.type == ColumnType.NUMERIC:
        return "NUMERIC(10, 2)"

    return col.type.value


def _generate_foreign_key_constraint(table_name: str, fk: ForeignKeyModel) -> str:
    """Genera la constraint FOREIGN KEY."""
    return (
        f"CONSTRAINT fk_{table_name}_{fk.column} "
        f"FOREIGN KEY ({fk.column}) "
        f"REFERENCES {fk.references_table}({fk.references_column}) "
        f"ON DELETE {fk.on_delete.value}"
    )


def _generate_indexes(table: TableModel) -> str:
    """Genera los CREATE INDEX para una tabla."""
    lines: list[str] = []

    for col_name in table.indexes:
        lines.append(
            f"CREATE INDEX IF NOT EXISTS idx_{table.name}_{col_name} "
            f"ON {table.name}({col_name});"
        )

    return "\n".join(lines) + "\n"
