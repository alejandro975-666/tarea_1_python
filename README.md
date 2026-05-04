# 🏎️ Inventario de F1 en Python

Aplicación de consola para gestionar un inventario de pilotos de Fórmula 1. Permite añadir, buscar, modificar y eliminar pilotos, con persistencia en JSON y registro de actividad en un archivo de log.

---

## 📋 Requisitos

- Python 3.x
- Sin dependencias externas (solo librerías estándar: `json`, `logging`, `os`)

---

## 🚀 Instalación y uso

1. Clona o descarga el repositorio.
2. Ejecuta el script principal:

```bash
python gestor_pilotos_f1.py
```

3. Navega por el menú interactivo con las opciones numeradas.

---

## 📁 Archivos generados

| Archivo | Descripción |
|---|---|
| `inventario_f1.json` | Base de datos con los pilotos guardados |
| `inventario_f1.log` | Registro de todas las operaciones realizadas |

---

## 🗂️ Estructura del proyecto

```
gestor_pilotos_f1/
├── gestor_pilotos_f1.py      # Script principal
├── inventario_f1.json        # Datos persistentes (se genera automáticamente)
├── inventario_f1.log         # Log de actividad (se genera automáticamente)
└── README.md
```

---

## ⚙️ Funcionalidades

### Menú principal

```
=============================
   MENÚ DEL INVENTARIO F1
=============================
1. Añadir piloto
2. Buscar piloto
3. Modificar piloto
4. Eliminar piloto
5. Mostrar todos los pilotos
6. Búsqueda avanzada
7. Salir
```

### Descripción de cada opción

**1. Añadir piloto** — Registra un nuevo piloto introduciendo ID único, nombre, equipo, nacionalidad, palmarés y categorías. El ID debe ser numérico y no puede repetirse.

**2. Buscar piloto** — Localiza un piloto por su ID y muestra sus datos en pantalla.

**3. Modificar piloto** — Permite editar el nombre, equipo, nacionalidad, palmarés y/o categoría de un piloto existente. Los campos que se dejen en blanco mantienen su valor anterior.

**4. Eliminar piloto** — Elimina permanentemente un piloto del inventario a partir de su ID.

**5. Mostrar todos** — Lista todos los pilotos registrados en el inventario.

**6. Búsqueda avanzada** — Permite filtrar pilotos por nombre, equipo o nacionalidad.

**7. Salir** — Guarda el inventario y cierra la aplicación.

---

## 🔍 Menú de búsqueda avanzada

```
=============================
   MENÚ DE BÚSQUEDA AVANZADA
=============================
1. Buscar por nombre
2. Buscar por equipo
3. Buscar por nacionalidad
```

Permite localizar uno o varios pilotos usando criterios distintos al ID. La búsqueda no distingue entre mayúsculas y minúsculas.

---

## 🧱 Arquitectura del código

### Clase `Piloto`

Representa a un piloto con los atributos `piloto_id`, `nombre`, `equipo`, `nacionalidad`, `palmares` y `categoria`.

| Método | Descripción |
|---|---|
| `__init__(piloto_id, nombre, equipo, nacionalidad, palmares, categoria)` | Constructor. Inicializa los seis atributos del piloto. |
| `to_dict()` | Convierte el objeto `Piloto` a un diccionario Python, necesario para serializar los datos a JSON antes de guardarlos. |
| `mostrar()` | Imprime por consola los datos del piloto en un formato legible. |

### Clase `Inventario`

Gestiona la colección completa de pilotos y la persistencia de datos.

| Método | Descripción |
|---|---|
| `__init__()` | Constructor. Inicializa la lista interna `pilotos` vacía. |
| `cargar()` | Lee el archivo `inventario_f1.json` y reconstruye la lista de objetos `Piloto`. Si el archivo no existe, arranca con la lista vacía. |
| `guardar()` | Serializa la lista de pilotos a JSON y la escribe en `inventario_f1.json`. |
| `id_existe(piloto_id)` | Devuelve `True` si ya hay un piloto registrado con ese ID, para evitar duplicados al insertar. |
| `buscar_por_id(piloto_id)` | Recorre la lista y devuelve el objeto `Piloto` cuyo ID coincide, o `None` si no existe. |
| `piloto_con_mas_titulos()` | Devuelve el piloto con mayor número de títulos según su palmarés. |
| `buscar_por_nombre(nombre)` | Devuelve una lista de pilotos cuyo nombre contiene el texto introducido. |
| `buscar_por_equipos(equipo)` | Devuelve una lista de pilotos que pertenecen o han pertenecido al equipo indicado. |
| `buscar_por_nacionalidad(nacionalidad)` | Devuelve una lista de pilotos con la nacionalidad indicada. |

### Funciones del menú

| Función | Descripción |
|---|---|
| `insertar_piloto(inventario)` | Solicita al usuario los datos de un nuevo piloto (ID, nombre, equipo, nacionalidad, palmarés y categoría), valida que el ID no esté repetido y que el nombre no esté vacío, y lo añade al inventario guardando los cambios. |
| `buscar_piloto(inventario)` | Pide un ID al usuario y, si existe, muestra los datos del piloto correspondiente. Registra en el log si la búsqueda tiene éxito o falla. |
| `modificar_piloto(inventario)` | Localiza un piloto por ID y permite actualizar su nombre, equipo, nacionalidad, palmarés y/o categoría. Los campos que se dejen en blanco no se modifican. Guarda los cambios al finalizar. |
| `eliminar_piloto(inventario)` | Busca un piloto por ID y lo elimina permanentemente de la lista, actualizando el archivo JSON. |
| `mostrar_todos(inventario)` | Recorre la lista de pilotos y llama a `mostrar()` sobre cada uno. Si el inventario está vacío, muestra un mensaje informativo. |
| `mostrar_estadisticas(inventario)` | Muestra estadísticas del inventario, como el piloto con más títulos registrados. |
| `busqueda_avanzada(inventario)` | Presenta un submenú para buscar pilotos por nombre, equipo o nacionalidad y muestra los resultados encontrados. |
| `menu()` | Función principal. Carga el inventario al arrancar y presenta el menú en bucle hasta que el usuario elige salir. Gestiona la navegación entre todas las opciones. |

---

## 📝 Formato de datos (JSON)

Cada piloto se almacena con la siguiente estructura:

```json
[
    {
        "id": 1,
        "nombre": "Max Verstappen",
        "equipo": "Red Bull",
        "nacionalidad": "Neerlandesa",
        "palmares": "4 Títulos Mundiales, 62 victorias",
        "categoria": "Fórmula 1"
    }
]
```

---

## 📌 Notas
   - Si el archivo JSON no existe al iniciar, la aplicación arranca con el inventario vacío.
   - Todas las operaciones quedan registradas en el log con fecha, hora y nivel de severidad.
