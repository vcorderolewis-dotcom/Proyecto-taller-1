
import pygame
import random
from copy import deepcopy
 
 
def generar_matriz_aleatoria(filas, columnas):
    """
    Descripción: Genera una matriz bidimensional con valores 0 o 1 asignados aleatoriamente.
    Entradas:
        filas (int): número de filas (debe ser entero positivo)
        columnas (int): número de columnas (debe ser entero positivo)
    Salidas:
        lista de listas con valores aleatorios de 0 o 1
    Restricciones:
        - filas y columnas deben ser mayores a cero
    """
    if filas <= 0 or columnas <= 0:
        raise ValueError("Las dimensiones deben ser mayores a cero.")
    return [[random.randint(0, 1) for _ in range(columnas)] for _ in range(filas)]
 
 
def generar_matriz_vacia(filas, columnas):
    """
    Descripción: Genera una matriz bidimensional inicializada en cero.
    Entradas:
        filas (int): número de filas (debe ser entero positivo)
        columnas (int): número de columnas (debe ser entero positivo)
    Salidas:
        lista de listas con todos los valores en 0
    Restricciones:
        - filas y columnas deben ser mayores a cero
    """
    if filas <= 0 or columnas <= 0:
        raise ValueError("Las dimensiones deben ser mayores a cero.")
    return [[0] * columnas for _ in range(filas)]
 
 
def transicion_celula(estado_actual, vecinos, nac, sob):
    """
    Descripción: Calcula el nuevo estado de una célula según sus vecinos y las reglas del autómata.
    Entradas:
        estado_actual (int): estado actual de la célula (0 o 1)
        vecinos (list): lista con los estados de los 8 vecinos
        nac (list): caracteres string que determinan cuándo nace una célula muerta
        sob (list): caracteres string que determinan cuándo sobrevive una célula viva
    Salidas:
        int con el nuevo estado de la célula (0 o 1)
    Restricciones:
        - estado_actual debe ser 0 o 1
        - nac y sob deben contener caracteres del '0' al '8'
    """
    vivos = sum(vecinos)
    if estado_actual == 0:
        if str(vivos) in nac:
            return 1
    else:
        if str(vivos) in sob:
            return 1
    return 0
 
 
def transicion(matriz, nac, sob):
    """
    Descripción: Aplica la función de transición a toda la matriz y retorna la siguiente generación.
    Entradas:
        matriz (list): matriz 2D con el estado actual del autómata
        nac (list): reglas de nacimiento como lista de caracteres string
        sob (list): reglas de supervivencia como lista de caracteres string
    Salidas:
        nueva matriz 2D con el estado siguiente del autómata
    Restricciones:
        - matriz no debe estar vacía
        - nac y sob no deben estar vacíos
    """
    if not matriz or not matriz[0]:
        raise ValueError("La matriz no puede estar vacía.")
 
    filas    = len(matriz)
    columnas = len(matriz[0])
    nueva    = generar_matriz_vacia(filas, columnas)
 
    for r in range(filas):
        for c in range(columnas):
            vecinos = [
                matriz[(r + i) % filas][(c + j) % columnas]
                for i in [-1, 0, 1]
                for j in [-1, 0, 1]
                if not (i == 0 and j == 0)
            ]
            nueva[r][c] = transicion_celula(matriz[r][c], vecinos, nac, sob)
 
    return nueva