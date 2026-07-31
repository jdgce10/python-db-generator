# Contribuir — python-db-generator

## Requisitos previos

- Python 3.13
- Git
- PostgreSQL (para pruebas de integración)

---

## Configuración del entorno

```bash
git clone https://github.com/tuusuario/python-db-generator.git
cd python-db-generator

python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
cp .env.example .env
```

---

## Ejecutar tests

```bash
pytest tests/ -v
```

---

## Estilo de código

Este proyecto sigue PEP8 con las siguientes herramientas:

```bash
# Formatear código
black .

# Linting
ruff check .
```

Reglas clave:
- Type hints en todas las funciones
- Variables con nombres descriptivos
- Comentarios solo cuando aporten valor real
- Una responsabilidad por archivo

---

## Flujo de trabajo

1. Crea una rama desde `main`
```bash
git checkout -b feat/nombre-de-la-feature
```

2. Escribe el código siguiendo el estilo del proyecto

3. Añade tests para la nueva funcionalidad

4. Ejecuta los tests y asegúrate que todo pasa
```bash
pytest tests/ -v
```

5. Formatea el código
```bash
black .
ruff check .
```

6. Haz commit con un mensaje descriptivo
```bash
git commit -m "feat: descripción clara de lo que hace"
```

7. Abre un Pull Request hacia `main`

---

## Convención de commits

| Prefijo | Cuándo usarlo |
|---|---|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de bug |
| `docs:` | Cambios en documentación |
| `test:` | Añadir o modificar tests |
| `refactor:` | Refactorización sin cambio de funcionalidad |
| `chore:` | Tareas de mantenimiento |

---

## Estructura del proyecto

```
python-db-generator/
├── config/          # Configuración y variables de entorno
├── src/
│   ├── cli.py       # Interfaz de línea de comandos
│   ├── database/    # Conexión y manejo de PostgreSQL
│   ├── services/    # Lógica principal (parser, validator, generator)
│   ├── models/      # Modelos de datos internos
│   └── utils/       # Utilidades generales
├── tests/           # Tests con pytest
├── docs/            # Documentación extendida
└── output/          # Archivos SQL generados (no se sube a Git)
```
