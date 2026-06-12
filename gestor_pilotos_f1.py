# Gestor de Pilotos de F1
# Aplicación para gestionar un inventario de pilotos de Fórmula 1
# con operaciones CRUD (Crear, Leer, Actualizar, Eliminar)

import json
import logging
import os

ARCHIVO_JSON = "inventario_f1.json"
ARCHIVO_LOG = "inventario_f1.log"

# Configuración del logging para guardar un registro de lo que hace la app
logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Aplicación iniciada.")


# Clase que representa a un piloto de F1
class Piloto:

    def __init__(self, piloto_id, nombre, equipo, nacionalidad, palmares, categoria):
        self.piloto_id = piloto_id
        self.nombre = nombre
        self.equipo = equipo
        self.nacionalidad = nacionalidad
        self.palmares = palmares
        self.categoria = categoria

    # Convierte el piloto a diccionario para poder guardarlo en JSON
    def to_dict(self):
        return {
            "id": self.piloto_id,
            "nombre": self.nombre,
            "equipo": self.equipo,
            "nacionalidad": self.nacionalidad,
            "palmares": self.palmares,
            "categoria": self.categoria
        }

    def mostrar(self):
        print(f"- ID: {self.piloto_id} | {self.nombre} | Equipo: {self.equipo} | "
              f"Nacionalidad: {self.nacionalidad} | Palmarés: {self.palmares} | Categoría: {self.categoria}")


# Clase que gestiona la lista de pilotos
class Inventario:

    def __init__(self):
        self.pilotos = []

    def cargar(self):
        if not os.path.exists(ARCHIVO_JSON):
            logging.warning("No existe archivo JSON. Se inicia inventario vacío.")
            return
        try:
            with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                for p in datos:
                    piloto = Piloto(p["id"], p["nombre"], p["equipo"], p["nacionalidad"], p["palmares"], p["categoria"])
                    self.pilotos.append(piloto)
            logging.info("Inventario cargado correctamente.")
        except Exception as e:
            logging.error(f"Error cargando inventario: {e}")

    def guardar(self):
        try:
            with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
                json.dump([p.to_dict() for p in self.pilotos], archivo, indent=4, ensure_ascii=False)
            logging.info("Inventario guardado correctamente.")
        except Exception as e:
            logging.error(f"Error guardando inventario: {e}")

    def id_existe(self, piloto_id):
        for p in self.pilotos:
            if p.piloto_id == piloto_id:
                return True
        return False

    def buscar_por_id(self, piloto_id):
        for p in self.pilotos:
            if p.piloto_id == piloto_id:
                return p
        return None

    def piloto_con_mas_titulos(self):
        if not self.pilotos:
            return None
        mejor = self.pilotos[0]
        for p in self.pilotos:
            if int(p.palmares) > int(mejor.palmares):
                mejor = p
        return mejor

    def buscar_por_nombre(self, nombre):
        resultados = []
        for p in self.pilotos:
            if nombre.lower() in p.nombre.lower():
                resultados.append(p)
        return resultados

    def buscar_por_equipo(self, equipo):
        resultados = []
        for p in self.pilotos:
            if equipo.lower() in p.equipo.lower():
                resultados.append(p)
        return resultados

    def buscar_por_nacionalidad(self, nacionalidad):
        resultados = []
        for p in self.pilotos:
            if nacionalidad.lower() in p.nacionalidad.lower():
                resultados.append(p)
        return resultados


