import time
import numpy as np

# Inicio de sesión o creación de usuario
contraseña = 2515
contraseña_admin = 1515
intentos = 3
tiempo_pausa = 2
contraseñas= np.array([2515, 1515])
tipos_usuario = np.array(["usuario","administrador"])

calificaciones_juegos = np.array([
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        
])
indice = None

# Diccionario de juegos
juegos = {     
    "1": {"nombre": "Coleccion Master Chief", "precio": 45.000},
    "2": {"nombre": "Fifa 2024", "precio": 110.000},
    "3": {"nombre": "Call OF Duty", "precio": 94.000},
    "4": {"nombre": "Fornite", "precio": 55.000},
    "5": {"nombre": "Apex Legendes", "precio": 80.000},
}

# Lista para almacenar los juegos comprados
juegos_comprados = []

def mostrar_juegos():
    global juegos, juegos_ordenados
    if 'juegos_ordenados' in globals():
        juegos_lista = juegos_ordenados
    else:
        juegos_lista = list(juegos.items())
    
    print("\nLista de juegos:")
    for id_juego, juego in juegos_lista:
        print(f"{id_juego}. {juego['nombre']} - ${juego['precio']:.2f}")


# Matriz para almacenar calificaciones de juegos
calificaciones_juegos = np.zeros((2, len(juegos)))

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

def calificacion_promedio():
    # Calcular calificación promedio de todos los juegos
    calificaciones = calificaciones_juegos.flatten()
    calificaciones = calificaciones[calificaciones != 0]  # Eliminar calificaciones vacías
    
    if len(calificaciones) > 0:  # Verificar si hay calificaciones
        calificacion_promedio = np.mean(calificaciones)
        print(f"Calificación promedio de todos los juegos: {calificacion_promedio:.2f}")
    else:
        print("No hay calificaciones para mostrar.")

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

def comprar_juego():
    global juegos, juegos_ordenados, juegos_comprados, calificaciones_juegos
    if 'juegos_ordenados' in globals():
        juegos_lista = juegos_ordenados
    else:
        juegos_lista = list(juegos.items())
    
    mostrar_juegos()
    id_juego = input("Ingrese el número del juego que desea comprar: ")
    
    for id, juego in juegos_lista:
        if id == id_juego:
            print(f"Ha comprado {juego['nombre']} por ${juego['precio']:.2f}")
            juegos_comprados.append({"nombre": juego['nombre'], "precio": juego['precio']})
            
            calificar = input("¿Desea calificar el juego? (S/N): ")
            if calificar.upper() == 'S':
                calificar_juego("usuario", None)
                calificacion_promedio()
            
            return
    
    print("Juego no encontrado")

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

def eliminar_juego(id_juego):
    if id_juego in juegos and int(id_juego) <= calificaciones_juegos.shape[1]:
        del juegos[id_juego]
        calificaciones_juegos = np.delete(calificaciones_juegos, int(id_juego) - 1, axis=1)
        print("juego eliminado con exito")
    else:
        print("juego no encontrado o ID inválido")

# Agrega esta función después de la definición de juegos
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

# Modifica la función ordenar_juegos_por_precio para utilizar quick_sort
def ordenar_juegos_por_precio():
    global juegos, juegos_ordenados
    tipo_orden = input("Desea ordenar en ascendente (A) o descendente (D)? ")
    if tipo_orden.upper() == 'A':
        tipo_orden = 'ascendente'
    elif tipo_orden.upper() == 'D':
        tipo_orden = 'descendente'
    else:
        print("Opción inválida")
        return
    
    juegos_lista = list(juegos.items())
    juegos_ordenados = quick_sort(juegos_lista, tipo_orden)
    
    print("\nJuegos ordenados por precio:")
    for id_juego, juego in juegos_ordenados:
        print(f"{id_juego}. {juego['nombre']} - ${juego['precio']:.2f}")

