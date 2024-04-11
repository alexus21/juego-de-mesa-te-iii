from random import randint as r

total_casillas = 80
casillas_seguras = [10, 12, 28, 32, 40, 60, 69]
casillas_penalizacion = [20, 41, 55, 63, 76]
casillas_tiro_doble = [7, 35, 61]
tunel_seguro = [70, 71, 72, 73, 74, 75]

# Variables para manejar el dado
min = 1
max = 6

# Variables de penalizacion y puntos del juego:
penalizacion_casilla_penalizacion = 5
posiciones_ficha_comida = 10
maximo_tiros_dobles = 3


class Jugador:
    def __init__(self, ficha, numero):
        self.nombre = "Jugador " + str(numero)
        self.ficha = ficha
        self.posicion = 0
        self.contador_tiro_doble = 0
        self.derecho_tiro_doble = False
        self.victoria = False


def lanzar_dados():
    # retorna dos numeros aleatorios entre 1 y 6
    return r(min, max), r(min, max)


def avanzar_jugador(jugador, jugadores):  # Agregado el parámetro 'jugadores' aquí
    if jugador.posicion == 0:
        dado1, dado2 = lanzar_dados()

        print(f"{jugador.nombre} ha lanzado los dados: {dado1} y {dado2}")  # imprime el jugador y los dados

        if dado1 == dado2:  # comprobar si saco par
            jugador.posicion += dado1 + dado2  # si es par avance en la posicion
            print(f"{jugador.nombre} avanza a la posición {jugador.posicion}")  # imprimo la posicion del jugador
            comprobar_casilla(jugador, jugadores)  # se llama la funcion comprobar casilla
            return True  # avanza
        else:
            print(f"{jugador.nombre} no saco par no puede avanzar")
            return False  # no avanza

    else:
        dado1, dado2 = lanzar_dados()

        print(f"{jugador.nombre} ha lanzado los dados: {dado1} y {dado2}")  # imprime el jugador y los dados
        jugador.posicion += dado1 + dado2
        if jugador.posicion > total_casillas:
            jugador.posicion = total_casillas
            jugador.victoria = True
        print(f"{jugador.nombre} avanza a la posición {jugador.posicion}")  # imprimo la posicion del jugador

        

        if dado1 == dado2:
            if jugador.posicion>=80:
                print()
            else:    
                print(f"¡{jugador.nombre} ha sacado un par! Tiene derecho a un tiro doble.")
                jugador.contador_tiro_doble += 1
                jugador.derecho_tiro_doble = True

        else:
            # print(f"{jugador.nombre} no ha sacado un par, pierde el derecho a tirar nuevamente.")
            jugador.derecho_tiro_doble = False
            jugador.contador_tiro_doble = 0

        comprobar_casilla(jugador, jugadores)  # se llama la funcion comprobar casilla
        return True


def comprobar_casilla(jugador, jugadores):
    if jugador.victoria is False:
        # La casilla segura no aplica la sanción de tiro doble (volver al inicio,
        # solo afecta a la cantidad de tiros dobles si esta es mayor o igual a 3)
        if jugador.posicion in casillas_seguras or jugador.posicion in tunel_seguro:
            print(f"El {jugador.nombre} está en una casilla segura.")
            if jugador.contador_tiro_doble >= maximo_tiros_dobles:
                jugador.contador_tiro_doble = 0
                jugador.derecho_tiro_doble = False
            return

        if jugador.posicion in casillas_penalizacion:
            print(
                f"El {jugador.nombre} está en una casilla de penalización. Pierde {penalizacion_casilla_penalizacion} posiciones.")
            jugador.posicion -= penalizacion_casilla_penalizacion

        if jugador.posicion in casillas_tiro_doble:
            print(f"El {jugador.nombre} está en una casilla con derecho a tiro doble.")
            jugador.contador_tiro_doble += 1
            jugador.derecho_tiro_doble = True
            return

        for comer_jugador in jugadores:
            if comer_jugador != jugador and comer_jugador.posicion == jugador.posicion:
                print(f"El {jugador.nombre} ha alcanzado a {comer_jugador.nombre}. ¡Se come la ficha de {comer_jugador.nombre}! y avanza {posiciones_ficha_comida} posiciones.")
                jugador.posicion += posiciones_ficha_comida
                jugador.contador_tiro_doble = 0
                jugador.derecho_tiro_doble = False
                if comer_jugador.posicion < 10:
                    print(
                        f"El {comer_jugador.nombre} vuelve al inicio.")
                    comer_jugador.posicion = 0
                else:
                    print(
                        f"El {comer_jugador.nombre} pierde {posiciones_ficha_comida} posiciones.")
                    comer_jugador.posicion -= posiciones_ficha_comida
                # print( f"¡El {jugador.nombre} ha ganado {posiciones_ficha_comida} posiciones por comer la ficha de {jugador.nombre} !")
                return

        if jugador.contador_tiro_doble >= maximo_tiros_dobles and jugador.derecho_tiro_doble:
            print(f"El {jugador.nombre} ha alcanzado el máximo de tiros dobles. Vuelve al inicio")
            jugador.posicion = 0
            jugador.contador_tiro_doble = 0
            jugador.derecho_tiro_doble = False


