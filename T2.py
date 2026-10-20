#Cesar Arredondo (n00416238) 

import time

N = 9
PUNTOS_MIN = 23
PAUSA = 0 

LABERINTO = [
    [1, 1, 1, 3, 0, 1, 1, 1, 4],  
    [3, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 3, 1, 1],
    [3, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 3, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 4],
    [1, 1, 3, 1, 0, 1, 1, 1, 1],   
]

INICIO = (8, 0)   
FIN = (0, 0)      

MOVIMIENTOS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
FLECHAS = {(-1, 0): "↑", (0, 1): "→", (1, 0): "↓", (0, -1): "←"}

visitado = [[False] * N for _ in range(N)]
camino = []          
solucion = []        
contador_nodos = 0   

mejor_a_F = []           
mejor_a_F_puntos = -1    
mas_cercano = []         
mas_cercano_dist = 10**9 


def imprimir_laberinto_original():
    print("LABERINTO ORIGINAL (F = llegada, I = inicio, 0 = pared)")
    print()
    for i in range(N):
        fila = ""
        for j in range(N):
            if (i, j) == FIN:
                fila += "  F"
            elif (i, j) == INICIO:
                fila += "  I"
            elif LABERINTO[i][j] == 0:
                fila += "  0"
            else:
                fila += f"{LABERINTO[i][j]:3d}"
        print(fila)
    print()


def imprimir_solucion(ruta, actual=None,
                      titulo="MATRIZ CON EL CAMINO (flechas = direccion del movimiento)"):
    marca = {}
    for k in range(len(ruta) - 1):
        a, b = ruta[k], ruta[k + 1]
        marca[a] = FLECHAS[(b[0] - a[0], b[1] - a[1])]
    print(titulo)
    print()
    for i in range(N):
        fila = ""
        for j in range(N):
            if (i, j) == FIN:
                fila += "  F"
            elif (i, j) == actual:
                fila += "  R"
            elif (i, j) in marca:
                fila += f"  {marca[(i, j)]}"
            elif LABERINTO[i][j] == 0:
                fila += "  0"
            else:
                fila += "  ."
        print(fila)
    print()


def mostrar_recorrido(ruta):
    total = len(ruta) - 1
    for k in range(1, len(ruta)):
        f, c = ruta[k]
        imprimir_solucion(ruta[:k + 1], actual=ruta[k],
                          titulo=f"PASO {k} de {total}: el raton avanza a ({f},{c})"
                                 f"  (R = raton)")
        time.sleep(PAUSA)


def construye_candidatos(fila, col):
    candidatos = []
    for df, dc in MOVIMIENTOS:
        nf, nc = fila + df, col + dc
        if 0 <= nf < N and 0 <= nc < N:           
            if LABERINTO[nf][nc] != 0:            
                if not visitado[nf][nc]:          
                    candidatos.append((nf, nc))
    return candidatos


def BT(fila, col, puntos):
    global solucion, contador_nodos
    global mejor_a_F, mejor_a_F_puntos, mas_cercano, mas_cercano_dist
    contador_nodos += 1

    if (fila, col) == FIN:
        if puntos >= PUNTOS_MIN:
            solucion = list(camino)
            return True
        if puntos > mejor_a_F_puntos:
            mejor_a_F = list(camino)
            mejor_a_F_puntos = puntos
        return False          # retroceder

    dist = abs(fila - FIN[0]) + abs(col - FIN[1])
    if dist < mas_cercano_dist:
        mas_cercano = list(camino)
        mas_cercano_dist = dist

    for (nf, nc) in construye_candidatos(fila, col):
        valor = LABERINTO[nf][nc]
        ganado = valor if valor >= 3 else 0     

        visitado[nf][nc] = True
        camino.append((nf, nc))

        if BT(nf, nc, puntos + ganado):
            return True

        camino.pop()
        visitado[nf][nc] = False

    return False


def main():
    imprimir_laberinto_original()

    visitado[INICIO[0]][INICIO[1]] = True
    camino.append(INICIO)

    if BT(INICIO[0], INICIO[1], 0):

        mostrar_recorrido(solucion)

        puntos = sum(LABERINTO[f][c] for f, c in solucion if LABERINTO[f][c] >= 3)
        print(f"¡El raton logro salir! Puntos acumulados: {puntos} (minimo {PUNTOS_MIN})")
        print(f"Pasos del camino: {len(solucion) - 1}")
        print()
        imprimir_solucion(solucion)
        print("Camino (fila, columna):")
        print(" -> ".join(f"({f},{c})" for f, c in solucion))
    else:
        if mejor_a_F:
            ruta = mejor_a_F
        else:
            ruta = mas_cercano
        mostrar_recorrido(ruta)

        if mejor_a_F:
            print(f"El raton no logro salir: llego a F pero con {mejor_a_F_puntos} puntos "
                  f"(necesita {PUNTOS_MIN} o mas)")
        else:
            print("El raton no logro salir: no existe camino hasta F "
                  "(las paredes lo bloquean).")
            print(f"Llego lo mas cerca posible, hasta la celda {ruta[-1]}.")
        print(f"Pasos del recorrido: {len(ruta) - 1}")
        print()
        imprimir_solucion(ruta, actual=ruta[-1])
        print("Camino (fila, columna):")
        print(" -> ".join(f"({f},{c})" for f, c in ruta))


if __name__ == "__main__":
    main()