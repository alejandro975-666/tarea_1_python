# ==========================================
#   INVENTARIO DE DARK SOULS 3 EN PYTHON
# ==========================================

import json
import logging
import os

ARCHIVO_JSON = "inventario_ds3.json"
ARCHIVO_LOG = "inventario.log"

# ------------------------------------------
# CONFIGURACIÓN DEL LOGGING
# ------------------------------------------

logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Aplicación iniciada.")

# ------------------------------------------
# INVENTARIO GLOBAL
# ------------------------------------------

inventario = []

# ------------------------------------------
# FUNCIONES JSON
# ------------------------------------------

def cargar_inventario():
    """Carga el inventario desde un archivo JSON."""
    global inventario

    if not os.path.exists(ARCHIVO_JSON):
        logging.warning("No existe archivo JSON. Se inicia inventario vacío.")
        return

    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            inventario = json.load(archivo)
            logging.info("Inventario cargado correctamente desde JSON.")
    except Exception as e:
        logging.error(f"Error cargando inventario: {e}")


def guardar_inventario():
    """Guarda el inventario en un archivo JSON."""
    try:
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
            json.dump(inventario, archivo, indent=4, ensure_ascii=False)
            logging.info("Inventario guardado correctamente en JSON.")
    except Exception as e:
        logging.error(f"Error guardando inventario: {e}")


# ---------------------------------------------------------
def insertar_elemento(datos):
    print("\n Añadir nuevo objeto al inventario")

    while True:
        try:
            item_id = int(input("ID del objeto: "))
            if any(item["id"] == item_id for item in datos):
                print("Ese ID ya existe.")
                continue
            break
        except ValueError:
            print("El ID debe ser un número.")

    nombre = input("Nombre del objeto: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre del objeto: ").strip()

    tipo = input("Tipo (arma, anillo, consumible...): ").strip()
    rareza = input("Rareza (común, raro, épico, legendario): ").strip()

    nuevo_item = {
        "id": item_id,
        "nombre": nombre,
        "tipo": tipo,
        "rareza": rareza
    }

    datos.append(nuevo_item)
    guardar_inventario()

    logging.info(f"Objeto añadido: {nuevo_item}")
    print("Objeto añadido con éxito.")


# ---------------------------------------------------------
def buscar_elemento(datos):
    print("\n Buscar objeto por ID")

    try:
        item_id = int(input("Introduce el ID a buscar: "))
    except ValueError:
        logging.warning("Búsqueda con ID inválido.")
        print("Debes introducir un número.")
        return

    for item in datos:
        if item["id"] == item_id:
            logging.info(f"Búsqueda realizada. Objeto encontrado: {item}")
            print("Objeto encontrado:", item)
            return item

    logging.info(f"Búsqueda fallida. ID {item_id} no existe.")
    print("No se encontró ningún objeto con ese ID.")


# ---------------------------------------------------------
def modificar_elemento(datos):
    print("\n Modificar objeto del inventario")

    try:
        item_id = int(input("ID del objeto a modificar: "))
    except ValueError:
        logging.warning("Modificación con ID inválido.")
        print(" ID inválido.")
        return

    for item in datos:
        if item["id"] == item_id:
            print("Objeto encontrado:", item)

            nuevo_nombre = input("Nuevo nombre (enter para mantener el actual): ").strip()
            if nuevo_nombre:
                item["nombre"] = nuevo_nombre

            nuevo_tipo = input("Nuevo tipo: ").strip()
            if nuevo_tipo:
                item["tipo"] = nuevo_tipo

            nueva_rareza = input("Nueva rareza: ").strip()
            if nueva_rareza:
                item["rareza"] = nueva_rareza

            guardar_inventario()
            logging.info(f"Objeto modificado: {item}")
            print("Objeto modificado correctamente.")
            return

    logging.warning(f"Intento de modificar ID inexistente: {item_id}")
    print("El objeto con ese ID no existe.")


# ---------------------------------------------------------
def eliminar_elemento(datos):
    print("\n Eliminar objeto del inventario")

    try:
        item_id = int(input("ID del objeto a eliminar: "))
    except ValueError:
        logging.warning("Eliminación con ID inválido.")
        print("ID inválido.")
        return

    for item in datos:
        if item["id"] == item_id:
            datos.remove(item)
            guardar_inventario()

            logging.info(f"Objeto eliminado: {item}")
            print("Objeto eliminado.")
            return

    logging.warning(f"Intento de borrar ID inexistente: {item_id}")
    print("No hay ningún objeto con ese ID.")


# ---------------------------------------------------------
def mostrar_todos(datos):
    print("\n Inventario completo:")

    if not datos:
        print("El inventario está vacío… ¡como tu barra de estamina!")
        return

    for item in datos:
        print(f"- ID: {item['id']} | {item['nombre']} | Tipo: {item['tipo']} | Rareza: {item['rareza']}")


# ==========================================
#              MENÚ PRINCIPAL
# ==========================================

def menu():
    cargar_inventario()

    while True:
        print("""
=============================
   MENÚ DEL INVENTARIO DS3 
=============================
1. Añadir objeto
2. Buscar objeto
3. Modificar objeto
4. Eliminar objeto
5. Mostrar inventario
6. Salir
""")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            insertar_elemento(inventario)
        elif opcion == "2":
            buscar_elemento(inventario)
        elif opcion == "3":
            modificar_elemento(inventario)
        elif opcion == "4":
            eliminar_elemento(inventario)
        elif opcion == "5":
            mostrar_todos(inventario)
        elif opcion == "6":
            guardar_inventario()
            logging.info("Aplicación cerrada por el usuario.")
            print("Saliendo del inventario... ¡Que el fuego te guíe!")
            break
        else:
            logging.warning(f"Opción inválida seleccionada: {opcion}")
            print("Opción inválida. Intenta nuevamente.")


# ------------------------------------------
if __name__ == "__main__":
    menu()