def imprimir_tablero(jugadores, casillas_seguras, casillas_penalizacion, casillas_tiro_doble, tunel_seguro):
    print("\n→→→→→→→→→→→→→→→→→→→→→→→→→  TABLERO  ←←←←←←←←←←←←←←←←←←←←←←←←")
    print("\n")
    print("\033[92mCASILLA SEGURA\033[0m")
    print("\033[91mCASILLA DE PENALIZACION\033[0m")
    print("\033[93mCASILLA DE TIRO DOBLE\033[0m")
    print("\033[96mTUNEL SEGURO\033[0m")
    print("\n")

    ancho_casilla = 6  # ancho total de cada celda (incluyendo corchetes y espacios adicionales)
    for i in range(1, total_casillas + 1):  # recorremos el tablero de 1 a total_casillas
        # Verificar el tipo de casilla
        if i in casillas_seguras:
            color_inicio = "\033[92m"  # color verde para casillas seguras
            color_fin = "\033[0m"  # restablecer el color
        elif i in casillas_penalizacion:
            color_inicio = "\033[91m"  # color rojo para casillas de penalización
            color_fin = "\033[0m"  # restablecer el color
        elif i in casillas_tiro_doble:
            color_inicio = "\033[93m"  # color amarillo para casillas de tiro doble
            color_fin = "\033[0m"  # restablecer el color
        elif i in tunel_seguro:
            color_inicio = "\033[96m"  # color cyan para túneles seguros
            color_fin = "\033[0m"  # restablecer el color
        else:
            color_inicio = ""  # no se cambia el color
            color_fin = ""  # no se cambia el color

        jugador_en_casilla = None
        for jugador in jugadores:
            if jugador.posicion == i:  # se compara si algún jugador coincide con el índice del tablero
                ficha_jugador = f' {jugador.ficha} '  # añadir espacios adicionales a la ficha del jugador
                print(f'[→{color_inicio}{ficha_jugador.center(ancho_casilla)}{color_fin}]',
                      end='')  # imprime la ficha del jugador centrada en una celda de ancho fijo con color
                jugador_en_casilla = True
                break  # para que no siga iterando e imprima más fichas
        if not jugador_en_casilla:
            casilla = f'[{i:02d}]'.center(
                ancho_casilla)  # si no hay jugador, imprime la posición centrada en una celda de ancho fijo
            if i in casillas_seguras or i in casillas_penalizacion or i in casillas_tiro_doble or i in tunel_seguro:
                casilla = color_inicio + casilla + color_fin  # aplicar color si es una casilla especial
            print(casilla, end='')
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
    jugadores = [Jugador(f"\033[1;37;4{i + 1}m{chr(65 + i)}\033[0m", i + 1) for i in range(num_jugadores)]

    turno = 0
    while jugadores[turno].victoria is False:
        # aca obtenemos el jugador por el turno
        jugador_actual = jugadores[turno]

        # espera que se presione una tecla para que se lanze los dados
        print("*" * 75)
        input(f"\n{jugador_actual.nombre}, presiona Enter para lanzar los dados.")

        # se llama la funcion avanzar jugador y se le pasa el jugador actual
        if avanzar_jugador(jugador_actual, jugadores):
            # Si el jugador actual está en una casilla segura, no se aplica ninguna regla
            if jugador_actual.posicion >= total_casillas:
                print(f"\n¡{jugador_actual.nombre} ha ganado!")
                print("\n→→→→→→→→→→→→→→→→→→→→→JUEGO TERMINADO←←←←←←←←←←←←←←←←←←←←")
                imprimir_tablero(jugadores, casillas_seguras, casillas_penalizacion, casillas_tiro_doble, tunel_seguro)
                break  # Salir del bucle si un jugador ha ganado

            # llamo el tablero  despues que un jugador avanza
            imprimir_tablero(jugadores, casillas_seguras, casillas_penalizacion, casillas_tiro_doble, tunel_seguro)
            if jugador_actual.posicion > 0:
                turno = (turno + 1) % num_jugadores

            if jugador_actual.derecho_tiro_doble:
                # El jugador ya tiene derecho a un tiro doble
                # Permitir múltiples tiros dobles si se siguen obteniendo
                while jugador_actual.derecho_tiro_doble:
                    # Esperar que el jugador presione una tecla para lanzar los dados nuevamente
                    input(f"\n{jugador_actual.nombre}, presiona Enter para lanzar los dados nuevamente.")

                    # Realizar el segundo lanzamiento
                    if avanzar_jugador(jugador_actual, jugadores):
                        imprimir_tablero(jugadores, casillas_seguras, casillas_penalizacion, casillas_tiro_doble,
                                         tunel_seguro)
                        print("\n→→→→→→→→→→→→→→→→→→→→→TURNO TERMINADO←←←←←←←←←←←←←←←←←←←←")

                    # Verificar si el jugador obtuvo otro tiro doble
                    if jugador_actual.derecho_tiro_doble:
                        # Si sí, permitir que el mismo jugador lance nuevamente
                        continue
                    else:
                        # Si no, cambiar al siguiente jugador
                        break
        else:
            # Si el jugador no tiene derecho a un tiro doble, cambiar al siguiente jugador
            turno = (turno + 1) % num_jugadores


if __name__ == "__main__":
    main()  # llamo solamente a la funcion main arreglalo como paso ese otro parametro donde aveces lo llamo en otro lado no funciona
