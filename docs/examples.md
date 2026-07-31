# Ejemplos — python-db-generator

Ejemplos reales de archivos YAML y el SQL que generan.

---

## Ejemplo 1 — Schema mínimo

**Entrada (`schema.yaml`):**

```yaml
name: blog

tables:
  - name: posts
    columns:
      - name: id
        type: SERIAL
        primary_key: true
      - name: titulo
        type: VARCHAR
        length: 200
        nullable: false
      - name: contenido
        type: TEXT
      - name: publicado_en
        type: TIMESTAMP
        default: "NOW()"
```

**SQL generado:**

```sql
-- Schema: blog
-- Generado por python-db-generator

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT,
    publicado_en TIMESTAMP DEFAULT NOW()
);
```

---

## Ejemplo 2 — Tablas con relaciones

**Entrada (`tienda.yaml`):**

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
      - name: nombre
        type: VARCHAR
        length: 100
    indexes:
      - email

  - name: productos
    columns:
      - name: id
        type: SERIAL
        primary_key: true
      - name: nombre
        type: VARCHAR
        length: 200
        nullable: false
      - name: precio
        type: NUMERIC
        nullable: false

  - name: pedidos
    columns:
      - name: id
        type: SERIAL
        primary_key: true
      - name: usuario_id
        type: INTEGER
        nullable: false
      - name: producto_id
        type: INTEGER
        nullable: false
      - name: cantidad
        type: INTEGER
        nullable: false
      - name: fecha
        type: TIMESTAMP
        default: "NOW()"
    foreign_keys:
      - column: usuario_id
        references_table: usuarios
        references_column: id
        on_delete: CASCADE
      - column: producto_id
        references_table: productos
        references_column: id
        on_delete: RESTRICT
    indexes:
      - usuario_id
      - producto_id
```

**SQL generado:**

```sql
-- Schema: tienda
-- Generado por python-db-generator

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,
    nombre VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_pedidos_usuario_id FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_pedidos_producto_id FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_pedidos_usuario_id ON pedidos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_pedidos_producto_id ON pedidos(producto_id);
```

---

## Ejemplo 3 — Sistema de usuarios con roles

```yaml
name: auth_system

tables:
  - name: roles
    columns:
      - name: id
        type: SERIAL
        primary_key: true
      - name: nombre
        type: VARCHAR
        length: 50
        nullable: false
        unique: true

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
      - name: password_hash
        type: TEXT
        nullable: false
      - name: rol_id
        type: INTEGER
        nullable: false
      - name: activo
        type: BOOLEAN
        default: "true"
      - name: creado_en
        type: TIMESTAMP
        default: "NOW()"
    foreign_keys:
      - column: rol_id
        references_table: roles
        references_column: id
        on_delete: RESTRICT
    indexes:
      - email
      - rol_id
```
