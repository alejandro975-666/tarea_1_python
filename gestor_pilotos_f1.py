# ==========================================
#   Gestor de Pilotos de F1
#   Aplicación para gestionar un inventario de pilotos de Fórmula 1
#   con operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
# ==========================================

import json
import logging
import os

# Definición de las rutas de los archivos de datos y registro
ARCHIVO_JSON = "inventario_f1.json"  # Archivo donde se guardan los pilotos en formato JSON
ARCHIVO_LOG = "inventario_f1.log"    # Archivo donde se registran todas las acciones

# ------------------------------------------
# CONFIGURACIÓN DEL LOGGING
# ------------------------------------------
# El logging permite registrar eventos importantes de la aplicación
# para auditoría, debugging y seguimiento de errores

logging.basicConfig(
    filename=ARCHIVO_LOG,           # Se guardan en ARCHIVO_LOG
    level=logging.INFO,             # Nivel mínimo de severidad a registrar
    format="%(asctime)s - %(levelname)s - %(message)s"  # Formato con fecha, nivel y mensaje
)

logging.info("Aplicación iniciada.")


# ------------------------------------------
# CLASE PILOTO
# ------------------------------------------
# Esta clase representa la estructura de datos de un piloto de F1
# Cada piloto tiene atributos como nombre, equipo, nacionalidad, etc.

class Piloto:
    """Representa un piloto de Fórmula 1."""

    def __init__(self, piloto_id, nombre, equipo, nacionalidad, palmares, categoria):
        """
        Constructor de la clase Piloto.
        Inicializa todos los atributos del piloto con los parámetros recibidos.
        
        Args:
            piloto_id (int): Identificador único del piloto
            nombre (str): Nombre completo del piloto
            equipo (str): Equipo para el que corre (Ferrari, Mercedes, etc.)
            nacionalidad (str): País de origen del piloto
            palmares (str): Récord de logros (títulos, victorias, etc.)
            categoria (str): Categorías en las que ha participado (F3, F2, F1, etc.)
        """
        self.piloto_id = piloto_id
        self.nombre = nombre
        self.equipo = equipo
        self.nacionalidad = nacionalidad
        self.palmares = palmares
        self.categoria = categoria

    def to_dict(self):
        """
        Convierte el objeto Piloto a un diccionario.
        Es necesario para poder guardar el piloto en formato JSON.
        
        Returns:
            dict: Diccionario con todos los atributos del piloto
        """
        return {
            "id": self.piloto_id,
            "nombre": self.nombre,
            "equipo": self.equipo,
            "nacionalidad": self.nacionalidad,
            "palmares": self.palmares,
            "categoria": self.categoria
        }

    def mostrar(self):
        """
        Imprime por pantalla la información del piloto en formato legible.
        Se utiliza cuando se quiere mostrar los datos de un piloto al usuario.
        """
        print(f"- ID: {self.piloto_id} | {self.nombre} | Equipo: {self.equipo} | Nacionalidad: {self.nacionalidad} | Palmarés: {self.palmares} | Categoría: {self.categoria}")


# ------------------------------------------
# CLASE INVENTARIO
# ------------------------------------------
# Esta clase gestiona la colección completa de pilotos
# Proporciona métodos para cargar, guardar, buscar y manipular pilotos