def menu_administrador():
    global juegos, calificaciones_juegos
    while True:
        print("\n ---Menu Administrador---")
        print(" 1. Agregar juegos ")
        print(" 2. Eliminar juegos ")
        print(" 3. Cambiar precio de juegos ")
        print(" 4. Salir ")
        opcion = input("ingresa una opcion: ")
        if opcion == '1':
            agregar_juego()
        elif opcion == '2':
            mostrar_juegos()
            id_juego = input(" ingresa el ID del juego que deseas eliminar: ")
            eliminar_juego(id_juego)
            calificaciones_juegos = np.delete(calificaciones_juegos, int(id_juego) - 1, axis=1)
        elif opcion == '3':
            mostrar_juegos()
            id_juego = input("ingresa el ID del juego que deseas cambiar de precio: ")
            actualizar_precio(id_juego)
        elif opcion == '4':
            print("gracias por tu visita creador ")
            break
        else:
            print("opcion invalida,\n intentalo de nuevo")

def agregar_juego():
    global juegos, calificaciones_juegos
    id_juego = str(len(juegos) + 1)
    nombre_juego = input("Ingrese el nombre del juego: ")
    precio_juego = float(input("Ingrese el precio del juego: "))
    juegos[id_juego] = {"nombre": nombre_juego, "precio": precio_juego}
    print("Juego agregado con éxito")
    # Agregar calificaciones_juegos
    calificaciones_juegos = np.pad(calificaciones_juegos, ((0, 0), (1, 0)), mode='constant')

def eliminar_juego(id_juego):
    global juegos, calificaciones_juegos
    if id_juego in juegos:
        del juegos[id_juego]
        print("Juego eliminado con éxito")
    else:
        print("Juego no encontrado")

def actualizar_precio(id_juego):
    global juegos, calificaciones_juegos
    if id_juego in juegos:
        nuevo_precio = float(input("Ingrese el nuevo precio: "))
        juegos[id_juego]["precio"] = nuevo_precio
        print("Precio actualizado con éxito")
    else:
        print("Juego no encontrado")

def menu_principal():
    global juegos_ordenados
    while True:
        print("\n""                      " "--- Menú Principal ---")
        print("                    1."            " Comprar juego")
        print("                    2."            " Recoger juegos")
        print("                    3."            " Buscar juegos")
        print("                    4."            " Menu administador ")
        print("                    5."            " Ordenar juegos por precio")
        print("                    6."            " Salir")
        opcion = input("\n" "Seleccione una opción: ")
        if opcion == '1':
            comprar_juego()
        elif opcion == '2':
            recoger_juegos()
        elif opcion == '3':
            buscar_juegos()
        elif opcion == '4':
            contraseña_administrador = int(input(" Ingresa la contraseña del administrador: "))
            if contraseña_administrador==contraseña_admin:
                menu_administrador()
            else:
                print("contraseña incorrecta")
        elif opcion == '5':
            ordenar_juegos_por_precio()
        elif opcion == '6':
            print("Gracias por su visita. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")



while intentos > 0:
    ingresar_contraseña = int(input("Ingresa la contraseña: "))
    indice = np.where(contraseñas == ingresar_contraseña)[0]
    if len(indice) > 0:
        tipo_usuario = tipos_usuario[indice[0]]
        print(f"inicio de sesion correcto como \n {tipo_usuario} ")
        if tipo_usuario == "usuario":
            menu_principal()
        elif tipo_usuario == "administrador":
            menu_administrador()
        calificar = (input("¿desea calificar el juego? (S/N):"))
        if calificar.lower() == "s":
            calificar_juego(tipo_usuario, indice[0])  # Corrección aquí
            calificacion_promedio()
        break
    else:
        intentos -= 1
        print(f"CONTRASEÑA INCORRECTA. {intentos} INTENTOS RESTANTES")
        if intentos > 0:
            print(f"{tiempo_pausa} segundos antes de otro intento")
            time.sleep(tiempo_pausa)
            tiempo_pausa += 2
        if intentos == 0:
            print("Cuenta bloqueada")