import numpy as np
import time
# Contraseñas de usuario
contraseña = 2515
intentos = 3
tiempo_pausa = 2

# Contraseñas de usuario
contraseñas = np.array([2515])  # Solo dejamos la contraseña para el usuario
tipos_usuario = np.array(["usuario"])  # Solo tenemos tipo "usuario"

# Inicializar el diccionario de juegos y la matriz de calificaciones
juegos = {}
calificaciones_juegos = np.zeros((2, 5))  # Para almacenar las calificaciones de los juegos
juegos_comprados = []  # Lista de juegos comprados
juegos_usuario = {}  # Diccionario para juegos creados por el usuario

# Clase Juego
class Juego:
    def _init_(self, id_juego, nombre_juego, plataforma, genero, precio):
        self.id_juego = id_juego
        self.nombre_juego = nombre_juego
        self.plataforma = plataforma
        self.genero = genero
        self.precio = precio

    def _str_(self):
        return f"ID: {self.id_juego}, Nombre: {self.nombre_juego}, Plataforma: {self.plataforma}, Género: {self.genero}, Precio: ${self.precio}"

# Clase EliminarRegistro
class EliminarRegistro:
    def _init_(self, juegos):
        """Inicializa la clase con los registros de juegos (puede ser la lista o diccionario de juegos)"""
        self.juegos = juegos  # Este es el diccionario de juegos registrados

    def eliminar_juego(self, id_juego):
        """Eliminar un juego del registro por su ID"""
        if id_juego in self.juegos:
            del self.juegos[id_juego]
            print(f"Juego con ID {id_juego} eliminado correctamente.")
            self.actualizar_archivo()
        else:
            print(f"El juego con ID {id_juego} no existe en el registro.")

    def mostrar_juegos(self):
        """Mostrar todos los juegos registrados"""
        if not self.juegos:
            print("No hay juegos registrados.")
        else:
            print("Juegos registrados:")
            for juego in self.juegos.values():
                print(juego)

    def actualizar_archivo(self):
        """Actualizar el archivo después de la eliminación de un juego"""
        with open('registros_juegos.txt', mode='w', encoding='utf-8') as archivo_txt:
            for juego in self.juegos.values():
                archivo_txt.write(f"{juego.id_juego} | {juego.nombre_juego} | {juego.plataforma} | {juego.genero} | ${juego.precio}\n")
            print("Archivo de registros actualizado correctamente.")

# Registro de Juegos (para agregar nuevos juegos)
class RegistroJuegos:
    def _init_(self):
        self.juegos = {}

    def agregar_juego(self):
        """Registrar un nuevo juego"""
        id_juego = str(len(self.juegos) + 1)
        nombre_juego = input("Ingrese el nombre del juego: ")
        plataforma = input("Ingrese la plataforma del juego (PC, PS5, Xbox, etc.): ")
        genero = input("Ingrese el género del juego (Aventura, Acción, RPG, etc.): ")
        precio = float(input("Ingrese el precio del juego: "))
        
        nuevo_juego = Juego(id_juego, nombre_juego, plataforma, genero, precio)
        self.juegos[id_juego] = nuevo_juego
        print("Juego registrado correctamente.")
        self.guardar_juegos()

    def guardar_juegos(self):
        """Guardar los juegos registrados en un archivo de texto"""
        with open('registros_juegos.txt', mode='w', encoding='utf-8') as archivo_txt:
            for juego in self.juegos.values():
                archivo_txt.write(f"{juego.id_juego} | {juego.nombre_juego} | {juego.plataforma} | {juego.genero} | ${juego.precio}\n")
            print("Juegos guardados correctamente en registros_juegos.txt.")