class Inventario:
    """Gestiona la colección de pilotos de F1."""

    def __init__(self):
        """
        Constructor de la clase Inventario.
        Inicializa una lista vacía que contendrá todos los pilotos.
        """
        self.pilotos = []

    def cargar(self):
        """
        Carga los pilotos desde el archivo JSON almacenado en disco.
        Si el archivo no existe, inicia con un inventario vacío.
        Si hay un error al cargar, lo registra en el archivo de log.
        """
        if not os.path.exists(ARCHIVO_JSON):
            logging.warning("No existe archivo JSON. Se inicia inventario vacío.")
            return

        try:
            # Abre el archivo JSON en modo lectura
            with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                # Convierte cada diccionario JSON en un objeto Piloto
                self.pilotos = [
                    Piloto(p["id"], p["nombre"], p["equipo"], p["nacionalidad"], p["palmares"], p["categoria"])
                    for p in datos
                ]
                logging.info("Inventario cargado correctamente.")
        except Exception as e:
            # Si algo falla, registra el error
            logging.error(f"Error cargando inventario: {e}")

    def guardar(self):
        """
        Guarda todos los pilotos del inventario en el archivo JSON.
        Convierte los objetos Piloto a diccionarios y los guarda en formato JSON.
        Si hay un error, lo registra en el archivo de log.
        """
        try:
            # Abre el archivo JSON en modo escritura (crea uno nuevo si no existe)
            with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
                # Convierte todos los pilotos a diccionarios y los guarda
                json.dump([p.to_dict() for p in self.pilotos], archivo, indent=4, ensure_ascii=False)
                logging.info("Inventario guardado correctamente.")
        except Exception as e:
            # Si algo falla, registra el error
            logging.error(f"Error guardando inventario: {e}")

    def id_existe(self, piloto_id):
        """
        Comprueba si ya existe un piloto con el ID especificado.
        Se utiliza para evitar crear pilotos con IDs duplicados.
        
        Args:
            piloto_id (int): ID a verificar
            
        Returns:
            bool: True si existe, False si no existe
        """
        return any(p.piloto_id == piloto_id for p in self.pilotos)

    def buscar_por_id(self, piloto_id):
        """
        Busca un piloto específico por su ID.
        Se utiliza para obtener los datos de un piloto concreto.
        
        Args:
            piloto_id (int): ID del piloto a buscar
            
        Returns:
            Piloto: El objeto Piloto si existe, None si no existe
        """
        for p in self.pilotos:
            if p.piloto_id == piloto_id:
                return p
        return None

    def piloto_con_mas_titulos(self):
        """
        Encuentra el piloto con más títulos/logros en su palmarés.
        Se utiliza para mostrar estadísticas.
        Nota: Convierte el palmares a número entero para comparar.
        
        Returns:
            Piloto: El piloto con mayor valor en palmares, None si no hay pilotos
        """
        if not self.pilotos:
            return None
        return max(self.pilotos, key=lambda p: int(p.palmares))

    
    def buscar_por_nombre(self, nombre):
        """
        Busca pilotos cuyo nombre contenga la cadena especificada.
        La búsqueda no distingue entre mayúsculas y minúsculas.
        
        Args:
            nombre (str): Texto a buscar en los nombres
            
        Returns:
            list: Lista de pilotos cuyo nombre contiene el texto buscado
        """
        return [p for p in self.pilotos if nombre.lower() in p.nombre.lower()]


    def buscar_por_equipo(self, equipo):
        """
        Busca pilotos que corren o han corrido para el equipo especificado.
        La búsqueda no distingue entre mayúsculas y minúsculas.
        
        Args:
            equipo (str): Nombre del equipo a buscar
            
        Returns:
            list: Lista de pilotos del equipo buscado
        """
        return [p for p in self.pilotos if equipo.lower() in p.equipo.lower()]
    

    def buscar_por_nacionalidad(self, nacionalidad):
        """
        Busca pilotos que tengan la nacionalidad especificada.
        La búsqueda no distingue entre mayúsculas y minúsculas.
        
        Args:
            nacionalidad (str): País a buscar
            
        Returns:
            list: Lista de pilotos de la nacionalidad especificada
        """
        return [p for p in self.pilotos if nacionalidad.lower() in p.nacionalidad.lower()]


# ------------------------------------------
# FUNCIONES DEL MENÚ
# ------------------------------------------
# Estas funciones manejan las interacciones del usuario a través del menú

