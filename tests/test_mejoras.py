"""
Tests para las mejoras #2 y #4.

#2 — Validación de tabla referenciada en FK
#4 — Ordenación topológica de tablas por dependencias
"""

import pytest
from src.services.validator import validate_schema, ValidationError
from src.services.generator import generate_sql, CircularDependencyError
from src.models.schema import (
    ColumnModel,
    ColumnType,
    ForeignKeyModel,
    OnDeleteAction,
    SchemaModel,
    TableModel,
)


# ─────────────────────────────────────────
# MEJORA #2 — Validación de tabla referenciada
# ─────────────────────────────────────────

class TestFKTableValidation:

    def test_fk_tabla_referenciada_existe(self) -> None:
        """FK válida — la tabla referenciada existe en el schema."""
        validate_schema({
            "name": "db",
            "tables": [
                {
                    "name": "usuarios",
                    "columns": [{"name": "id", "type": "SERIAL", "primary_key": True}],
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
                        }
                    ],
                },
            ],
        })

    def test_fk_tabla_referenciada_no_existe(self) -> None:
        """FK inválida — la tabla referenciada no existe en el schema."""
        with pytest.raises(ValidationError, match="tabla inexistente"):
            validate_schema({
                "name": "db",
                "tables": [
                    {
                        "name": "pedidos",
                        "columns": [
                            {"name": "id", "type": "SERIAL", "primary_key": True},
                            {"name": "usuario_id", "type": "INTEGER"},
                        ],
                        "foreign_keys": [
                            {
                                "column": "usuario_id",
                                "references_table": "usuarrios",  # typo intencional
                                "references_column": "id",
                            }
                        ],
                    }
                ],
            })

    def test_fk_mensaje_incluye_tablas_disponibles(self) -> None:
        """El mensaje de error lista las tablas disponibles."""
        with pytest.raises(ValidationError, match="Tablas disponibles"):
            validate_schema({
                "name": "db",
                "tables": [
                    {
                        "name": "productos",
                        "columns": [
                            {"name": "id", "type": "SERIAL", "primary_key": True},
                            {"name": "cat_id", "type": "INTEGER"},
                        ],
                        "foreign_keys": [
                            {
                                "column": "cat_id",
                                "references_table": "no_existe",
                                "references_column": "id",
                            }
                        ],
                    }
                ],
            })

    def test_fk_referencia_a_si_misma_no_permitida_si_no_existe(self) -> None:
        """Una FK que referencia una tabla que está en el schema pasa ok."""
        validate_schema({
            "name": "db",
            "tables": [
                {
                    "name": "categorias",
                    "columns": [
                        {"name": "id", "type": "SERIAL", "primary_key": True},
                        {"name": "padre_id", "type": "INTEGER"},
                    ],
                    "foreign_keys": [
                        {
                            "column": "padre_id",
                            "references_table": "categorias",  # auto-referencia
                            "references_column": "id",
                        }
                    ],
                }
            ],
        })


# ─────────────────────────────────────────
# MEJORA #4 — Ordenación topológica
# ─────────────────────────────────────────

