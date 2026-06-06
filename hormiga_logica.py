import pygame as py
 
def generar_colores(n):
    """
    Genera n colores distintos en formato RGB para representar
    los estados de las celdas en el autómata.
    Parámetros:
        n (int): número de colores requeridos (debe ser positivo)
    Retorna:
        lista de tuplas (R, G, B) con los colores generados
    """
    colores = []
    for i in range(1, n + 1):
        r = int((i * 20) % 100)
        g = int((i * 80) % 200) + 55
        b = int((i * 60) % 156) + 100
        if (r, g, b) not in colores:
            colores.append((r, g, b))
    return colores
 
def generar_matriz_vacia(filas, columnas):
    """
    Crea y retorna una matriz bidimensional inicializada en cero.
    Parámetros:
        filas (int): número de filas
        columnas (int): número de columnas
    Retorna:
        matriz 2D (lista de listas) con todos los valores en 0
    """
    return [[0 for _ in range(columnas)] for _ in range(filas)]
 
def avanzar_hormiga(direccion, x, y):
    """
    Calcula la nueva posición de la hormiga tras avanzar una celda
    en la dirección que apunta actualmente.
    Parámetros:
        direccion (str): orientación actual ("arriba", "abajo", "izquierda", "derecha")
        x (int): columna actual
        y (int): fila actual
    Retorna:
        tupla (x, y) con la nueva posición
    """
    if direccion == "arriba":
        return x, y - 1
    elif direccion == "derecha":
        return x + 1, y
    elif direccion == "abajo":
        return x, y + 1
    elif direccion == "izquierda":
        return x - 1, y
 
def girar_hormiga(direccion, girar):
    """
    Determina la nueva orientación de la hormiga según el giro indicado.
    Parámetros:
        direccion (str): orientación actual ("arriba", "abajo", "izquierda", "derecha")
        girar (str): sentido del giro, "R" para derecha o "L" para izquierda
    Retorna:
        str con la nueva dirección de la hormiga
    """
    giros_derecha = {
        "arriba": "derecha",
        "derecha": "abajo",
        "abajo": "izquierda",
        "izquierda": "arriba"
    }
    giros_izquierda = {
        "arriba": "izquierda",
        "izquierda": "abajo",
        "abajo": "derecha",
        "derecha": "arriba"
    }
    if girar == "R":
        return giros_derecha[direccion]
    if girar == "L":
        return giros_izquierda[direccion]
 
def siguiente(numero, direccion):
    """
    Retorna el índice del siguiente color en el ciclo de estados de la celda.
    Parámetros:
        numero (int): índice del color actual de la celda
        direccion (list): lista de direcciones que define cuántos colores hay
    Retorna:
        int con el índice del siguiente color (de forma cíclica)
    """
    return (numero + 1) % len(direccion)