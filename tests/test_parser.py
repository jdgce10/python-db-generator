"""
Tests del parser.
Cubre parseo correcto, archivos inválidos y errores de formato.
"""

import pytest
from pathlib import Path
from src.services.parser import parse_yaml_file, ParserError
from src.models.schema import ColumnType, OnDeleteAction


# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────

def write_temp_yaml(tmp_path: Path, content: str, filename: str = "schema.yaml") -> Path:
    """Escribe un archivo YAML temporal para testing."""
    file = tmp_path / filename
    file.write_text(content, encoding="utf-8")
    return file


# ─────────────────────────────────────────
# Parseo correcto
# ─────────────────────────────────────────

class TestParseValid:

    def test_schema_simple(self, tmp_path: Path) -> None:
        yaml = """
name: mi_db
tables:
  - name: usuarios
    columns:
      - name: id
        type: SERIAL
        primary_key: true
      - name: email
        type: VARCHAR
        nullable: false
"""
        path = write_temp_yaml(tmp_path, yaml)
        schema = parse_yaml_file(path)

        assert schema.name == "mi_db"
        assert len(schema.tables) == 1
        assert schema.tables[0].name == "usuarios"

    def test_columna_primary_key(self, tmp_path: Path) -> None:
        yaml = """
name: db
tables:
  - name: t
    columns:
      - name: id
        type: SERIAL
        primary_key: true
"""
        path = write_temp_yaml(tmp_path, yaml)
        schema = parse_yaml_file(path)

        col = schema.tables[0].get_primary_key()
        assert col is not None
        assert col.name == "id"
        assert col.nullable is False

    def test_columna_varchar_con_length(self, tmp_path: Path) -> None:
        yaml = """
name: db
tables:
  - name: t
    columns:
      - name: nombre
        type: VARCHAR
        length: 200
"""
        path = write_temp_yaml(tmp_path, yaml)
        schema = parse_yaml_file(path)

        col = schema.tables[0].columns[0]
        assert col.type == ColumnType.VARCHAR
        assert col.length == 200

    def test_foreign_key_parseada(self, tmp_path: Path) -> None:
        yaml = """
name: db
tables:
  - name: usuarios
    columns:
      - name: id
        type: SERIAL
        primary_key: true
  - name: pedidos
    columns:
      - name: id
        type: SERIAL
        primary_key: true
      - name: usuario_id
        type: INTEGER
    foreign_keys:
      - column: usuario_id
        references_table: usuarios
        references_column: id
        on_delete: CASCADE
"""
        path = write_temp_yaml(tmp_path, yaml)
        schema = parse_yaml_file(path)

        pedidos = schema.get_table("pedidos")
        assert pedidos is not None
        assert len(pedidos.foreign_keys) == 1
        fk = pedidos.foreign_keys[0]
        assert fk.column == "usuario_id"
        assert fk.references_table == "usuarios"
        assert fk.on_delete == OnDeleteAction.CASCADE

    def test_indexes_parseados(self, tmp_path: Path) -> None:
        yaml = """
name: db
tables:
  - name: t
    columns:
      - name: id
        type: SERIAL
        primary_key: true
      - name: email
        type: VARCHAR
    indexes:
      - email
"""
        path = write_temp_yaml(tmp_path, yaml)
        schema = parse_yaml_file(path)

        assert "email" in schema.tables[0].indexes

    def test_multiples_tablas(self, tmp_path: Path) -> None:
        yaml = """
name: db
tables:
  - name: tabla_a
    columns:
      - name: id
        type: SERIAL
  - name: tabla_b
    columns:
      - name: id
        type: SERIAL
  - name: tabla_c
    columns:
      - name: id
        type: SERIAL
"""
        path = write_temp_yaml(tmp_path, yaml)
        schema = parse_yaml_file(path)

        assert len(schema.tables) == 3
        assert schema.table_names() == ["tabla_a", "tabla_b", "tabla_c"]


# ─────────────────────────────────────────
# Errores de archivo
# ─────────────────────────────────────────

class TestParseFileErrors:

    def test_archivo_no_existe(self) -> None:
        with pytest.raises(ParserError, match="no encontrado"):
            parse_yaml_file("no_existe.yaml")

    def test_extension_invalida(self, tmp_path: Path) -> None:
        file = tmp_path / "schema.json"
        file.write_text("{}", encoding="utf-8")
        with pytest.raises(ParserError, match=".yaml"):

            parse_yaml_file(file)

    def test_yaml_malformado(self, tmp_path: Path) -> None:
        file = tmp_path / "schema.yaml"
        file.write_text("esto: no: es: yaml: valido:::", encoding="utf-8")
        with pytest.raises(ParserError):
            parse_yaml_file(file)

    def test_yaml_vacio(self, tmp_path: Path) -> None:
        path = write_temp_yaml(tmp_path, "")
        with pytest.raises(ParserError):
            parse_yaml_file(path)


# ─────────────────────────────────────────
# Errores de validación propagados
# ─────────────────────────────────────────

class TestParseValidationErrors:

    def test_tipo_invalido_propagado(self, tmp_path: Path) -> None:
        yaml = """
name: db
tables:
  - name: t
    columns:
      - name: id
        type: INVENTADO
"""
        path = write_temp_yaml(tmp_path, yaml)
        with pytest.raises(ParserError, match="validación"):
            parse_yaml_file(path)

    def test_tabla_duplicada_propagada(self, tmp_path: Path) -> None:
        yaml = """
name: db
tables:
  - name: t
    columns:
      - name: id
        type: SERIAL
  - name: t
    columns:
      - name: id
        type: SERIAL
"""
        path = write_temp_yaml(tmp_path, yaml)
        with pytest.raises(ParserError, match="validación"):
            parse_yaml_file(path)
