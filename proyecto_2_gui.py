import pygame
import easygui as g
import pickle as p
import random
import sys
import life_like_logica as li
import hormiga_logica as ho
 
velocidad = 15
 

def interfaz_principal():
    """
    Descripción: Muestra el menú principal del proyecto y redirige al autómata seleccionado.
    Entradas: Ninguna.
    Salidas: Ninguna (invoca la función del autómata elegido por el usuario).
    Restricciones: Requiere las librerías easygui, life_like_logica y hormiga_logica instaladas.
    """
    titulo = "Proyecto 1 Autómatas Celulares"
    mensaje = "Selecciona un autómata"
    opciones = ["Life-Like", "Hormiga de Langton"]
    eleccion = g.buttonbox(mensaje, titulo, choices=opciones)
 
    if eleccion == opciones[0]:
        life_like_game(interfaz_life_like)
    elif eleccion == opciones[1]:
        hormiga_game(interfaz_hormiga)
 
 
 
def interfaz_hormiga():
    """
    Descripción: Solicita al usuario los parámetros del autómata Hormiga de Langton mediante easygui.
    Entradas: Ninguna (los valores se capturan por cuadros de diálogo).
    Salidas: lista con los datos ingresados [filas, columnas, tam, direccion].
    Restricciones:
        - Todos los campos deben completarse.
        - Filas, columnas y tamaño de celda deben ser enteros positivos.
        - El campo Dirección solo acepta combinaciones de los caracteres 'L' y 'R'.
    """
    titulo_ventana = "Proyecto 1 Autómatas Celulares - Hormiga de Langton"
    encabezado = "Parámetros Hormiga de Langton"
    campos = ["Filas: ", "Columnas: ", "Tamaño de celda: ", "Dirección (ej: LR): "]
 
    seguir = True
    while seguir:
        sin_dato = False
        no_entero = False
        dir_invalida = False
        datos = g.multenterbox(encabezado, titulo_ventana, campos)
        if datos is None:
            interfaz_principal()
            sys.exit(0)
        encabezado = "Parámetros Hormiga de Langton"
        for i in range(len(datos)):
            if datos[i] == "":
                sin_dato = True
            for caracter in datos[i]:
                if i in [0, 1, 2]:
                    if caracter not in ["0","1","2","3","4","5","6","7","8","9"]:
                        no_entero = True
                else:
                    if caracter not in ["L", "R"]:
                        dir_invalida = True
        if sin_dato or no_entero or dir_invalida:
            encabezado += "\n\nError:"
        if sin_dato:
            encabezado += "\n- Faltan datos por rellenar."
        if no_entero:
            encabezado += "\n- Solo se permiten números enteros positivos."
        if dir_invalida:
            encabezado += "\n- Dirección solo permite\n  combinaciones de 'L' y 'R'."
        if not sin_dato and not no_entero and not dir_invalida:
            seguir = False
 
    return datos
 
 
