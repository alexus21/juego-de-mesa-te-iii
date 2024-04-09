from random import randint as r

total_casillas = 80
casillas_seguras = [10, 12, 28, 32, 40, 60, 69]
casillas_penalizacion = [20, 41, 55, 63, 76]
casillas_tiro_doble = [7, 35, 61]
tunel_seguro = [70, 71, 72, 73, 74, 75]

# Variables para manejar el dado
min = 1
max = 6


class Jugador:
    def __init__(self, ficha, numero):
        self.nombre = "Jugador " + str(numero)
        self.ficha = ficha
        self.posicion = 0
        self.contador_tiro_doble = 0
        


def lanzar_dados():
    # retorna dos numeros aleatorios entre 1 y 6
    return r(min, max), r(min, max)


def avanzar_jugador(jugador):

    if jugador.posicion == 0:
        dado1, dado2 = lanzar_dados()

        print(f"{jugador.nombre} ha lanzado los dados: {dado1} y {dado2}")  # imprime el jugador y los dados

        if dado1 == dado2:  # comprobar si saco par
            jugador.posicion += dado1 + dado2  # si es par avance en la posicion
            print(f"{jugador.nombre} avanza a la posición {jugador.posicion}")  # imprino  la posicion del jugador
            return True  # avanza
        else:
            print(f"{jugador.nombre} no saco par no puede avanzar")
            return False  # no avanza
    else:
        dado1, dado2 = lanzar_dados()

        print(f"{jugador.nombre} ha lanzado los dados: {dado1} y {dado2}")  # imprime el jugador y los dados
        jugador.posicion += dado1 + dado2
        print(f"{jugador.nombre} avanza a la posición {jugador.posicion}")  # imprino  la posicion del jugador
        return True


def comprobar_casilla(jugador):
    jugador.contador_tiro_doble += 1
    print(f"Tiros dobles: {jugador.contador_tiro_doble}")

    if jugador.posicion in casillas_seguras or jugador.posicion in tunel_seguro:
        print(f"El {jugador.nombre} está en una casilla segura.")

    if jugador.posicion in casillas_penalizacion:
        print(f"El {jugador.nombre} está en una casilla de penalización. Pierde 5 posiciones.")
        jugador.posicion -= 5

    if jugador.posicion in casillas_tiro_doble:
        print(f"El {jugador.nombre} está en una casilla con derecho a tiro doble.")
        jugador.contador_tiro_doble += 1

    if jugador.contador_tiro_doble == 3:
        print(f"El {jugador.nombre} ha alcanzado el máximo de tiros dobles. Vuelve al inicio")
        jugador.posicion = 0


def imprimir_tablero(jugadores):
    print("\nTablero:")
    total_casillas = 80  # tamaño del tablero
    ancho_casilla = 6  # ancho total de cada celda (incluyendo corchetes y espacios adicionales)
    for i in range(1, total_casillas + 1):  # recorremos el tablero de 1 a total_casillas
        jugador_en_casilla = None
        for jugador in jugadores:
            if jugador.posicion == i:  # se compara si algún jugador coincide con el índice del tablero
                ficha_jugador = f' {jugador.ficha} '  # añadir espacios adicionales a la ficha del jugador
                print(f'[→{ficha_jugador.center(ancho_casilla)}]', end='')  # imprime la ficha del jugador centrada en una celda de ancho fijo
                jugador_en_casilla = True
                break  # para que no siga iterando e imprima más fichas
        if not jugador_en_casilla:
            print(f'[{i:02d}]'.center(ancho_casilla), end='')  # si no hay jugador, imprime la posición centrada en una celda de ancho fijo
        if i % 10 == 0:  # Agregar salto de línea cada 10 casillas
            print()


def get_numero_jugadores():
    while True:
        try:
            # Pedimos cuantos jugadores son
            num_jugadores = int(input("Ingrese el número de jugadores MIN 2 , MAX 4: "))
            # Mínimo 2 jugadores; máximo, 4
            if num_jugadores < 2 or num_jugadores > 4:
                print("El número de jugadores debe estar entre 2 y 4.")
            else:
                return num_jugadores
        except ValueError:
            print("Por favor, ingrese un número válido.")


def mostrar_reglas_del_juego():
    with open("./explicacion-juego.txt", "r") as reglas_juego:
        contenido = reglas_juego.read()
        print(contenido)
        reglas_juego.close()


def main():
    mostrar_reglas_del_juego()
    input("\n\nPresione enter para iniciar...")

    num_jugadores = get_numero_jugadores()  # se llama la funcion get_numero_jugadores

    # lista de jugadores y la posicion de cada uno
    jugadores = [Jugador(f"\033[1;37;4{i+1}m{chr(65 + i)}\033[0m", i + 1) for i in range(num_jugadores)]


    turno = 0
    while True:
        # aca obtenemos el jugador por el turno
        jugador_actual = jugadores[turno]

        # espera que se presione una tecla para que se lanze los dados
        input(f"\n{jugador_actual.nombre}, presiona Enter para lanzar los dados.")

        # se llama la funcion avanzar jugador y se le pasa el jugador actual
        if avanzar_jugador(jugador_actual):
            # Si el jugador actual está en una casilla segura, no se aplica ninguna regla
            if jugador_actual.posicion >= total_casillas:
                print(f"\n¡{jugador_actual.nombre} ha ganado!")
                # ESTO OBVIAMENTE SE VA APLICAR TODAS LAS REGLAS
                return
                # llamo el tablero  despues que un jugador avanza
            imprimir_tablero(jugadores)
            if jugador_actual.posicion > 0:
                turno = (turno + 1) % num_jugadores
        else:
            # Si el jugador no avanza (no saca un par), pasa al siguiente jugador
            turno = (turno + 1) % num_jugadores
        print(f"Turno del jugador {jugadores[turno].nombre}")


if __name__ == "__main__":
    main()  # llamo solamente a la funcion main