def agregar_juego_usuario():
    """Agregar un juego por el usuario"""
    id_juego = str(len(juegos_usuario) + 1)
    nombre_juego = input("Ingrese el nombre del juego: ")
    plataforma = input("Ingrese la plataforma del juego (PC, PS5, Xbox, etc.): ")
    genero = input("Ingrese el género del juego (Aventura, Acción, RPG, etc.): ")
    precio = float(input("Ingrese el precio del juego: "))
    
    nuevo_juego = Juego(id_juego, nombre_juego, plataforma, genero, precio)
    juegos_usuario[id_juego] = nuevo_juego
    print("Juego añadido correctamente.")

    # Guardar los juegos en el archivo de texto
    with open('registros_juegos_usuario.txt', mode='a', encoding='utf-8') as archivo_txt:
        archivo_txt.write(f"ID JUEGO {nuevo_juego.id_juego} | \n NOMBRE JUEGO {nuevo_juego.nombre_juego} | \n PLATAFORMA {nuevo_juego.plataforma} |\n GENERO  {nuevo_juego.genero} | \n PRECIO ${nuevo_juego.precio}\n")

def eliminar_juego_usuario():
    """Eliminar un juego creado por el usuario"""
    mostrar_juegos_usuario()
    id_juego = input("Ingrese el ID del juego a eliminar: ")
    if id_juego in juegos_usuario:
        del juegos_usuario[id_juego]
        print("Juego eliminado correctamente.")
        with open('registros_juegos_usuario.txt', mode='w', encoding='utf-8') as archivo_txt:
            for juego in juegos_usuario.values():
                archivo_txt.write(f"{juego.id_juego} | {juego.nombre_juego} | {juego.plataforma} | {juego.genero} | ${juego.precio}\n")
    else:
        print("El juego no existe.")

def mostrar_juegos_usuario():
    """Mostrar los juegos creados por el usuario"""
    if not juegos_usuario:
        print("No hay juegos creados por el usuario.")
    else:
        print("Juegos creados por el usuario:")
        for juego in juegos_usuario.values():
            print(juego)

def menu_principal():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Comprar juego")
        print("2. Recoger juegos")
        print("3. Buscar juegos")
        print("4. Añadir registro de juego")  # Opción para agregar juego
        print("5. Eliminar Registro de juego")  # Opción para eliminar juego
        print("6. Mostrar los registros")  # Mostrar juegos del usuario
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            comprar_juego()
        elif opcion == '2':
            recoger_juegos()
        elif opcion == '3':
            buscar_juegos()
        elif opcion == '4':
            agregar_juego_usuario()
        elif opcion == '5':
            eliminar_juego_usuario()
        elif opcion == '6':
            mostrar_juegos_usuario()
        elif opcion == '7':
            print("Gracias por su visita. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

def comprar_juego():
    print("Funcionalidad de compra de juego aún no implementada")

def recoger_juegos():
    print("Funcionalidad de recolección de juegos aún no implementada")

def buscar_juegos():
    print("Funcionalidad de búsqueda de juegos aún no implementada")

# Cargar juegos al inicio (puedes modificarlo para cargar desde archivos)
def cargar_juegos():
    pass  # Deberías cargar los juegos desde los archivos si deseas mantener los datos

# Iniciar sesión
while intentos > 0:
    ingresar_contraseña = int(input("Ingresa la contraseña: "))
    indice = np.where(contraseñas == ingresar_contraseña)[0]
    if len(indice) > 0:
        tipo_usuario = tipos_usuario[indice[0]]
        print(f"Ingreso exitoso como {tipo_usuario}")
        
        # Crear instancia de EliminarRegistro para manejar los juegos
        eliminar_registro = EliminarRegistro(juegos)
        
        menu_principal()
        break
    else:
        intentos -= 1
        print(f"Contraseña incorrecta. {intentos} intentos restantes")
        if intentos > 0:
            print(f"{tiempo_pausa} segundos antes de otro intento")
            time.sleep(tiempo_pausa)
            tiempo_pausa += 2
        if intentos == 0:
            print("cuenta bloqueada")
