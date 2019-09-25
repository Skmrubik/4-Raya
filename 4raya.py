import numpy as np 
import pygame
import sys
import math

BLUE = (0,0,255)
RED = (255,0,0)
BLACK =(0,0,0)
YELLOW = (255,255,0)

CONT_FILAS=6
CONT_COLUMNAS=7

def crear_tablero():
    tablero = np.zeros((CONT_FILAS,CONT_COLUMNAS))
    return tablero

def tirar_ficha(tablero, fil, col, ficha):
    tablero[fil][col] = ficha

def es_columna_valida(tablero, col):
    return tablero[CONT_FILAS-1][col] == 0

def get_proxima_fila_abierta(tablero, col):
    for f in range(CONT_FILAS):
        if tablero[f][col] == 0:
            return f

def pintar_tablero(tablero):
    print(np.flip(tablero,0))

def movimiento_ganador(tablero, ficha):
    
    for c in range(CONT_COLUMNAS):
        cont = 0
        for f in range(CONT_FILAS):
            if tablero[f][c] == ficha:
                cont += 1
            else:
                cont = 0

            if cont == 4:
                return True
    
    for f in range(CONT_FILAS):
        cont = 0
        for c in range(CONT_COLUMNAS):
            if tablero[f][c] == ficha:
                cont += 1
            else:
                cont = 0

            if cont == 4:
                return True
    
    for c in range(CONT_COLUMNAS-3):
        for f in range(CONT_FILAS-3):
            if tablero[f][c] == ficha and tablero[f+1][c+1] == ficha and tablero[f+2][c+2] == ficha and tablero[f+3][c+3] == ficha:
                return True
                
    for c in range(CONT_COLUMNAS-3):
        for f in range(3,CONT_FILAS):
            if tablero[f][c] == ficha and tablero[f-1][c+1] == ficha and tablero[f-2][c+2] == ficha and tablero[f-3][c+3] == ficha:
                return True

def dibujar_tablero(tablero):
     
    for c in range(CONT_COLUMNAS):
        for f in range (CONT_FILAS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, f*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(f*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)
    for c in range(CONT_COLUMNAS):
        for f in range (CONT_FILAS):
            if tablero[f][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(f*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif tablero[f][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(f*SQUARESIZE+SQUARESIZE/2)),RADIUS)
    pygame.display.update()


tablero = crear_tablero()  
print (tablero)  
game_over = False
turno = 0

pygame.init()

SQUARESIZE = 100

width = CONT_COLUMNAS * SQUARESIZE
height = (CONT_FILAS+1) * SQUARESIZE

size = (width,height)

RADIUS = int(SQUARESIZE/2 -5)

screen = pygame.display.set_mode(size)
dibujar_tablero(tablero)
pygame.display.update()

myfont = pygame.font.SysFont("monospace",75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0,width, SQUARESIZE))
            posx = event.pos[0]
            if turno == 0:
                pygame.draw.circle(screen, RED, (posx,int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx,int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)
            #Preguntar por el jugador 1
            if turno == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if es_columna_valida(tablero, col):
                    fila = get_proxima_fila_abierta(tablero, col)
                    tirar_ficha(tablero, fila, col, 1)
                    turno = (turno+ 1) % 2
                    pygame.draw.circle(screen, YELLOW, (posx,int(SQUARESIZE/2)), RADIUS)
                    print(turno)
                    if(movimiento_ganador(tablero, 1)):
                        print("Jugador 1 GANA!")
                        label = myfont.render("JUGADOR 1 GANA", 1, RED)
                        screen.blit(label,(40,10))
                        game_over = True
                        
            #Preguntar por el jugador 2
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if es_columna_valida(tablero, col):
                    fila = get_proxima_fila_abierta(tablero, col)
                    tirar_ficha(tablero, fila, col, 2)
                    turno = (turno+ 1) % 2
                    pygame.draw.circle(screen, RED, (posx,int(SQUARESIZE/2)), RADIUS)
                    print(turno)
                    if(movimiento_ganador(tablero, 2)):
                        print("Jugador 2 GANA!")
                        label = myfont.render("JUGADOR 2 GANA", 1, YELLOW)
                        screen.blit(label,(40,10))
                        game_over = True
            pygame.display.update()
        print(pintar_tablero(tablero))
        dibujar_tablero(tablero)
            
        #turno = turno % 2

        if game_over:
            pygame.time.wait(5000)
