import random

from jugador import Jugador


def lanzar_dados():
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6) #generamos los dados
    return dado1, dado2

def avanzar_jugador(jugador):
    #se llama la funcion y se le asigna los datos de dado 1 y 2
    dado1, dado2 = lanzar_dados()

    print(f"{jugador.nombre} ha lanzado los dados: {dado1} y {dado2}")#imprime el jugador y los dados
    
    if dado1 == dado2: #comprobar si saco par

        jugador.posicion += dado1 + dado2 #si es par avance en la posicion
        print(f"{jugador.nombre} avanza a la posición {jugador.posicion}")#imprino  la posicion del jugador
        return True #avanza
    else:
        print(f"{jugador.nombre} no saco par no puede avanzar")
        return False #no avanza




def imprimir_tablero(jugadores):
    print("\nTablero:")
    for i in range(80): #tamaño del tablero
        #recorremos los jugadores
        for jugador in jugadores:
            if jugador.posicion == i: #se compara si algun jugador coincide con el indice del tablero
                print(jugador.ficha, end='') #si es asi imprime la ficha que es una por default
                break #para que no siga iterando e imprima mas fichas
        else:
            print('-', end='') #si no hay nada imprime un guion o podria ser la psicion en si a mostrar queda a decision
    print()

def jugar():
    print(".......BIENVENIDOS AL JUEGO DE MESA........")
    num_jugadores = int(input("Ingrese el número de jugadores MIN 2 , MAX 4: ")) #pedimos cuantos jugadores son 
    if num_jugadores < 2 or num_jugadores > 4: #le deje minimo 2 y maximi 4 
        print("El número de jugadores debe estar entre 2 y 4.")
        return

    jugadores = [Jugador(chr(65 + i), i + 1) for i in range(num_jugadores)]   #lista de jugadores y la posicion esto si no muy bien como funciona fue crtl c y crtlv xd     
  #pero imprime A B C D asi el indicador

    turno = 0
    while True:
        jugador_actual = jugadores[turno] #aca obtenemos el jugador por el turno



        input(f"\n{jugador_actual.nombre}, presiona Enter para lanzar los dados.") #espera que se presione una tecla para que se lanze los dados
        if avanzar_jugador(jugador_actual): #se llama la funcion avanzar jugador y se le pasa el jugador actual 
            if jugador_actual.posicion >= 80:   #se verifica si el jugador actual en la posicion supera a 80 gano
                print(f"\n¡{jugador_actual.nombre} ha ganado!")
                return      #ESTO OBVIAMENTE SE VA APLICAR TODAS LAS REGLAS
            imprimir_tablero(jugadores)  #llamo el tablero  despues que un jugador avanza
        else:
             # Si el jugador no avanza (no saca un par), pasa al siguiente jugador
            turno = (turno + 1) % num_jugadores

if __name__ == "__main__":
    jugar() #llamo solamente a la funcion jugar