def hormiga_game(interfaz):
    """
    Descripción: Ejecuta el ciclo principal pygame del autómata Hormiga de Langton.
    Entradas: interfaz (función): función que retorna los parámetros del autómata.
    Salidas: Ninguna (maneja eventos, lógica y renderizado en bucle).
    Restricciones:
        - Requiere pygame y hormiga_logica instalados.
        - El archivo de guardado debe existir antes de intentar cargar.
        - Al cargar, las dimensiones de la matriz guardada deben coincidir con las actuales.
        - Si el archivo cargado contiene más colores que las reglas actuales, se rechaza la carga.
    """
    activo = True
    while activo:
        params = interfaz()
        filas    = int(params[0])
        columnas = int(params[1])
        tam      = int(params[2])
        reglas   = list(params[3])
 
        pos_x   = columnas // 2
        pos_y   = filas // 2
        rumbo   = "arriba"
 
        pygame.init()
        reloj = pygame.time.Clock()
 
        tabla  = ho.generar_matriz_vacia(filas, columnas)
        paleta = ho.generar_colores(len(reglas))
 
        ancho, alto = columnas * tam, filas * tam
        pantalla = pygame.display.set_mode((ancho, alto))
        pantalla.fill(paleta[0])
 
        corriendo = True
        en_pausa  = False
 
        try:
            while corriendo:
                for evento in pygame.event.get():
                    if evento.type == pygame.KEYDOWN:
                        teclas = pygame.key.get_pressed()
 
                        
                        if teclas[pygame.K_SPACE]:
                            en_pausa = not en_pausa
 
                        
                        elif teclas[pygame.K_ESCAPE]:
                            corriendo = False
 
                        
                        elif teclas[pygame.K_b]:
                            tabla = ho.generar_matriz_vacia(filas, columnas)
                            pos_x = columnas // 2
                            pos_y = filas // 2
                            rumbo = "arriba"
                            pantalla.fill(paleta[0])
                            for f in range(filas):
                                for c in range(columnas):
                                    pygame.draw.rect(pantalla, paleta[0], (c * tam, f * tam, tam, tam))
 
                        
                        elif teclas[pygame.K_r]:
                            for f in range(filas):
                                for c in range(columnas):
                                    tabla[f][c] = random.randint(0, len(reglas) - 1)
                            pos_x = columnas // 2
                            pos_y = filas // 2
                            rumbo = "arriba"
                            for f in range(filas):
                                for c in range(columnas):
                                    pygame.draw.rect(pantalla, paleta[tabla[f][c]], (c * tam, f * tam, tam, tam))
 
                        
                        elif teclas[pygame.K_g]:
                            with open("save_hormiga.txt", 'wb') as archivo:
                                datos_guardado = [tabla, rumbo, pos_x, pos_y, reglas]
                                p.dump(datos_guardado, archivo)
 
                        
                        elif teclas[pygame.K_c]:
                            try:
                                with open("save_hormiga.txt", 'rb') as archivo:
                                    datos_guardado = p.load(archivo)
                                tabla_guardada  = datos_guardado[0]
                                reglas_guardadas = datos_guardado[4]
 
                                if len(tabla_guardada) != filas or len(tabla_guardada[0]) != columnas:
                                    print("ERROR: El archivo guardado tiene dimensiones distintas.")
                                else:
                                    valor_max = max(tabla_guardada[f][c]
                                                    for f in range(filas)
                                                    for c in range(columnas))
                                    if valor_max >= len(reglas_guardadas):
                                        print("ERROR: El archivo guardado es incompatible con las reglas actuales.")
                                    else:
                                        tabla  = tabla_guardada
                                        rumbo  = datos_guardado[1]
                                        pos_x  = datos_guardado[2]
                                        pos_y  = datos_guardado[3]
                                        reglas = reglas_guardadas
                                        paleta = ho.generar_colores(len(reglas))
                                        for f in range(filas):
                                            for c in range(columnas):
                                                pygame.draw.rect(pantalla, paleta[tabla[f][c]],
                                                                 (c * tam, f * tam, tam, tam))
                            except FileNotFoundError:
                                print("ERROR: No hay datos de guardado disponibles.")
                            except Exception as e:
                                print(f"ERROR al cargar: {e}")
 
                
                botones = pygame.mouse.get_pressed()
                mx, my  = pygame.mouse.get_pos()
                if botones[0]:
                    fila_click = (my // tam) % filas
                    col_click  = (mx // tam) % columnas
                    tabla[fila_click][col_click] = (tabla[fila_click][col_click] + 1) % len(reglas)
                    pygame.draw.rect(pantalla, paleta[tabla[fila_click][col_click]],
                                     (col_click * tam, fila_click * tam, tam, tam))
 
                
                if not en_pausa:
                    estado_celda = tabla[pos_y][pos_x]
                    rumbo = ho.girar_hormiga(rumbo, reglas[estado_celda])
                    tabla[pos_y][pos_x] = ho.siguiente(estado_celda, reglas)
                    pygame.draw.rect(pantalla, paleta[tabla[pos_y][pos_x]],
                                     (pos_x * tam, pos_y * tam, tam, tam))
                    pos_x, pos_y = ho.avanzar_hormiga(rumbo, pos_x, pos_y)
                    pos_x = pos_x % columnas
                    pos_y = pos_y % filas
 
                pygame.display.update()
                reloj.tick(velocidad)
 
        except Exception as e:
            print(f"ERROR: {e}")
 
        pygame.quit()
 
 
 
def interfaz_life_like():
    """
    Descripción: Solicita al usuario los parámetros del autómata Life-Like mediante easygui.
    Entradas: Ninguna (los valores se capturan por cuadros de diálogo).
    Salidas: lista con los datos ingresados [filas, columnas, tam, nac, sob].
    Restricciones:
        - Todos los campos deben completarse.
        - Filas, columnas y tamaño de celda deben ser enteros positivos.
        - Nacimiento y Sobrevive solo admiten dígitos del '0' al '8'.
    """
    titulo_ventana = "Proyecto 1 Autómatas Celulares - Life-Like Game"
    encabezado = "Parámetros Life-Like Game"
    campos = ["Filas: ", "Columnas: ", "Tamaño de celda: ", "Nacimiento: ", "Sobrevive: "]
 
    seguir = True
    while seguir:
        sin_dato  = False
        no_entero = False
        regla_inv = False
        datos = g.multenterbox(encabezado, titulo_ventana, campos)
        if datos is None:
            interfaz_principal()
            sys.exit(0)
        encabezado = "Parámetros Life-Like Game"
        for i in range(len(datos)):
            if datos[i] == "":
                sin_dato = True
            for caracter in datos[i]:
                if i in [0, 1, 2]:
                    if caracter not in ["0","1","2","3","4","5","6","7","8","9"]:
                        no_entero = True
                else:
                    if caracter not in ["0","1","2","3","4","5","6","7","8"]:
                        regla_inv = True
        if sin_dato or no_entero or regla_inv:
            encabezado += "\n\nError:"
        if sin_dato:
            encabezado += "\n- Faltan datos por rellenar."
        if no_entero:
            encabezado += "\n- Solo se permiten números enteros positivos."
        if regla_inv:
            encabezado += "\n- Nacimiento y Sobrevive solo permiten\n  números enteros positivos del 0 al 8"
        if not sin_dato and not no_entero and not regla_inv:
            seguir = False
 
    return datos
 
 
def life_like_game(interfaz):
    """
    Descripción: Ejecuta el ciclo principal pygame del autómata Life-Like.
    Entradas: interfaz (función): función que retorna los parámetros del autómata.
    Salidas: Ninguna (maneja eventos, lógica y renderizado en bucle).
    Restricciones:
        - Requiere pygame y life_like_logica instalados.
        - El archivo de guardado debe existir antes de intentar cargar.
    """
    activo = True
    while activo:
        params   = interfaz()
        filas    = int(params[0])
        columnas = int(params[1])
        tam      = int(params[2])
        nac      = list(params[3])
        sob      = list(params[4])
 
        pygame.init()
        reloj = pygame.time.Clock()
        tabla = li.generar_matriz_aleatoria(filas, columnas)
 
        ancho, alto = columnas * tam, filas * tam
        pantalla = pygame.display.set_mode((ancho, alto))
 
        corriendo = True
        en_pausa  = False
 
        try:
            while corriendo:
                for evento in pygame.event.get():
                    if evento.type == pygame.KEYDOWN:
                        teclas = pygame.key.get_pressed()
                        if teclas[pygame.K_SPACE]:
                            en_pausa = not en_pausa
                        elif teclas[pygame.K_ESCAPE]:
                            corriendo = False
                        elif teclas[pygame.K_b]:
                            tabla = li.generar_matriz_vacia(filas, columnas)
                        elif teclas[pygame.K_r]:
                            tabla = li.generar_matriz_aleatoria(filas, columnas)
                        elif teclas[pygame.K_g]:
                            with open("save_lifelike.txt", 'wb') as archivo:
                                datos_guardado = [tabla, nac, sob]
                                p.dump(datos_guardado, archivo)
                        elif teclas[pygame.K_c]:
                            with open("save_lifelike.txt", 'rb') as archivo:
                                datos_guardado = p.load(archivo)
                                tabla, nac, sob = datos_guardado[0], datos_guardado[1], datos_guardado[2]
 
                    botones = pygame.mouse.get_pressed()
                    mx, my  = pygame.mouse.get_pos()
                    if botones[0]:
                        fila_click = (my // tam) % filas
                        col_click  = (mx // tam) % columnas
                        tabla[fila_click][col_click] = (tabla[fila_click][col_click] + 1) % 2
 
                pantalla.fill((0, 0, 0))
                for f in range(filas):
                    for c in range(columnas):
                        if tabla[f][c] == 1:
                            px = c * tam
                            py = f * tam
                            pygame.draw.rect(pantalla, (0, 200, 255), (px, py, tam, tam))
                if not en_pausa:
                    tabla = li.transicion(tabla, nac, sob)
                pygame.display.update()
                reloj.tick(velocidad)
 
        except FileNotFoundError:
            print("ERROR: No hay datos de guardado disponibles.")
        except Exception as e:
            print(f"ERROR: {e}")
 
        pygame.quit()
 
 
interfaz_principal()