# 🏎️ Inventario de F1 en Python

Aplicación de consola para gestionar un inventario de pilotos de Fórmula 1. Permite añadir, buscar, modificar y eliminar pilotos, con persistencia en JSON y registro de actividad en un archivo de log.

---

## 💬 Nota del autor

> *Pedro, sé que antes el proyecto trataba sobre otro tema que consideré como algo de nicho y que era posible que no se entendiera muy bien si uno no sabe lo que es. Por eso he decidido cambiarlo a algo que creo que es más fácil de entender: un gestor de Pilotos de F1.*

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
├── inventario_f1.json    # Datos persistentes (se genera automáticamente)
├── inventario_f1.log     # Log de actividad (se genera automáticamente)
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
6. Salir
```

### Descripción de cada opción

**1. Añadir piloto** — Registra un nuevo piloto introduciendo ID único, nombre, equipo y nacionalidad. El ID debe ser numérico y no puede repetirse.

**2. Buscar piloto** — Localiza un piloto por su ID y muestra sus datos en pantalla.

**3. Modificar piloto** — Permite editar el nombre, equipo y/o nacionalidad de un piloto existente. Los campos que se dejen en blanco mantienen su valor anterior.

**4. Eliminar piloto** — Elimina permanentemente un piloto del inventario a partir de su ID.

**5. Mostrar todos** — Lista todos los pilotos registrados en el inventario.

**6. Salir** — Guarda el inventario y cierra la aplicación.

---

## 🧱 Arquitectura del código

### Clase `Piloto`

Representa a un piloto con los atributos `piloto_id`, `nombre`, `equipo` y `nacionalidad`.

| Método | Descripción |
|---|---|
| `__init__(piloto_id, nombre, equipo, nacionalidad)` | Constructor. Inicializa los cuatro atributos del piloto. |
| `to_dict()` | Convierte el objeto `Piloto` a un diccionario Python, necesario para poder serializar los datos a JSON antes de guardarlos. |
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

### Funciones del menú

| Función | Descripción |
|---|---|
| `insertar_piloto(inventario)` | Solicita al usuario los datos de un nuevo piloto (ID, nombre, equipo, nacionalidad), valida que el ID no esté repetido y que el nombre no esté vacío, y lo añade al inventario guardando los cambios. |
| `buscar_piloto(inventario)` | Pide un ID al usuario y, si existe, muestra los datos del piloto correspondiente. Registra en el log si la búsqueda tiene éxito o falla. |
| `modificar_piloto(inventario)` | Localiza un piloto por ID y permite actualizar su nombre, equipo y/o nacionalidad. Los campos que se dejen en blanco no se modifican. Guarda los cambios al finalizar. |
| `eliminar_piloto(inventario)` | Busca un piloto por ID y lo elimina permanentemente de la lista, actualizando el archivo JSON. |
| `mostrar_todos(inventario)` | Recorre la lista de pilotos y llama a `mostrar()` sobre cada uno. Si el inventario está vacío, muestra un mensaje informativo. |
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
        "nacionalidad": "Neerlandesa"
    }
]
```

---

## 📌 Notas

- Si el archivo JSON no existe al iniciar, la aplicación arranca con el inventario vacío.
- Todas las operaciones quedan registradas en el log con fecha, hora y nivel de severidad.
