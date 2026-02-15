# ==========================================
#   Gestor de Pilotos de F1
# ==========================================

import json
import logging
import os

ARCHIVO_JSON = "inventario_f1.json"
ARCHIVO_LOG = "inventario_f1.log"

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
# CLASE PILOTO
# ------------------------------------------

class Piloto:
    """Representa un piloto de Fórmula 1."""

    def __init__(self, piloto_id, nombre, equipo, nacionalidad):
        self.piloto_id = piloto_id
        self.nombre = nombre
        self.equipo = equipo
        self.nacionalidad = nacionalidad

    def to_dict(self):
        """Convierte el piloto a diccionario para guardarlo en JSON."""
        return {
            "id": self.piloto_id,
            "nombre": self.nombre,
            "equipo": self.equipo,
            "nacionalidad": self.nacionalidad
        }

    def mostrar(self):
        """Muestra la información del piloto por pantalla."""
        print(f"- ID: {self.piloto_id} | {self.nombre} | Equipo: {self.equipo} | Nacionalidad: {self.nacionalidad}")


# ------------------------------------------
# CLASE INVENTARIO
# ------------------------------------------

class Inventario:
    """Gestiona la colección de pilotos de F1."""

    def __init__(self):
        self.pilotos = []

    def cargar(self):
        """Carga los pilotos desde el archivo JSON."""
        if not os.path.exists(ARCHIVO_JSON):
            logging.warning("No existe archivo JSON. Se inicia inventario vacío.")
            return

        try:
            with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                self.pilotos = [
                    Piloto(p["id"], p["nombre"], p["equipo"], p["nacionalidad"])
                    for p in datos
                ]
                logging.info("Inventario cargado correctamente.")
        except Exception as e:
            logging.error(f"Error cargando inventario: {e}")

    def guardar(self):
        """Guarda los pilotos en el archivo JSON."""
        try:
            with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
                json.dump([p.to_dict() for p in self.pilotos], archivo, indent=4, ensure_ascii=False)
                logging.info("Inventario guardado correctamente.")
        except Exception as e:
            logging.error(f"Error guardando inventario: {e}")

    def id_existe(self, piloto_id):
        """Comprueba si ya existe un piloto con ese ID."""
        return any(p.piloto_id == piloto_id for p in self.pilotos)

    def buscar_por_id(self, piloto_id):
        """Devuelve el piloto con ese ID, o None si no existe."""
        for p in self.pilotos:
            if p.piloto_id == piloto_id:
                return p
        return None


# ------------------------------------------
# FUNCIONES DEL MENÚ
# ------------------------------------------

def insertar_piloto(inventario):
    """Añade un nuevo piloto al inventario."""
    print("\n Añadir nuevo piloto")

    while True:
        try:
            piloto_id = int(input("ID del piloto: "))
            if inventario.id_existe(piloto_id):
                print("Ese ID ya existe.")
                continue
            break
        except ValueError:
            print("El ID debe ser un número.")

    nombre = input("Nombre del piloto: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre del piloto: ").strip()

    equipo = input("Equipo (Ferrari, Mercedes, Red Bull...): ").strip()
    nacionalidad = input("Nacionalidad: ").strip()

    nuevo = Piloto(piloto_id, nombre, equipo, nacionalidad)
    inventario.pilotos.append(nuevo)
    inventario.guardar()

    logging.info(f"Piloto añadido: {nuevo.to_dict()}")
    print("Piloto añadido con éxito.")


def buscar_piloto(inventario):
    """Busca un piloto por su ID."""
    print("\n Buscar piloto por ID")

    try:
        piloto_id = int(input("Introduce el ID a buscar: "))
    except ValueError:
        print("Debes introducir un número.")
        logging.warning("Búsqueda con ID inválido.")
        return

    piloto = inventario.buscar_por_id(piloto_id)
    if piloto:
        piloto.mostrar()
        logging.info(f"Piloto encontrado: {piloto.to_dict()}")
    else:
        print("No se encontró ningún piloto con ese ID.")
        logging.info(f"Búsqueda fallida. ID {piloto_id} no existe.")


def modificar_piloto(inventario):
    """Modifica los datos de un piloto existente."""
    print("\n Modificar piloto")

    try:
        piloto_id = int(input("ID del piloto a modificar: "))
    except ValueError:
        print("ID inválido.")
        logging.warning("Modificación con ID inválido.")
        return

    piloto = inventario.buscar_por_id(piloto_id)
    if not piloto:
        print("No existe ningún piloto con ese ID.")
        logging.warning(f"Intento de modificar ID inexistente: {piloto_id}")
        return

    piloto.mostrar()

    nuevo_nombre = input("Nuevo nombre (enter para mantener el actual): ").strip()
    if nuevo_nombre:
        piloto.nombre = nuevo_nombre

    nuevo_equipo = input("Nuevo equipo: ").strip()
    if nuevo_equipo:
        piloto.equipo = nuevo_equipo

    nueva_nacionalidad = input("Nueva nacionalidad: ").strip()
    if nueva_nacionalidad:
        piloto.nacionalidad = nueva_nacionalidad

    inventario.guardar()
    logging.info(f"Piloto modificado: {piloto.to_dict()}")
    print("Piloto modificado correctamente.")


def eliminar_piloto(inventario):
    """Elimina un piloto del inventario."""
    print("\n Eliminar piloto")

    try:
        piloto_id = int(input("ID del piloto a eliminar: "))
    except ValueError:
        print("ID inválido.")
        logging.warning("Eliminación con ID inválido.")
        return

    piloto = inventario.buscar_por_id(piloto_id)
    if not piloto:
        print("No hay ningún piloto con ese ID.")
        logging.warning(f"Intento de borrar ID inexistente: {piloto_id}")
        return

    inventario.pilotos.remove(piloto)
    inventario.guardar()
    logging.info(f"Piloto eliminado: {piloto.to_dict()}")
    print("Piloto eliminado.")


def mostrar_todos(inventario):
    """Muestra todos los pilotos del inventario."""
    print("\n Inventario completo de pilotos F1:")

    if not inventario.pilotos:
        print("El inventario está vacío... ¡como la parrilla sin motores!")
        return

    for piloto in inventario.pilotos:
        piloto.mostrar()


# ==========================================
#              MENÚ PRINCIPAL
# ==========================================

def menu():
    inventario = Inventario()
    inventario.cargar()

    while True:
        print("""
=============================
   MENÚ DEL INVENTARIO F1
=============================
1. Añadir piloto
2. Buscar piloto
3. Modificar piloto
4. Eliminar piloto
5. Mostrar todos los pilotos
6. Salir
""")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            insertar_piloto(inventario)
        elif opcion == "2":
            buscar_piloto(inventario)
        elif opcion == "3":
            modificar_piloto(inventario)
        elif opcion == "4":
            eliminar_piloto(inventario)
        elif opcion == "5":
            mostrar_todos(inventario)
        elif opcion == "6":
            inventario.guardar()
            logging.info("Aplicación cerrada por el usuario.")
            print("Saliendo... ¡Luces apagadas y allá vamos!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")
            logging.warning(f"Opción inválida seleccionada: {opcion}")


# ------------------------------------------
if __name__ == "__main__":
    menu()

