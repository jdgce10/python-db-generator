"""
Tests del generador de SQL.
Cubre generación de tablas, columnas, FK, índices y exportación.
"""

import pytest
from pathlib import Path
from src.models.schema import (
    ColumnModel,
    ColumnType,
    ForeignKeyModel,
    OnDeleteAction,
    SchemaModel,
    TableModel,
)
from src.services.generator import generate_sql, export_sql_file


# ─────────────────────────────────────────
# Generación de SQL básico
# ─────────────────────────────────────────

class TestGenerateSQL:

    def test_genera_create_table(self, schema_simple: SchemaModel) -> None:
        sql = generate_sql(schema_simple)
        assert "CREATE TABLE IF NOT EXISTS usuarios" in sql

    def test_incluye_nombre_schema_en_comentario(self, schema_simple: SchemaModel) -> None:
        sql = generate_sql(schema_simple)
        assert "-- Schema: test_db" in sql

    def test_genera_columna_primary_key(self, schema_simple: SchemaModel) -> None:
        sql = generate_sql(schema_simple)
        assert "id SERIAL PRIMARY KEY" in sql

    def test_genera_columna_not_null(self, schema_simple: SchemaModel) -> None:
        sql = generate_sql(schema_simple)
        assert "NOT NULL" in sql

    def test_genera_columna_unique(self, schema_simple: SchemaModel) -> None:
        sql = generate_sql(schema_simple)
        assert "UNIQUE" in sql

    def test_genera_varchar_con_length(self) -> None:
        col = ColumnModel(name="nombre", type=ColumnType.VARCHAR, length=150)
        table = TableModel(name="t", columns=[col])
        schema = SchemaModel(name="db", tables=[table])
        sql = generate_sql(schema)
        assert "VARCHAR(150)" in sql

    def test_varchar_sin_length_usa_255(self) -> None:
        col = ColumnModel(name="nombre", type=ColumnType.VARCHAR)
        table = TableModel(name="t", columns=[col])
        schema = SchemaModel(name="db", tables=[table])
        sql = generate_sql(schema)
        assert "VARCHAR(255)" in sql

    def test_genera_columna_con_default(self) -> None:
        col = ColumnModel(
            name="creado_en",
            type=ColumnType.TIMESTAMP,
            default="NOW()",
        )
        table = TableModel(name="t", columns=[col])
        schema = SchemaModel(name="db", tables=[table])
        sql = generate_sql(schema)
        assert "DEFAULT NOW()" in sql

    def test_genera_multiples_tablas(self, schema_completo: SchemaModel) -> None:
        sql = generate_sql(schema_completo)
        assert "CREATE TABLE IF NOT EXISTS usuarios" in sql
        assert "CREATE TABLE IF NOT EXISTS pedidos" in sql


# ─────────────────────────────────────────
# Foreign Keys
# ─────────────────────────────────────────

class TestForeignKeys:

    def test_genera_constraint_fk(self, schema_completo: SchemaModel) -> None:
        sql = generate_sql(schema_completo)
        assert "FOREIGN KEY (usuario_id)" in sql
        assert "REFERENCES usuarios(id)" in sql

    def test_fk_on_delete_cascade(self, schema_completo: SchemaModel) -> None:
        sql = generate_sql(schema_completo)
        assert "ON DELETE CASCADE" in sql

    def test_fk_on_delete_restrict(self) -> None:
        fk = ForeignKeyModel(
            column="cat_id",
            references_table="categorias",
            references_column="id",
            on_delete=OnDeleteAction.RESTRICT,
        )
        col_id = ColumnModel(name="id", type=ColumnType.SERIAL, primary_key=True)
        col_cat = ColumnModel(name="cat_id", type=ColumnType.INTEGER)
        table = TableModel(name="productos", columns=[col_id, col_cat], foreign_keys=[fk])
        schema = SchemaModel(name="db", tables=[table])
        sql = generate_sql(schema)
        assert "ON DELETE RESTRICT" in sql

    def test_nombre_constraint_fk(self, schema_completo: SchemaModel) -> None:
        sql = generate_sql(schema_completo)
        assert "fk_pedidos_usuario_id" in sql


# ─────────────────────────────────────────
# Índices
# ─────────────────────────────────────────

class TestIndexes:

    def test_genera_create_index(self, schema_simple: SchemaModel) -> None:
        sql = generate_sql(schema_simple)
        assert "CREATE INDEX IF NOT EXISTS" in sql
        assert "idx_usuarios_email" in sql

    def test_genera_multiples_indexes(self, schema_completo: SchemaModel) -> None:
        sql = generate_sql(schema_completo)
        assert "idx_usuarios_email" in sql
        assert "idx_pedidos_usuario_id" in sql

    def test_tabla_sin_indexes_no_genera_create_index(self) -> None:
        col = ColumnModel(name="id", type=ColumnType.SERIAL, primary_key=True)
        table = TableModel(name="t", columns=[col])
        schema = SchemaModel(name="db", tables=[table])
        sql = generate_sql(schema)
        assert "CREATE INDEX" not in sql


# ─────────────────────────────────────────
# Exportación a archivo
# ─────────────────────────────────────────

class TestExportSQLFile:

    def test_crea_archivo_sql(self, tmp_path: Path, schema_simple: SchemaModel) -> None:
        file_path = export_sql_file(schema_simple, tmp_path)
        assert file_path.exists()
        assert file_path.suffix == ".sql"

    def test_nombre_archivo_es_nombre_schema(self, tmp_path: Path, schema_simple: SchemaModel) -> None:
        file_path = export_sql_file(schema_simple, tmp_path)
        assert file_path.stem == schema_simple.name

    def test_contenido_archivo_es_sql_valido(self, tmp_path: Path, schema_simple: SchemaModel) -> None:
        file_path = export_sql_file(schema_simple, tmp_path)
        contenido = file_path.read_text(encoding="utf-8")
        assert "CREATE TABLE" in contenido

    def test_crea_carpeta_si_no_existe(self, tmp_path: Path, schema_simple: SchemaModel) -> None:
        output = tmp_path / "nueva_carpeta" / "sub"
        export_sql_file(schema_simple, output)
        assert output.exists()
