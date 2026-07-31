# CHANGELOG

## [0.2.0] — 2026-07-31

### Añadido
- src/models/schema.py — modelos internos (ColumnModel, TableModel, SchemaModel, ForeignKeyModel)
- src/services/validator.py — validación completa de YAML con mensajes de error claros
- src/services/parser.py — parseo de YAML a modelos internos
- src/services/generator.py — generación de SQL (CREATE TABLE, FOREIGN KEY, INDEX)
- src/cli.py — interfaz CLI con click y rich
- main.py — punto de entrada del programa
- example_schema.yaml — ejemplo de uso con 3 tablas y relaciones
- Fase 2 completada: lógica principal funcional

## [0.1.0] — 2026-07-31

### Añadido
- Estructura completa de carpetas del proyecto
- config/settings.py — configuración de la app y PostgreSQL
- config/.env.example — plantilla de variables de entorno
- src/__init__.py y módulos base (database, services, models, utils)
- src/database/connection.py — clase DatabaseConnection con patrón singleton
- README.md completado con descripción real del proyecto
- PLAN.md — plan de desarrollo por fases con estado actual
- Fase 1 completada: base del proyecto lista
