# python-db-generator

Herramienta CLI en Python para generar bases de datos PostgreSQL automáticamente.
Define tus tablas en un archivo YAML y el programa genera el esquema SQL completo,
listo para ejecutar en PostgreSQL.

---

## Inicio rápido

```bash
git clone https://github.com/tuusuario/python-db-generator.git
cd python-db-generator
pip install -r requirements.txt
cp .env.example .env
```

```bash
# Ver el SQL en consola
python main.py generate example_schema.yaml --preview

# Guardar en output/
python main.py generate example_schema.yaml
```

---

## Ejemplo

Defines tu base de datos en YAML:

```yaml
name: tienda

tables:
  - name: usuarios
    columns:
      - name: id
        type: SERIAL
        primary_key: true
      - name: email
        type: VARCHAR
        length: 150
        nullable: false
        unique: true
    indexes:
      - email
```

Y obtienes SQL listo para PostgreSQL:

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
```

---

## Características

- Genera `CREATE TABLE` con tipos, constraints e índices
- Soporte para `FOREIGN KEY` con acciones `CASCADE`, `RESTRICT`, `SET NULL`
- Validación del YAML con mensajes de error claros
- Exporta el SQL a archivo `.sql`
- Preview en consola con sintaxis coloreada
- CLI intuitiva con `--preview` y `--output`

---

## Tipos soportados

`SERIAL` `BIGSERIAL` `INTEGER` `BIGINT` `VARCHAR` `TEXT`
`BOOLEAN` `DATE` `TIMESTAMP` `FLOAT` `NUMERIC` `UUID`

---

## Documentación

- [Guía de uso](docs/usage.md) — comandos, opciones y referencia completa
- [Ejemplos](docs/examples.md) — YAMLs de ejemplo con su SQL generado
- [Contribuir](docs/contributing.md) — cómo contribuir al proyecto
- [Arquitectura](architecture.md) — diseño interno del proyecto
- [Roadmap](PLAN.md) — estado y fases de desarrollo
- [Decisiones](decisions.md) — registro de decisiones técnicas
- [Changelog](CHANGELOG.md) — historial de cambios

---

## Stack

- Python 3.13
- PostgreSQL
- click — CLI
- rich — output en consola
- PyYAML — parseo de definiciones
- pytest — testing
- python-dotenv — variables de entorno

---

## Tests

```bash
pytest tests/ -v
```

---

## Estado del proyecto

🟢 Fase 4 completada — Documentación lista

---

## Licencia

MIT