def insertar_piloto(inventario):
    """
    Añade un nuevo piloto al inventario.
    Solicita al usuario los datos del piloto con validaciones:
    - El ID debe ser un número y no puede estar duplicado
    - El nombre no puede estar vacío
    Después de añadir, guarda automáticamente el inventario en JSON.
    
    Args:
        inventario (Inventario): Objeto del inventario donde se añadirá el piloto
    """
    print("\n Añadir nuevo piloto")

    # Solicita y valida el ID
    while True:
        try:
            piloto_id = int(input("ID del piloto: "))
            if inventario.id_existe(piloto_id):
                print("Ese ID ya existe.")
                continue
            break
        except ValueError:
            print("El ID debe ser un número.")

    # Solicita y valida el nombre (no puede estar vacío)
    nombre = input("Nombre del piloto: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre del piloto: ").strip()

    # Solicita el resto de datos sin validación especial
    equipo = input("Equipo (Ferrari, Mercedes, Red Bull...): ").strip()
    nacionalidad = input("Nacionalidad: ").strip()
    palmares = input("Palmarés del piloto (Carreras ganadas, Títulos, Gran Premios ganados...): ")
    categoria = input("Categorías en las que el piloto participa o ha participado: ")
    

    # Crea un nuevo objeto Piloto y lo añade al inventario
    nuevo = Piloto(piloto_id, nombre, equipo, nacionalidad, palmares, categoria)
    inventario.pilotos.append(nuevo)
    inventario.guardar()

    # Registra la acción en el log
    logging.info(f"Piloto añadido: {nuevo.to_dict()}")
    print("Piloto añadido con éxito.")


def buscar_piloto(inventario):
    """
    Busca un piloto por su ID y muestra sus datos.
    Si el ID es inválido, muestra un mensaje de error.
    Si no existe el piloto, informa al usuario.
    
    Args:
        inventario (Inventario): Objeto del inventario en el que buscar
    """
    print("\n Buscar piloto por ID")

    try:
        piloto_id = int(input("Introduce el ID a buscar: "))
    except ValueError:
        print("Debes introducir un número.")
        logging.warning("Búsqueda con ID inválido.")
        return

    # Busca el piloto y lo muestra si existe
    piloto = inventario.buscar_por_id(piloto_id)
    if piloto:
        piloto.mostrar()
        logging.info(f"Piloto encontrado: {piloto.to_dict()}")
    else:
        print("No se encontró ningún piloto con ese ID.")
        logging.info(f"Búsqueda fallida. ID {piloto_id} no existe.")


def modificar_piloto(inventario):
    """
    Permite modificar los datos de un piloto existente.
    Busca el piloto por ID y luego solicita los nuevos valores.
    Si se deja un campo vacío (solo presionar Enter), no se modifica ese campo.
    Después de realizar cambios, guarda automáticamente el inventario.
    
    Args:
        inventario (Inventario): Objeto del inventario
    """
    print("\n Modificar piloto")

    try:
        piloto_id = int(input("ID del piloto a modificar: "))
    except ValueError:
        print("ID inválido.")
        logging.warning("Modificación con ID inválido.")
        return

    # Busca el piloto a modificar
    piloto = inventario.buscar_por_id(piloto_id)
    if not piloto:
        print("No existe ningún piloto con ese ID.")
        logging.warning(f"Intento de modificar ID inexistente: {piloto_id}")
        return

    # Muestra los datos actuales del piloto
    piloto.mostrar()

    # Solicita los nuevos valores de forma opcional
    nuevo_nombre = input("Nuevo nombre (enter para mantener el actual): ").strip()
    if nuevo_nombre:
        piloto.nombre = nuevo_nombre

    nuevo_equipo = input("Nuevo equipo: ").strip()
    if nuevo_equipo:
        piloto.equipo = nuevo_equipo

    nueva_nacionalidad = input("Nueva nacionalidad: ").strip()
    if nueva_nacionalidad:
        piloto.nacionalidad = nueva_nacionalidad

    nuevo_palmares = input("Nuevo palmares (si no ha habido cambios dejar en blanco): ").strip()
    if nuevo_palmares:
        piloto.palmares = nuevo_palmares

    nueva_categoria = input("Nueva categoría (si no ha habido cambios dejar en blanco): ").strip()
    if nueva_categoria:
        piloto.categoria = nueva_categoria

    # Guarda los cambios
    inventario.guardar()
    logging.info(f"Piloto modificado: {piloto.to_dict()}")
    print("Piloto modificado correctamente.")


