# CHANGELOG

## [0.3.0] — 2026-07-31

### Añadido
- docs/usage.md — guía completa de uso con referencia de tipos y propiedades
- docs/examples.md — 3 ejemplos reales con YAML de entrada y SQL de salida
- docs/contributing.md — guía de contribución con flujo de trabajo y convenciones
- README.md actualizado con inicio rápido, ejemplo inline y links a docs
- conftest.py en raíz y pytest.ini para resolución correcta de imports
- Fase 4 completada: documentación lista

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
