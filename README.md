# Registro de ventas semiautomático (v1.0)

**Proyecto de muestra** para demostrar buenas prácticas en Python: la **v1.0** es un registro semiautomático de ventas que calcula base, IVA y totales, y exporta a Excel con fecha y hora. La **v2.0** evoluciona a gestor de inventario con persistencia en SQLite y análisis con pandas.

> He utilizado un asistente de IA como apoyo para resolver dudas puntuales; el diseño, la lógica y la escritura del código son míos y cada línea está comprendida.

## 1. Estructura del proyecto

La estructura es relativa, de modo que funciona independientemente del sistema operativo. Cada funcionalidad vive en su propio módulo, y el flujo principal se orquesta en `main.py`.

# Estructura del proyecto (v1.0)

registro_de_ventas_semiauto/
├── tools/
│ ├── __init__.py
│ ├── func_center.py # Lógica principal (clase Producto, funciones)
│ └── logs/
│ ├── __init__.py
│ └── logs_func.py # Configuración de logging
├── data/ # Archivos Excel generados (no versionado)
├── log/ # Archivos de log (no versionado)
├── examples/ # Ejemplos de salida (Excel y log)
├── tests/
│ ├── __init__.py
│ └── test_code.py # Tests unitarios
├── main.py # Punto de entrada
├── README.md # Este archivo
└── requirements.txt # Dependencias

## 2. Qué problema resuelve la v1.0

La v1.0 facilita el **ingreso manual de datos** de ventas con una estructura ordenada y un cómputo global. Los datos se guardan en un Excel con nombre `ventas_AAAA-MM-DD_HH-MM-SS.xlsx`, de modo que se sabe cuándo se creó. El sistema de logs registra cada acción en un archivo `.log`, lo que permite tener constancia de lo ocurrido.

**Importante**: la v1.0 es un **registro**, no un gestor. El Excel es la salida, no la fuente de verdad: el código no lee ni modifica el Excel generado. La v2.0 migrará a SQLite para que la persistencia sea real y el programa pueda consultar, actualizar y analizar.

## 3. Tecnologías

### 1.0 (actual)
- **Python 3.10+**: Lenguaje principal.
- **openpyxl**: Generación de archivos Excel.
- **pathlib**: Gestión de rutas multiplataforma.
- **logging**: Sistema de registro de eventos con rotación.
- **unittest**: Pruebas unitarias.

### 2.0 (planificada)
- **SQLite**: Persistencia real.
- **pandas**: Análisis de datos y estadísticas.
- **matplotlib**: Gráficas y visualización.

## 4. Instalación y uso

**Requisitos: Python 3.10 o superior.**

1. Clona el repositorio:
    ```bash
    git clone https://github.com/zztx07/registro_de_ventas_semiauto.git
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta el programa:
    ```bash
    python main.py
    ```
    
## 5. Ejemplo de salida

En la carpeta examples/ puedes ver un Excel generado por el programa y el fragmento de un log de ejecución real.

## Limitaciones y decisiones de diseño

- Logs: en esta versión se escriben en log/ con permisos por defecto del sistema. En un entorno real, deberían estar fuera del proyecto, con permisos restringidos, y el acceso mediado por un servicio de autenticación. Esta capa es infraestructura, no lógica de negocio, y se documenta como decisión consciente.

- Persistencia: el Excel es una salida, no una fuente de verdad. La v2.0 migra a SQLite para evitar problemas de concurrencia, formato e integridad.

- Encoding: en la v2.0, al leer CSV o JSON, se especificará encoding="utf-8" para evitar problemas con acentos en Windows.

## 7. Roadmap

- v1.0 — Registro semiautomático de ventas con Excel, logging y tests. ✅

- v2.0 (en desarrollo) — Persistencia con SQLite, análisis con pandas, gráficas con matplotlib y logging con handlers (File + Stream + Null). 🚧