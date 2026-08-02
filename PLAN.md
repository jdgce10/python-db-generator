# Plan de Desarrollo — python-db-generator

## Qué es este proyecto

---

## Estado actual

- ✅ Estructura de carpetas creada
- ✅ Git inicializado
- ✅ .gitignore configurado
- ✅ LICENSE añadida
- ✅ CLAUDE.md definido
- ✅ decisions.md activo
- ✅ requirements.txt con dependencias base
- ✅ Arquitectura definida (capas: interfaz → lógica → datos)
- ✅ Decisión tomada: PostgreSQL
- ❌ src/ vacío — sin código
- ❌ config/ vacío
- ❌ scripts/ vacío
- ❌ tests/ vacío
- ❌ docs/ vacío
- ❌ README sin completar
- ❌ CHANGELOG vacío

---

## Fases

### FASE 1 — Completar base del proyecto ← AQUÍ ESTAMOS
- [ ] Completar README.md con descripción real del proyecto
- [ ] Crear config/settings.py — configuración de conexión a PostgreSQL
- [ ] Crear config/.env.example — variables de entorno de ejemplo
- [ ] Crear src/__init__.py
- [ ] Crear src/models/ — modelos de datos
- [ ] Crear src/database/ — conexión y manejo de PostgreSQL
- [ ] Crear src/utils/ — utilidades generales
- [ ] Actualizar CHANGELOG.md

### FASE 2 — Lógica principal
- [ ] Crear src/services/generator.py — lógica de generación de esquemas
- [ ] Crear src/services/parser.py — parseo de input del usuario
- [ ] Crear src/services/validator.py — validación de entradas
- [ ] Crear CLI principal con click (main.py o src/cli.py)
- [ ] Soporte para definir tablas desde YAML o JSON
- [ ] Generación de SQL (CREATE TABLE, relaciones, índices)
- [ ] Inserción de datos de prueba (fixtures)
- [ ] Exportar esquema a archivo .sql

### FASE 3 — Testing
- [ ] Crear tests/test_generator.py
- [ ] Crear tests/test_parser.py
- [ ] Crear tests/test_validator.py
- [ ] Crear tests/conftest.py con fixtures de pytest
- [ ] Cobertura mínima del 80%

### FASE 4 — Documentación
- [ ] Completar README con ejemplos reales de uso
- [ ] Crear docs/usage.md — guía de uso detallada
- [ ] Crear docs/examples.md — ejemplos con YAML de entrada y SQL de salida
- [ ] Crear docs/contributing.md — cómo contribuir
- [ ] Actualizar CHANGELOG con todas las versiones

### FASE 5 — Despliegue
- [ ] Empaquetar como herramienta instalable con pip
- [ ] Crear pyproject.toml
- [ ] Publicar en PyPI (opcional)
- [ ] Subir a GitHub con README completo

---

## Stack confirmado

- Python 3.13
- PostgreSQL
- click — interfaz CLI
- psycopg2 — conexión a PostgreSQL
- PyYAML — parseo de definiciones
- rich — output bonito en consola
- pytest — testing
- black + ruff — formateo y linting
- python-dotenv — variables de entorno

---

## Próxima sesión

Empezar por FASE 1:
1. config/settings.py
2. config/.env.example
3. src/database/connection.py
4. Actualizar README

Comando de commit al terminar fase 1:
git commit -m "feat: base del proyecto — config, conexión DB y estructura src"
