from tablero import crear_tablero, crear_piezas
from logica import suma_dados, turno_jugador,movimiento_pieza

mode = input("Modo de juego d/j: ")

def jugar_ludo():
    orden = ["🟥 Rojo", "🟩 Verde", "🟦 Azul", "🟨Amarillo"]
    tablero = crear_tablero()
    piezas = crear_piezas()
    x="s"
    while x=="s":
        color = orden[0]
        print(f"Turno del jugador {color}")
        dados_actuales = suma_dados(mode)
        movimiento_pieza(piezas, dados_actuales, tablero=tablero, color=color,turno=turno_jugador(color, piezas, tablero, dados_actuales))
        x=input("Continuar s/n: ")
        color = orden[0]
        orden.append(orden.pop(0))
        if x =="n":
            break

    return color

jugar_ludo()