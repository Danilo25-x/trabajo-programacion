import time
import numpy as np

# Inicio de sesión o creación de usuario
contraseña = 2515
contraseña_admin = 1515
intentos = 3
tiempo_pausa = 2

contraseñas = np.array([2515, 1515])  # Contraseñas de usuario y administrador
tipos_usuario = np.array(["usuario", "administrador"])  # Tipos de usuario

# Inicializar el diccionario de juegos y la matriz de calificaciones
juegos = {}
calificaciones_juegos = np.zeros((2, 5))  # Para almacenar las calificaciones de los juegos
juegos_ordenados = []  # Inicializar juegos ordenados como lista vacía
juegos_comprados = []  # Definir globalmente una lista vacía de juegos comprados


# Función para cargar los juegos desde un archivo
def cargar_juegos():
    global juegos
    try:
        with open('juegos.txt', 'r') as archivo:
            for linea in archivo.readlines():
                # Ignorar líneas vacías
                if not linea.strip():
                    continue
                id_juego, nombre_juego, precio_juego = linea.strip().split(',')
                juegos[id_juego] = {"nombre": nombre_juego, "precio": float(precio_juego)}
    except FileNotFoundError:
        print("Archivo de juegos no encontrado. Se creará uno nuevo.")

# Función para guardar los juegos en el archivo
def guardar_juegos():
    with open('juegos.txt', 'w') as archivo:
        for id_juego, juego in juegos.items():
            archivo.write(f"{id_juego},{juego['nombre']},{juego['precio']}\n")

# Función para mostrar los juegos
def mostrar_juegos():
    print("\nLista de juegos:")
    for id_juego, juego in juegos.items():
        print(f"{id_juego}. {juego['nombre']} - ${juego['precio']:.2f}")

# Función para agregar un juego
def agregar_juego():
    global juegos, calificaciones_juegos
    id_juego = str(len(juegos) + 1)
    nombre_juego = input("Ingrese el nombre del juego: ")
    precio_juego = float(input("Ingrese el precio del juego: "))
    juegos[id_juego] = {"nombre": nombre_juego, "precio": precio_juego}
    print("Juego agregado con éxito")
    # Guardar en el archivo
    guardar_juegos()

    # Agregar una nueva columna a la matriz de calificaciones
    calificaciones_juegos = np.pad(calificaciones_juegos, ((0, 0), (1, 0)), mode='constant')

# Función para eliminar un juego
def eliminar_juego(id_juego):
    global juegos, calificaciones_juegos
    if id_juego in juegos:
        del juegos[id_juego]
        print("Juego eliminado con éxito")
        # Guardar los cambios en el archivo
        guardar_juegos()
        
        # Eliminar la calificación de ese juego
        calificaciones_juegos = np.delete(calificaciones_juegos, int(id_juego) - 1, axis=1)
    else:
        print(f"Juego con ID {id_juego} no encontrado.")

# Función para actualizar el precio de un juego
def actualizar_precio(id_juego):
    global juegos
    if id_juego in juegos:
        nuevo_precio = float(input("Ingrese el nuevo precio: "))
        juegos[id_juego]["precio"] = nuevo_precio
        print("Precio actualizado con éxito")
        # Guardar los cambios en el archivo
        guardar_juegos()
    else:
        print("Juego no encontrado")

# Función para calificar un juego
def calificar_juego(tipo_usuario, indice):
    id_juego = input("Ingrese el número del juego que desea calificar: ")
    if id_juego in juegos:
        calificacion = float(input("Ingrese la calificación (1-5): "))
        while calificacion < 1 or calificacion > 5:
            print("Calificación inválida. Por favor, ingrese una calificación entre 1 y 5.")
            calificacion = float(input("Ingrese la calificación (1-5): "))
        
        # Convertir id_juego a índice (0-4)
        indice_juego = int(id_juego) - 1
        
        # Guardar calificación en la matriz
        if tipo_usuario == "usuario":
            calificaciones_juegos[0, indice_juego] = calificacion
        elif tipo_usuario == "administrador":
            calificaciones_juegos[1, indice_juego] = calificacion
        
        print("Calificación guardada con éxito.")
    else:
        print("Juego no encontrado.")

