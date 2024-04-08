import random


class Parchis:
    def __init__(self, num_jugadores=2, num_fichas_por_jugador=1):
        self.num_jugadores = num_jugadores
        self.num_fichas_por_jugador = num_fichas_por_jugador
        self.tam_tablero = 80
        self.casillas_seguras = [9, 11, 27, 31, 39, 59, 68]  # Casillas seguras (llegada)
        self.casillas_penalizacion = [19, 40, 54, 62, 75]  # Casillas de penalización
        self.casillas_tiro_doble = [6, 34, 60]  # Casillas de tirada doble
        self.casillas_tunel_seguridad = [69, 74]  # Casillas de tunel de seguridad
        self.jugadores = {chr(65 + i): Jugador(num_fichas_por_jugador) for i in range(self.num_jugadores)}
        self.turno = 0
        self.contador_dobles = 0

    def iniciar(self):
        print("Comenzando juego de Parchís con {} jugadores y {} fichas por jugador.".format(self.num_jugadores,
                                                                                             self.num_fichas_por_jugador))
        print("¡Que empiece el juego!")

    def lanzar_dados(self):
        return random.randint(1, 6), random.randint(1, 6)

    def modificar_posicion(self, nueva_posicion, jugador, dado_1, dado_2):
        if nueva_posicion > 80:
            print("Sigue en el mismo lugar")

        if nueva_posicion == 80:
            jugador.mover_ficha(1, sum([dado_1, dado_2]))
            print("¡El jugador ha llegado al final de todo!")
            return True

        casillas_ocupadas = [ficha for jugador in self.jugadores.values() for ficha in jugador.fichas]

        if nueva_posicion in self.casillas_seguras:
            jugador.mover_ficha(1, sum([dado_1, dado_2]))
            print("¡El jugador ha llegado a un tunel de seguridad!")
        elif nueva_posicion in self.casillas_penalizacion:
            jugador.mover_ficha(1, sum([dado_1, dado_2]))
            print("¡El jugador ha caído en una casilla de penalización!, pierde turno")
            jugador.turno_perdido = True
        elif nueva_posicion in self.casillas_tiro_doble:
            jugador.mover_ficha(1, sum([dado_1, dado_2]))
            print("¡El jugador ha caído en una casilla de tiro doble!")
            return False
        # Validar la variable nueva_posicion con todas las posiciones de los demás jugadores Si la posición
        # nueva_posicion es igual a alguna de las posiciones de los demás jugadores entonces validar si
        # está en tunel de seguridad, si no, entonces mover la ficha a la casilla de inicio
        elif nueva_posicion in casillas_ocupadas:
            if nueva_posicion in self.casillas_tunel_seguridad:
                jugador.mover_ficha(1, sum([dado_1, dado_2]))
                print("¡El jugador ha caído en un tunel de seguridad!")
            else:
                jugador.reiniciar_fichas()
                print("¡El jugador ha caído en una casilla ocupada!, regresa a la casilla de inicio")
        else:
            jugador.mover_ficha(1, sum([dado_1, dado_2]))

        self.turno = (self.turno + 1) % self.num_jugadores

        return False

    def jugar_turno(self):
        id_jugador = chr(65 + self.turno)
        jugador = self.jugadores[id_jugador]

        while jugador.turno_perdido:
            jugador.turno_perdido = False
            self.turno = (self.turno + 1) % self.num_jugadores
            id_jugador = chr(65 + self.turno)
            jugador = self.jugadores[id_jugador]

        dado_1, dado_2 = self.lanzar_dados()

        print("El jugador {} ha sacado {} y {}".format(id_jugador, dado_1, dado_2))

        # Verificar si el jugador puede iniciar sus fichas
        if not jugador.iniciado:
            if sum([dado_1, dado_2]) % 2 == 0:
                jugador.iniciar()
                print("¡El jugador {} ha iniciado!".format(id_jugador))
                self.contador_dobles = 0
                self.turno = (self.turno + 1) % self.num_jugadores
            else:
                print("El jugador {} no ha sacado una suma par para iniciar las fichas.".format(id_jugador))
        else:
            print("El jugador {} ha sacado {} y {}".format(id_jugador, dado_1, dado_2))

            nueva_posicion = jugador.fichas[0] + sum([dado_1, dado_2])

            if dado_1 == dado_2:
                self.contador_dobles += 1
                if self.contador_dobles == 3:
                    jugador.reiniciar_fichas()
                    print(
                        "¡El jugador {} ha sacado 3 dobles seguidos y ha perdido todas sus fichas!".format(id_jugador))
                else:
                    print("¡El jugador {} ha sacado un doble!".format(id_jugador))
                    return self.modificar_posicion(nueva_posicion, jugador, dado_1, dado_2)
            else:
                return self.modificar_posicion(nueva_posicion, jugador, dado_1, dado_2)

        return False

    def mostrar_tablero(self):
        for i in range(1, self.tam_tablero + 1):
            jugador_en_casilla = None
            for id_jugador, jugador in self.jugadores.items():
                for ficha, posicion_ficha in enumerate(jugador.fichas, start=1):
                    if posicion_ficha == i:
                        jugador_en_casilla = id_jugador + str(ficha)
                        break
                if jugador_en_casilla:
                    break
            if jugador_en_casilla:
                print(f"[{jugador_en_casilla}]", end=" ")
            else:
                print(f"[{i:02d}]", end=" ")
            if i % 10 == 0:  # Agregar salto de línea cada 10 casillas
                print()


class Jugador:
    def __init__(self, num_fichas):
        self.fichas = [0] * num_fichas
        self.iniciado = False
        self.turno_perdido = False

    def iniciar(self):
        for i in range(len(self.fichas)):
            self.fichas[i] = 1
        self.iniciado = True

    def mover_ficha(self, ficha, pasos):
        self.fichas[ficha - 1] += 5
        if self.fichas[ficha - 1] > 80:
            self.fichas[ficha - 1] = 80
            print("¡El jugador ha llegado al final!")

        print(ficha - 1, pasos, self.fichas[ficha - 1])

    def reiniciar_fichas(self):
        for i in range(len(self.fichas)):
            self.fichas[i] = 0
        self.iniciado = False


# Función principal para iniciar el juego
def main():
    num_jugadores = int(input("Ingrese el número de jugadores: "))
    num_fichas_por_jugador = int(input("Ingrese el número de fichas por jugador: "))
    juego = Parchis(num_jugadores)
    juego.iniciar()

    while True:
        validar = juego.jugar_turno()
        juego.mostrar_tablero()
        if validar:
            break
        print(validar)
        input("Presiona Enter para continuar...")


if __name__ == "__main__":
    main()
