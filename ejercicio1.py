# ==========================================
#   INVENTARIO DE DARK SOULS 3 EN PYTHON
# ==========================================

"""
Módulo de gestión de inventario inspirado en Dark Souls 3.
Permite añadir, buscar, modificar, eliminar y mostrar objetos.
Estructura utilizada: lista de diccionarios.
"""

# Estructura principal del inventario
inventario = []


# ---------------------------------------------------------
def insertar_elemento(datos):
    """
    Solicita datos al usuario y agrega un nuevo objeto al inventario.
    Valida que el ID sea un número y que el nombre no esté vacío.
    """
    print("\n Añadir nuevo objeto al inventario")

    # Validación de ID numérico
    while True:
        try:
            item_id = int(input("ID del objeto: "))
            break
        except ValueError:
            print("El ID debe ser un número.")

    # Validación del nombre
    nombre = input("Nombre del objeto: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre del objeto: ").strip()

    tipo = input("Tipo (arma, anillo, consumible...): ").strip()
    rareza = input("Rareza (común, raro, épico, legendario): ").strip()

    # Crear diccionario-objeto
    nuevo_item = {
        "id": item_id,
        "nombre": nombre,
        "tipo": tipo,
        "rareza": rareza
    }

    datos.append(nuevo_item)
    print("Objeto añadido con éxito.")


# ---------------------------------------------------------
def buscar_elemento(datos):
    """
    Busca un objeto del inventario según su ID.
    Devuelve el objeto encontrado o un mensaje informativo.
    """
    print("\n Buscar objeto por ID")
    try:
        item_id = int(input("Introduce el ID a buscar: "))
    except ValueError:
        print("Debes introducir un número.")
        return

    for item in datos:
        if item["id"] == item_id:
            print("Objeto encontrado:", item)
            return item

    print("No se encontró ningún objeto con ese ID.")


# ---------------------------------------------------------
def modificar_elemento(datos):
    """
    Permite modificar un campo de un objeto existente.
    Maneja errores si el ID no existe.
    """
    print("\n Modificar objeto del inventario")

    try:
        item_id = int(input("ID del objeto a modificar: "))
    except ValueError:
        print(" ID inválido.")
        return

    # Buscar el objeto
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

            print("Objeto modificado correctamente.")
            return
    
    print("El objeto con ese ID no existe.")


# ---------------------------------------------------------
def eliminar_elemento(datos):
    """
    Elimina un objeto según su ID.
    Maneja errores si el ID no existe.
    """
    print("\n Eliminar objeto del inventario")

    try:
        item_id = int(input("ID del objeto a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return

    for item in datos:
        if item["id"] == item_id:
            datos.remove(item)
            print("Objeto eliminado.")
            return

    print("No hay ningún objeto con ese ID.")


# ---------------------------------------------------------
def mostrar_todos(datos):
    """
    Muestra el inventario completo de forma formateada.
    """
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
    """
    Muestra y gestiona el menú interactivo del programa.
    """
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
            print("Saliendo del inventario... ¡Que el fuego te guíe!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")


# Ejecutar menú si el archivo se corre directamente
if __name__ == "__main__":
    menu()