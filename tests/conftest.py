"""
Fixtures compartidos para todos los tests.
Datos reutilizables que evitan repetición entre archivos de test.
"""

import pytest
from src.models.schema import (
    ColumnModel,
    ColumnType,
    ForeignKeyModel,
    OnDeleteAction,
    SchemaModel,
    TableModel,
)


# ─────────────────────────────────────────
# Fixtures de columnas
# ─────────────────────────────────────────

@pytest.fixture
def col_id() -> ColumnModel:
    return ColumnModel(name="id", type=ColumnType.SERIAL, primary_key=True)


@pytest.fixture
def col_nombre() -> ColumnModel:
    return ColumnModel(name="nombre", type=ColumnType.VARCHAR, length=100, nullable=False)


@pytest.fixture
def col_email() -> ColumnModel:
    return ColumnModel(name="email", type=ColumnType.VARCHAR, length=150, nullable=False, unique=True)


@pytest.fixture
def col_usuario_id() -> ColumnModel:
    return ColumnModel(name="usuario_id", type=ColumnType.INTEGER, nullable=False)


# ─────────────────────────────────────────
# Fixtures de tablas
# ─────────────────────────────────────────

@pytest.fixture
def tabla_usuarios(col_id, col_nombre, col_email) -> TableModel:
    return TableModel(
        name="usuarios",
        columns=[col_id, col_nombre, col_email],
        indexes=["email"],
    )


@pytest.fixture
def tabla_pedidos(col_id, col_usuario_id) -> TableModel:
    fk = ForeignKeyModel(
        column="usuario_id",
        references_table="usuarios",
        references_column="id",
        on_delete=OnDeleteAction.CASCADE,
    )
    return TableModel(
        name="pedidos",
        columns=[col_id, col_usuario_id],
        foreign_keys=[fk],
        indexes=["usuario_id"],
    )


# ─────────────────────────────────────────
# Fixtures de schema
# ─────────────────────────────────────────

@pytest.fixture
def schema_simple(tabla_usuarios) -> SchemaModel:
    return SchemaModel(name="test_db", tables=[tabla_usuarios])


@pytest.fixture
def schema_completo(tabla_usuarios, tabla_pedidos) -> SchemaModel:
    return SchemaModel(name="tienda", tables=[tabla_usuarios, tabla_pedidos])


# ─────────────────────────────────────────
# Fixtures de datos YAML (dicts)
# ─────────────────────────────────────────

@pytest.fixture
def yaml_valido() -> dict:
    return {
        "name": "mi_db",
        "tables": [
            {
                "name": "usuarios",
                "columns": [
                    {"name": "id", "type": "SERIAL", "primary_key": True},
                    {"name": "email", "type": "VARCHAR", "nullable": False},
                ],
            }
        ],
    }


@pytest.fixture
def yaml_con_fk() -> dict:
    return {
        "name": "tienda",
        "tables": [
            {
                "name": "usuarios",
                "columns": [
                    {"name": "id", "type": "SERIAL", "primary_key": True},
                ],
            },
            {
                "name": "pedidos",
                "columns": [
                    {"name": "id", "type": "SERIAL", "primary_key": True},
                    {"name": "usuario_id", "type": "INTEGER", "nullable": False},
                ],
                "foreign_keys": [
                    {
                        "column": "usuario_id",
                        "references_table": "usuarios",
                        "references_column": "id",
                        "on_delete": "CASCADE",
                    }
                ],
            },
        ],
    }
