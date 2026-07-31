# Guía de uso — python-db-generator

## Instalación

```bash
git clone https://github.com/tuusuario/python-db-generator.git
cd python-db-generator
pip install -r requirements.txt
cp .env.example .env
```

---

## Uso básico

```bash
# Ver el SQL generado en consola sin guardar
python main.py generate schema.yaml --preview

# Generar y guardar en output/
python main.py generate schema.yaml

# Guardar en una carpeta específica
python main.py generate schema.yaml --output mis_esquemas/

# Ver versión
python main.py version
```

---

## Estructura del archivo YAML

El archivo de entrada describe tu base de datos. Tiene tres secciones principales:

### 1. Nombre del schema

```yaml
name: nombre_de_tu_db
```

### 2. Tablas

```yaml
tables:
  - name: nombre_tabla
    columns: [...]
    foreign_keys: [...]   # opcional
    indexes: [...]        # opcional
```

### 3. Columnas

Cada columna requiere `name` y `type`. El resto es opcional.

```yaml
columns:
  - name: id
    type: SERIAL
    primary_key: true

  - name: email
    type: VARCHAR
    length: 150
    nullable: false
    unique: true

  - name: creado_en
    type: TIMESTAMP
    default: "NOW()"
```

### Tipos soportados

| Tipo | Descripción |
|---|---|
| `SERIAL` | Entero autoincremental (ideal para IDs) |
| `BIGSERIAL` | Entero autoincremental largo |
| `INTEGER` | Número entero |
| `BIGINT` | Número entero largo |
| `VARCHAR` | Texto con longitud máxima (usa `length`) |
| `TEXT` | Texto sin límite |
| `BOOLEAN` | Verdadero o falso |
| `DATE` | Fecha |
| `TIMESTAMP` | Fecha y hora |
| `FLOAT` | Número decimal |
| `NUMERIC` | Número decimal preciso (10,2) |
| `UUID` | Identificador único universal |

### Propiedades de columna

| Propiedad | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `name` | string | requerido | Nombre de la columna |
| `type` | string | requerido | Tipo de dato |
| `primary_key` | bool | false | Marca como clave primaria |
| `nullable` | bool | true | Permite valores nulos |
| `unique` | bool | false | Valores únicos |
| `default` | string | null | Valor por defecto |
| `length` | int | 255 | Longitud máxima (solo VARCHAR) |

---

## Foreign Keys

```yaml
foreign_keys:
  - column: usuario_id
    references_table: usuarios
    references_column: id
    on_delete: CASCADE
```

### Valores de on_delete

| Valor | Comportamiento |
|---|---|
| `RESTRICT` | Bloquea el borrado si hay registros relacionados (por defecto) |
| `CASCADE` | Borra los registros relacionados automáticamente |
| `SET NULL` | Pone NULL en la columna relacionada |
| `NO ACTION` | No hace nada (deja que la DB decida) |

---

## Índices

```yaml
indexes:
  - email
  - nombre
```

Genera un `CREATE INDEX` por cada columna listada.

---

## Archivo de salida

El SQL generado se guarda en `output/<nombre_schema>.sql` por defecto.

Ejemplo de salida para una tabla `usuarios`:

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
```
