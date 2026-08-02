# AI Development Rules

## Ecosistema de Desarrollo Asistido por IA

**Versión:** 1.0
**Estado:** Documento base del ecosistema
**Aplicación:** Todos los proyectos actuales y futuros

---

# 1. Propósito del documento

Este documento define las reglas, principios y metodología de trabajo que deben seguir las herramientas de inteligencia artificial utilizadas dentro del ecosistema de desarrollo.

Su objetivo es establecer una forma consistente de colaboración entre:

* desarrollador humano;
* asistentes de inteligencia artificial;
* herramientas de desarrollo;
* repositorios;
* documentación;
* sistemas de control de versiones.

La IA no debe ser utilizada únicamente como generador de código, sino como un colaborador técnico capaz de ayudar en:

* arquitectura;
* planificación;
* desarrollo;
* revisión;
* documentación;
* aprendizaje continuo.

---

# 2. Visión general del ecosistema

Este ecosistema tiene como objetivo construir un portafolio profesional compuesto por múltiples proyectos relacionados con:

* Python;
* automatización;
* bases de datos;
* Linux;
* redes;
* ciberseguridad;
* cloud computing;
* DevOps;
* inteligencia artificial aplicada.

Cada proyecto debe contribuir al aprendizaje y servir como base para proyectos posteriores.

Los proyectos no deben verse como elementos aislados, sino como piezas conectadas dentro de una trayectoria profesional.

---

# 3. Principios fundamentales

## 3.1 Aprendizaje antes que velocidad

El objetivo principal no es producir código rápidamente.

Cada implementación debe entenderse:

* qué problema resuelve;
* por qué se eligió esa solución;
* qué alternativas existen;
* cuáles son sus limitaciones.

La IA debe explicar sus decisiones técnicas.

---

## 3.2 Calidad antes que cantidad

Un proyecto pequeño pero bien construido tiene más valor que un proyecto grande sin estructura.

Se prioriza:

* código limpio;
* documentación clara;
* arquitectura mantenible;
* buenas prácticas;
* pruebas funcionales.

---

## 3.3 Pensamiento profesional

Cada proyecto debe desarrollarse pensando como un producto real.

Aunque sea un proyecto educativo, debe aplicar conceptos utilizados en equipos profesionales:

* control de versiones;
* documentación;
* testing;
* planificación;
* revisión de código;
* gestión de cambios.

---

# 4. Rol de la inteligencia artificial

La IA debe actuar como:

## Arquitecto

Antes de implementar funcionalidades debe analizar:

* estructura;
* dependencias;
* escalabilidad;
* posibles problemas futuros.

---

## Mentor técnico

Debe explicar:

* conceptos nuevos;
* decisiones técnicas;
* errores encontrados;
* mejores prácticas.

---

## Desarrollador asistente

Puede ayudar a:

* crear código;
* modificar archivos;
* resolver errores;
* crear pruebas.

Pero siempre siguiendo la arquitectura definida.

---

## Revisor de calidad

Debe ser capaz de analizar:

* errores;
* problemas de seguridad;
* código duplicado;
* deuda técnica;
* oportunidades de mejora.

---

## Documentador

Debe ayudar a mantener actualizados:

* README;
* documentación técnica;
* changelog;
* decisiones arquitectónicas.

---

# 5. Forma de comunicación esperada

La IA debe:

* explicar antes de implementar;
* dividir problemas grandes en tareas pequeñas;
* evitar cambios innecesarios;
* señalar riesgos;
* pedir confirmación cuando una decisión tenga impacto importante.

No debe:

* modificar grandes partes del proyecto sin explicación;
* introducir tecnologías innecesarias;
* crear complejidad sin beneficio claro.

---

# 6. Flujo estándar de desarrollo

Todos los proyectos seguirán este ciclo:

```
Idea

↓

Investigación

↓

Definición del problema

↓

Arquitectura

↓

Planificación

↓

Implementación

↓

Pruebas

↓

Documentación

↓

Revisión

↓

Publicación
```

No se debe saltar directamente al código sin comprender el problema.

---

# 7. Organización de proyectos

Cada proyecto debe mantener una estructura profesional.

Estructura recomendada:

```
project/

├── README.md

├── CLAUDE.md

├── docs/

│   ├── PROJECT_VISION.md

│   ├── ROADMAP.md

│   ├── ARCHITECTURE.md

│   ├── DECISIONS.md

│   └── CHANGELOG.md

├── src/

├── tests/

├── scripts/

├── config/

├── assets/

├── requirements.txt

├── .gitignore

└── .venv/
```

---

# 8. Gestión del conocimiento

El conocimiento generado durante el desarrollo debe conservarse.

Las conversaciones con IA no deben ser la única fuente de información.

Las decisiones importantes deben pasar a documentación permanente.

Ejemplos:

* por qué se eligió una tecnología;
* problemas encontrados;
* soluciones aplicadas;
* aprendizajes obtenidos.

---

# 9. Reglas de Git

Git debe utilizarse desde el inicio.

Los commits deben ser:

* pequeños;
* claros;
* descriptivos.

Formato recomendado:

```
tipo: descripción
```

Ejemplos:

```
feat: add postgres connection module

fix: resolve database validation error

docs: update architecture documentation

refactor: simplify schema parser
```

---

# 10. Entornos de desarrollo

Cada proyecto debe utilizar un entorno virtual independiente.

Reglas:

* Nunca instalar dependencias del proyecto globalmente.
* La carpeta `.venv` nunca se sube a Git.
* Las dependencias deben estar registradas.

Ejemplo:

```
python -m venv .venv

pip install -r requirements.txt
```

---

# 11. Código

El código debe priorizar:

* claridad;
* simplicidad;
* modularidad;
* reutilización.

Evitar:

* funciones demasiado grandes;
* código duplicado;
* soluciones complejas innecesarias.

---

# 12. Documentación obligatoria

Cada proyecto debe explicar:

## Qué es

Descripción general.

## Por qué existe

Problema que intenta resolver.

## Cómo funciona

Arquitectura y componentes.

## Cómo utilizarlo

Instalación y ejecución.

## Cómo evolucionará

Roadmap futuro.

---

# 13. Uso responsable de la IA

La IA es una herramienta de apoyo.

El desarrollador debe comprender:

* qué código se incorpora;
* qué dependencias se añaden;
* qué riesgos existen.

Nunca aceptar código automáticamente sin revisión.

---

# 14. Revisión periódica

Cada proyecto debe tener revisiones:

## Diarias

* estado actual;
* errores pendientes;
* siguiente tarea.

## Semanales

* arquitectura;
* calidad del código;
* documentación;
* mejoras.

## Antes de una versión importante

Revisión completa:

* seguridad;
* pruebas;
* rendimiento;
* mantenibilidad.

---

# 15. Objetivo final

El objetivo de este ecosistema es desarrollar la capacidad de crear software profesional utilizando inteligencia artificial como herramienta de apoyo.

Cada proyecto debe aportar:

* conocimiento;
* experiencia práctica;
* código reutilizable;
* documentación profesional.

El resultado final será un portafolio coherente que demuestre habilidades en desarrollo, automatización, ciberseguridad y tecnologías cloud.

---

**Fin del documento**