# Función para mostrar las calificaciones de los juegos
def mostrar_calificaciones_juegos():
    print("\nCalificaciones de juegos:")
    for i, (id_juego, juego) in enumerate(juegos.items()):
        calificacion_usuario = calificaciones_juegos[0, i]
        calificacion_admin = calificaciones_juegos[1, i]
        
        print(f"{id_juego}. {juego['nombre']}:")
        if calificacion_usuario != 0:
            print(f"  - Calificación usuario: {calificacion_usuario:.2f}")
        else:
            print("  - Calificación usuario: No calificado")
        
        if calificacion_admin != 0:
            print(f"  - Calificación administrador: {calificacion_admin:.2f}")
        else:
            print("  - Calificación administrador: No calificado")

# Función para ordenar juegos por precio
def ordenar_juegos_por_precio():
    global juegos
    tipo_orden = input("Desea ordenar en ascendente (A) o descendente (D)? ")
    if tipo_orden.upper() == 'A':
        tipo_orden = 'ascendente'
    elif tipo_orden.upper() == 'D':
        tipo_orden = 'descendente'
    else:
        print("Opción inválida")
        return

    juegos_lista = list(juegos.items())
    juegos_ordenados = quick_sort(juegos_lista, tipo_orden)  # Se debe retornar y actualizar la variable global

    print("\nJuegos ordenados por precio:")
    for id_juego, juego in juegos_ordenados:
        print(f"{id_juego}. {juego['nombre']} - ${juego['precio']:.2f}")

def recoger_juegos():
    global juegos_comprados, juegos, calificaciones_juegos
    if not juegos_comprados:
        print("\nNo has comprado ningún juego todavía.")
    else:
        print("\nJuegos disponibles para recoger:")
        for i, juego in enumerate(juegos_comprados, 1):
            id_juego = [id for id, juego_comprado in juegos.items() if juego_comprado['nombre'] == juego['nombre']][0]
            calificacion_usuario = calificaciones_juegos[0, int(id_juego) - 1]
            calificacion_admin = calificaciones_juegos[1, int(id_juego) - 1]
            
            print(f"{i}. {juego['nombre']} - ${juego['precio']:.2f}")
            if calificacion_usuario != 0:
                print(f"  - Calificación usuario: {calificacion_usuario:.2f}")
            else:
                print("  - Calificación usuario: No calificado")
            
            if calificacion_admin != 0:
                print(f"  - Calificación administrador: {calificacion_admin:.2f}")
            else:
                print("  - Calificación administrador: No calificado")
        
        seleccion = input("\nIngrese el número del juego que desea recoger (o 'todos' para recoger todos): ")
        if seleccion.lower() == 'todos':
            print("\nHas recogido todos tus juegos:")
            for juego in juegos_comprados:
                print(f"- {juego['nombre']} - ${juego['precio']}")
            juegos_comprados.clear()
        elif seleccion.isdigit() and 1 <= int(seleccion) <= len(juegos_comprados):
            juego_recogido = juegos_comprados.pop(int(seleccion) - 1)
            print(f"Has recogido: {juego_recogido['nombre']} - ${juego_recogido['precio']}")
        else:
            print("Selección inválida.")

