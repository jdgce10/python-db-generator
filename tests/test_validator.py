"""
Tests del validador.
Cubre casos válidos, campos faltantes, tipos incorrectos y duplicados.
"""

import pytest
from src.services.validator import validate_schema, ValidationError


# ─────────────────────────────────────────
# Schema válido
# ─────────────────────────────────────────

class TestValidSchemas:

    def test_schema_minimo_valido(self, yaml_valido: dict) -> None:
        """Un schema bien formado no debe lanzar errores."""
        validate_schema(yaml_valido)

    def test_schema_con_foreign_key_valido(self, yaml_con_fk: dict) -> None:
        """Un schema con FK bien formada no debe lanzar errores."""
        validate_schema(yaml_con_fk)

    def test_schema_con_indexes_validos(self) -> None:
        data = {
            "name": "db",
            "tables": [
                {
                    "name": "productos",
                    "columns": [
                        {"name": "id", "type": "SERIAL", "primary_key": True},
                        {"name": "nombre", "type": "VARCHAR"},
                    ],
                    "indexes": ["nombre"],
                }
            ],
        }
        validate_schema(data)


# ─────────────────────────────────────────
# Campos requeridos faltantes
# ─────────────────────────────────────────

class TestMissingRequiredFields:

    def test_schema_sin_name(self) -> None:
        with pytest.raises(ValidationError, match="name"):
            validate_schema({"tables": [{"name": "x", "columns": [{"name": "id", "type": "SERIAL"}]}]})

    def test_schema_sin_tables(self) -> None:
        with pytest.raises(ValidationError, match="tables"):
            validate_schema({"name": "db"})

    def test_tabla_sin_columns(self) -> None:
        with pytest.raises(ValidationError):
            validate_schema({
                "name": "db",
                "tables": [{"name": "usuarios"}],
            })

    def test_columna_sin_type(self) -> None:
        with pytest.raises(ValidationError, match="type"):
            validate_schema({
                "name": "db",
                "tables": [
                    {"name": "t", "columns": [{"name": "id"}]}
                ],
            })

    def test_columna_sin_name(self) -> None:
        with pytest.raises(ValidationError, match="name"):
            validate_schema({
                "name": "db",
                "tables": [
                    {"name": "t", "columns": [{"type": "INTEGER"}]}
                ],
            })


# ─────────────────────────────────────────
# Tipos inválidos
# ─────────────────────────────────────────

class TestInvalidTypes:

    def test_tipo_columna_invalido(self) -> None:
        with pytest.raises(ValidationError, match="Tipo inválido"):
            validate_schema({
                "name": "db",
                "tables": [
                    {"name": "t", "columns": [{"name": "id", "type": "INVENTADO"}]}
                ],
            })

    def test_on_delete_invalido(self) -> None:
        """
        El schema incluye ambas tablas para que la validación de
        tabla referenciada pase y llegue a validar el on_delete.
        """
        with pytest.raises(ValidationError, match="on_delete"):
            validate_schema({
                "name": "db",
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
                            {"name": "usuario_id", "type": "INTEGER"},
                        ],
                        "foreign_keys": [
                            {
                                "column": "usuario_id",
                                "references_table": "usuarios",
                                "references_column": "id",
                                "on_delete": "INVENTADO",
                            }
                        ],
                    },
                ],
            })


# ─────────────────────────────────────────
# Duplicados
# ─────────────────────────────────────────

class TestDuplicates:

    def test_tablas_duplicadas(self) -> None:
        with pytest.raises(ValidationError, match="duplicada"):
            validate_schema({
                "name": "db",
                "tables": [
                    {"name": "usuarios", "columns": [{"name": "id", "type": "SERIAL"}]},
                    {"name": "usuarios", "columns": [{"name": "id", "type": "SERIAL"}]},
                ],
            })

    def test_columnas_duplicadas(self) -> None:
        with pytest.raises(ValidationError, match="duplicada"):
            validate_schema({
                "name": "db",
                "tables": [
                    {
                        "name": "t",
                        "columns": [
                            {"name": "id", "type": "SERIAL"},
                            {"name": "id", "type": "INTEGER"},
                        ],
                    }
                ],
            })


# ─────────────────────────────────────────
# Referencias inexistentes
# ─────────────────────────────────────────

class TestInvalidReferences:

    def test_fk_columna_inexistente(self) -> None:
        """
        La tabla referenciada existe pero la columna local no.
        Incluimos usuarios para que pase la validación de tabla.
        """
        with pytest.raises(ValidationError, match="inexistente"):
            validate_schema({
                "name": "db",
                "tables": [
                    {
                        "name": "usuarios",
                        "columns": [{"name": "id", "type": "SERIAL"}],
                    },
                    {
                        "name": "pedidos",
                        "columns": [{"name": "id", "type": "SERIAL"}],
                        "foreign_keys": [
                            {
                                "column": "no_existe",
                                "references_table": "usuarios",
                                "references_column": "id",
                            }
                        ],
                    },
                ],
            })

    def test_index_columna_inexistente(self) -> None:
        with pytest.raises(ValidationError, match="inexistente"):
            validate_schema({
                "name": "db",
                "tables": [
                    {
                        "name": "t",
                        "columns": [{"name": "id", "type": "SERIAL"}],
                        "indexes": ["no_existe"],
                    }
                ],
            })