def eliminar_piloto(inventario):
    """
    Elimina un piloto del inventario.
    Busca el piloto por ID y lo elimina si existe.
    Después de eliminar, guarda automáticamente el inventario.
    
    Args:
        inventario (Inventario): Objeto del inventario
    """
    print("\n Eliminar piloto")

    try:
        piloto_id = int(input("ID del piloto a eliminar: "))
    except ValueError:
        print("ID inválido.")
        logging.warning("Eliminación con ID inválido.")
        return

    # Busca el piloto a eliminar
    piloto = inventario.buscar_por_id(piloto_id)
    if not piloto:
        print("No hay ningún piloto con ese ID.")
        logging.warning(f"Intento de borrar ID inexistente: {piloto_id}")
        return

    # Elimina el piloto de la lista
    inventario.pilotos.remove(piloto)
    inventario.guardar()
    logging.info(f"Piloto eliminado: {piloto.to_dict()}")
    print("Piloto eliminado.")


def mostrar_todos(inventario):
    """
    Muestra todos los pilotos del inventario por pantalla.
    Si el inventario está vacío, muestra un mensaje personalizado.
    
    Args:
        inventario (Inventario): Objeto del inventario a mostrar
    """
    print("\n Inventario completo de pilotos F1:")

    # Verifica si hay pilotos
    if not inventario.pilotos:
        print("El inventario está vacío... ¡como la parrilla sin motores!")
        return

    # Muestra cada piloto usando su método mostrar()
    for piloto in inventario.pilotos:
        piloto.mostrar()


def mostrar_estadisticas(inventario):
    """
    Muestra estadísticas del inventario.
    Actualmente muestra el piloto con más títulos/logros.
    
    Args:
        inventario (Inventario): Objeto del inventario
    """
    print("\n ESTADISTICAS F1")
    mejor = inventario.piloto_con_mas_titulos()

    if mejor:
        print(f"Piloto con más titulos: {mejor.nombre} ({mejor.palmares} titulos)")
    else:
        print("No hay pilostos registrados")


def busqueda_avanzada(inventario):
    """
    Permite al usuario realizar búsquedas avanzadas con diferentes filtros.
    Opciones disponibles:
    1. Buscar por nombre
    2. Buscar por equipo
    3. Buscar por nacionalidad
    
    Muestra los resultados encontrados o un mensaje si no hay coincidencias.
    
    Args:
        inventario (Inventario): Objeto del inventario en el que buscar
    """
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

    # Según la opción elegida, realiza la búsqueda correspondiente
    if opcion == "1":
        nombre = input("Introduce el nombre: ")
        resultados = inventario.buscar_por_nombre(nombre)
    elif opcion == "2":
        equipo = input("Introduce el nombre del equipo: ")
        resultados = inventario.buscar_por_equipo(equipo)
    elif opcion == "3":
        nacionalidad = input("Introduce la nacionalidad del o de los pilotos deseados: ")
        resultados = inventario.buscar_por_nacionalidad(nacionalidad)
    else:
        print("Opción inválida.")
        return

    # Muestra los resultados
    if resultados:
        print("\n RESULTADOS:")
        for piloto in resultados:
            piloto.mostrar()
    else:
        print("No se encontraron resultados.")
    

# ==========================================
#              MENÚ PRINCIPAL
# ==========================================
# Esta es la función principal que controla el flujo de la aplicación

def menu():
    """
    Función principal que muestra el menú interactivo.
    Carga el inventario al inicio y permite al usuario elegir operaciones:
    1. Añadir piloto
    2. Buscar piloto
    3. Modificar piloto
    4. Eliminar piloto
    5. Mostrar todos los pilotos
    6. Búsqueda avanzada
    7. Salir
    
    El menú se repite en un bucle infinito hasta que el usuario elige salir.
    """
    # Crea un nuevo inventario y carga los datos desde JSON
    inventario = Inventario()
    inventario.cargar()

    # Bucle principal del menú
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

        # Ejecuta la función correspondiente a la opción elegida
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
            # Guarda antes de salir y registra la salida
            inventario.guardar()
            logging.info("Aplicación cerrada por el usuario.")
            print("Saliendo... ¡Luces apagadas y allá vamos!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")
            logging.warning(f"Opción inválida seleccionada: {opcion}")


# ------------------------------------------
# Punto de entrada del programa
# ------------------------------------------
if __name__ == "__main__":
    menu()