# Función para el ordenamiento rápido (quick sort) de juegos
def quick_sort(juegos, tipo_orden):
    if len(juegos) <= 1:
        return juegos
    pivote = juegos[len(juegos) // 2]
    izquierda = [x for x in juegos if x[1]['precio'] < pivote[1]['precio']]
    medio = [x for x in juegos if x[1]['precio'] == pivote[1]['precio']]
    derecha = [x for x in juegos if x[1]['precio'] > pivote[1]['precio']]
    
    if tipo_orden == 'ascendente':
        return quick_sort(izquierda, tipo_orden) + medio + quick_sort(derecha, tipo_orden)
    elif tipo_orden == 'descendente':
        return quick_sort(derecha, tipo_orden) + medio + quick_sort(izquierda, tipo_orden)

# Función para el menú principal de administrador
def menu_administrador():
    while True:
        print("\n ---Menu Administrador---")
        print(" 1. Agregar juegos ")
        print(" 2. Eliminar juegos ")
        print(" 3. Mostrar juegos ")
        print(" 4. Actualizar precio juego ")
        print(" 5. Ordenar juegos por precio ")
        print(" 6. Mostrar calificaciones ")
        print(" 7. Salir ")

        opcion = input("\nElige una opción: ")
        
        if opcion == '1':
            agregar_juego()
        elif opcion == '2':
            id_juego = input("Ingrese el ID del juego que desea eliminar: ")
            eliminar_juego(id_juego)
        elif opcion == '3':
            mostrar_juegos()
        elif opcion == '4':
            id_juego = input("Ingrese el ID del juego que desea actualizar: ")
            actualizar_precio(id_juego)
        elif opcion == '5':
            ordenar_juegos_por_precio()
        elif opcion == '6':
            mostrar_calificaciones_juegos()
        elif opcion == '7':
            break
        else:
            print("Opción inválida, por favor intente de nuevo.")


def calificacion_promedio():
    # Calcular calificación promedio de todos los juegos
    calificaciones = calificaciones_juegos.flatten()
    calificaciones = calificaciones[calificaciones != 0]  # Eliminar calificaciones vacías
    
    if len(calificaciones) > 0:  # Verificar si hay calificaciones
        calificacion_promedio = np.mean(calificaciones)
        print(f"Calificación promedio de todos los juegos: {calificacion_promedio:.2f}")
    else:
        print("No hay calificaciones para mostrar.")

def comprar_juego():
    global juegos, juegos_comprados, calificaciones_juegos
    mostrar_juegos()
    id_juego = input("Ingrese el número del juego que desea comprar: ")
    
    if id_juego in juegos:
        juego = juegos[id_juego]
        print(f"Ha comprado {juego['nombre']} por ${juego['precio']:.2f}")
        juegos_comprados.append({"nombre": juego['nombre'], "precio": juego['precio']})
        
        calificar = input("¿Desea calificar el juego? (S/N): ")
        if calificar.upper() == 'S':
            calificar_juego("usuario", None)  # Asegúrate de manejar correctamente el tipo de usuario
            calificacion_promedio()
    else:
        print("Juego no encontrado.")


def buscar_juegos():
    print("\n ---Busqueda de juegos---")
    nombre_juego = input(" ingresa el nombre del juego: ").lower()
    resultados = [juego for juego in juegos.values() if nombre_juego in juego['nombre'].lower()]
    
    if resultados:
        print(" resultado de la busqueda :")
        for juego in resultados:
            print(f"-{juego['nombre']}-${juego['precio']}")
        
        respuesta = input("¿ Desea comprar este videojuego ? (S/N): ")
        if respuesta.lower() == 'S':
            juego_comprado = resultados[0]
            juegos_comprados.append({"nombre": juego_comprado['nombre'], "precio": juego_comprado['precio']})
            print(f"usted ha comprado {juego_comprado['nombre']} por ${juego_comprado['precio']}")
            
            calificar = input("¿Desea calificar el juego? (S/N): ")
            if calificar.upper() == 'S':
                calificar_juego("usuario", None)
                calificacion_promedio()
        
        else:
            print("Busqueda finalizada ")
    
    else:
        print("no se ha encontrado resultados")

# Función para el menú principal del usuario
def menu_principal():
    global juegos_ordenados
    while True:
        print("\n --- Menú Principal ---")
        print(" 1. Comprar juego")
        print(" 2. Recoger juegos")
        print(" 3. Buscar juegos")
        print(" 4. Menu Administrador")
        print(" 5. Ordenar juegos por precio")
        print(" 6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            comprar_juego()
        elif opcion == '2':
            recoger_juegos()
        elif opcion == '3':
            buscar_juegos()
        elif opcion == '4':
            contraseña_administrador = int(input(" Ingresa la contraseña del administrador: "))
            if contraseña_administrador == contraseña_admin:
                menu_administrador()
            else:
                print("Contraseña incorrecta")
        elif opcion == '5':
            ordenar_juegos_por_precio()
        elif opcion == '6':
            print("Gracias por su visita. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

# Cargar los juegos al iniciar
cargar_juegos()

# Iniciar sesión
while intentos > 0:
    ingresar_contraseña = int(input("Ingresa la contraseña: "))
    indice = np.where(contraseñas == ingresar_contraseña)[0]
    if len(indice) > 0:
        tipo_usuario = tipos_usuario[indice[0]]
        print(f"Ingreso exitoso como {tipo_usuario}")
        if tipo_usuario == "usuario":
            menu_principal()
        elif tipo_usuario == "administrador":
            menu_administrador()
        break
    else:
        intentos -= 1
        print(f"Contraseña incorrecta. {intentos} intentos restantes")
        if intentos > 0:
            print(f"{tiempo_pausa} segundos antes de otro intento")
            time.sleep(tiempo_pausa)
            tiempo_pausa += 2
        if intentos == 0:
            print("Cuenta bloqueada")
    