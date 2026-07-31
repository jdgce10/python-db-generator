# python-db-generator

Herramienta CLI en Python para generar bases de datos PostgreSQL automáticamente.
Define tus tablas en un archivo YAML y el programa genera el esquema SQL,
lo ejecuta, inserta datos de prueba y documenta todo.

---

## Estado del proyecto

🚧 En desarrollo activo — Fase 1

---

## Objetivos

- Generar esquemas PostgreSQL desde definiciones YAML
- Crear tablas, relaciones e índices automáticamente
- Insertar datos de prueba (fixtures)
- Exportar el esquema a archivo .sql
- Documentar la base de datos generada

---

## Tecnologías

- Python 3.13
- PostgreSQL
- click — interfaz CLI
- psycopg2 — conexión a PostgreSQL
- PyYAML — parseo de definiciones
- rich — output en consola
- pytest — testing
- python-dotenv — variables de entorno

---

## Instalación

```bash
git clone https://github.com/tuusuario/python-db-generator.git

cd python-db-generator

pip install -r requirements.txt

cp .env.example .env
# Edita .env con tus credenciales de PostgreSQL
```

---

## Uso

```bash
# Próximamente
python main.py generate --input schema.yaml
```

---

## Estructura

```
python-db-generator/
├── config/          # Configuración y variables de entorno
├── src/
│   ├── database/    # Conexión y manejo de PostgreSQL
│   ├── services/    # Lógica de generación
│   ├── models/      # Modelos de datos
│   └── utils/       # Utilidades generales
├── tests/           # Tests con pytest
├── docs/            # Documentación extendida
├── scripts/         # Scripts auxiliares
└── output/          # Esquemas y archivos generados
```

---

## Arquitectura

Ver: [architecture.md](architecture.md)

## Roadmap

Ver: [PLAN.md](PLAN.md)

## Decisiones técnicas

Ver: [decisions.md](decisions.md)

---

## Licencia

MIT