# Añade un nuevo piloto al inventario
def insertar_piloto(inventario):
    print("\n Añadir nuevo piloto")

    # Pedimos el ID y comprobamos que sea válido y no esté repetido
    while True:
        try:
            piloto_id = int(input("ID del piloto: "))
            if inventario.id_existe(piloto_id):
                print("Ese ID ya existe.")
                continue
            break
        except ValueError:
            print("El ID debe ser un número.")

    # El nombre no puede estar vacío
    nombre = input("Nombre del piloto: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre del piloto: ").strip()

    equipo = input("Equipo (Ferrari, Mercedes, Red Bull...): ").strip()
    nacionalidad = input("Nacionalidad: ").strip()
    palmares = input("Palmarés del piloto (títulos mundiales): ")
    categoria = input("Categorías en las que participa o ha participado: ")

    nuevo = Piloto(piloto_id, nombre, equipo, nacionalidad, palmares, categoria)
    inventario.pilotos.append(nuevo)
    inventario.guardar()

    logging.info(f"Piloto añadido: {nuevo.to_dict()}")
    print("Piloto añadido con éxito.")


# Busca un piloto por ID y muestra sus datos
def buscar_piloto(inventario):
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


# Permite cambiar los datos de un piloto existente
def modificar_piloto(inventario):
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

    # Si el usuario no escribe nada, se mantiene el valor anterior
    nuevo_nombre = input("Nuevo nombre (enter para mantener el actual): ").strip()
    if nuevo_nombre:
        piloto.nombre = nuevo_nombre

    nuevo_equipo = input("Nuevo equipo (enter para mantener el actual): ").strip()
    if nuevo_equipo:
        piloto.equipo = nuevo_equipo

    nueva_nacionalidad = input("Nueva nacionalidad (enter para mantener): ").strip()
    if nueva_nacionalidad:
        piloto.nacionalidad = nueva_nacionalidad

    nuevo_palmares = input("Nuevo palmarés (enter para mantener): ").strip()
    if nuevo_palmares:
        piloto.palmares = nuevo_palmares

    nueva_categoria = input("Nueva categoría (enter para mantener): ").strip()
    if nueva_categoria:
        piloto.categoria = nueva_categoria

    inventario.guardar()
    logging.info(f"Piloto modificado: {piloto.to_dict()}")
    print("Piloto modificado correctamente.")


# Elimina un piloto del inventario
def eliminar_piloto(inventario):
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


# Muestra todos los pilotos del inventario
def mostrar_todos(inventario):
    print("\n Inventario completo de pilotos F1:")

    if not inventario.pilotos:
        print("El inventario está vacío... ¡como la parrilla sin motores!")
        return

    for piloto in inventario.pilotos:
        piloto.mostrar()


# Muestra el piloto con más títulos
def mostrar_estadisticas(inventario):
    print("\n ESTADÍSTICAS F1")
    mejor = inventario.piloto_con_mas_titulos()

    if mejor:
        print(f"Piloto con más títulos: {mejor.nombre} ({mejor.palmares} títulos)")
    else:
        print("No hay pilotos registrados.")


# Permite buscar por nombre, equipo o nacionalidad
def busqueda_avanzada(inventario):
    print("""
=============================
   MENÚ DE BÚSQUEDA AVANZADA
=============================
1. Buscar por nombre
2. Buscar por equipo
3. Buscar por nacionalidad

Pulse cualquier otro número para salir de la búsqueda avanzada.
""")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        nombre = input("Introduce el nombre: ")
        resultados = inventario.buscar_por_nombre(nombre)
    elif opcion == "2":
        equipo = input("Introduce el nombre del equipo: ")
        resultados = inventario.buscar_por_equipo(equipo)
    elif opcion == "3":
        nacionalidad = input("Introduce la nacionalidad: ")
        resultados = inventario.buscar_por_nacionalidad(nacionalidad)
    else:
        print("Opción inválida.")
        return

    if resultados:
        print("\n RESULTADOS:")
        for piloto in resultados:
            piloto.mostrar()
    else:
        print("No se encontraron resultados.")


# Función principal con el menú de opciones
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
6. Búsqueda avanzada
7. Salir
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
            busqueda_avanzada(inventario)
        elif opcion == "7":
            inventario.guardar()
            logging.info("Aplicación cerrada por el usuario.")
            print("Saliendo... ¡Luces apagadas y allá vamos!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")
            logging.warning(f"Opción inválida seleccionada: {opcion}")


if __name__ == "__main__":
    menu()