class TestTopologicalSort:

    def _make_table(self, name: str, fk_to: str | None = None) -> TableModel:
        """Helper para crear tablas de prueba rápidamente."""
        cols = [ColumnModel(name="id", type=ColumnType.SERIAL, primary_key=True)]
        fks = []

        if fk_to:
            cols.append(ColumnModel(name=f"{fk_to}_id", type=ColumnType.INTEGER))
            fks.append(ForeignKeyModel(
                column=f"{fk_to}_id",
                references_table=fk_to,
                references_column="id",
                on_delete=OnDeleteAction.RESTRICT,
            ))

        return TableModel(name=name, columns=cols, foreign_keys=fks)

    def test_tabla_referenciada_aparece_primero_en_sql(self) -> None:
        """usuarios debe aparecer antes que pedidos en el SQL."""
        pedidos = self._make_table("pedidos", fk_to="usuarios")
        usuarios = self._make_table("usuarios")

        # Orden invertido intencionalmente — pedidos primero en la lista
        schema = SchemaModel(name="db", tables=[pedidos, usuarios])
        sql = generate_sql(schema)

        pos_usuarios = sql.index("CREATE TABLE IF NOT EXISTS usuarios")
        pos_pedidos = sql.index("CREATE TABLE IF NOT EXISTS pedidos")

        assert pos_usuarios < pos_pedidos, (
            "usuarios debe crearse antes que pedidos"
        )

    def test_cadena_de_dependencias(self) -> None:
        """A → B → C: el SQL debe crearlas en orden C, B, A."""
        tabla_a = self._make_table("tabla_a", fk_to="tabla_b")
        tabla_b = self._make_table("tabla_b", fk_to="tabla_c")
        tabla_c = self._make_table("tabla_c")

        schema = SchemaModel(name="db", tables=[tabla_a, tabla_b, tabla_c])
        sql = generate_sql(schema)

        pos_a = sql.index("CREATE TABLE IF NOT EXISTS tabla_a")
        pos_b = sql.index("CREATE TABLE IF NOT EXISTS tabla_b")
        pos_c = sql.index("CREATE TABLE IF NOT EXISTS tabla_c")

        assert pos_c < pos_b < pos_a

    def test_tablas_sin_dependencias_orden_alfabetico(self) -> None:
        """Tablas sin FK deben salir en orden alfabético."""
        tabla_z = self._make_table("tabla_z")
        tabla_a = self._make_table("tabla_a")
        tabla_m = self._make_table("tabla_m")

        schema = SchemaModel(name="db", tables=[tabla_z, tabla_a, tabla_m])
        sql = generate_sql(schema)

        pos_a = sql.index("CREATE TABLE IF NOT EXISTS tabla_a")
        pos_m = sql.index("CREATE TABLE IF NOT EXISTS tabla_m")
        pos_z = sql.index("CREATE TABLE IF NOT EXISTS tabla_z")

        assert pos_a < pos_m < pos_z

    def test_dependencia_circular_lanza_error(self) -> None:
        """Dependencias circulares deben lanzar CircularDependencyError."""
        col_id = ColumnModel(name="id", type=ColumnType.SERIAL, primary_key=True)
        col_b_id = ColumnModel(name="b_id", type=ColumnType.INTEGER)
        col_a_id = ColumnModel(name="a_id", type=ColumnType.INTEGER)

        fk_a_to_b = ForeignKeyModel(
            column="b_id", references_table="tabla_b",
            references_column="id", on_delete=OnDeleteAction.RESTRICT,
        )
        fk_b_to_a = ForeignKeyModel(
            column="a_id", references_table="tabla_a",
            references_column="id", on_delete=OnDeleteAction.RESTRICT,
        )

        tabla_a = TableModel(name="tabla_a", columns=[col_id, col_b_id], foreign_keys=[fk_a_to_b])
        tabla_b = TableModel(name="tabla_b", columns=[col_id, col_a_id], foreign_keys=[fk_b_to_a])

        schema = SchemaModel(name="db", tables=[tabla_a, tabla_b])

        with pytest.raises(CircularDependencyError, match="circular"):
            generate_sql(schema)

    def test_multiples_fk_resueltas_correctamente(self) -> None:
        """Una tabla con FK a dos tablas distintas — ambas deben ir antes."""
        roles = self._make_table("roles")
        departamentos = self._make_table("departamentos")

        col_id = ColumnModel(name="id", type=ColumnType.SERIAL, primary_key=True)
        col_rol = ColumnModel(name="rol_id", type=ColumnType.INTEGER)
        col_dep = ColumnModel(name="dep_id", type=ColumnType.INTEGER)

        fk_rol = ForeignKeyModel(
            column="rol_id", references_table="roles",
            references_column="id", on_delete=OnDeleteAction.RESTRICT,
        )
        fk_dep = ForeignKeyModel(
            column="dep_id", references_table="departamentos",
            references_column="id", on_delete=OnDeleteAction.RESTRICT,
        )

        empleados = TableModel(
            name="empleados",
            columns=[col_id, col_rol, col_dep],
            foreign_keys=[fk_rol, fk_dep],
        )

        schema = SchemaModel(name="db", tables=[empleados, roles, departamentos])
        sql = generate_sql(schema)

        pos_empleados = sql.index("CREATE TABLE IF NOT EXISTS empleados")
        pos_roles = sql.index("CREATE TABLE IF NOT EXISTS roles")
        pos_dep = sql.index("CREATE TABLE IF NOT EXISTS departamentos")

        assert pos_roles < pos_empleados
        assert pos_dep < pos_empleados
