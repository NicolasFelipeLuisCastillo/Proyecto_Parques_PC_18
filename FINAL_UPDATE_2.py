import random

mode = input("Modo de juego d/j: ") 

# TABLERO

def crear_tablero():
    seguros = [5,17,22,34,39,51,56,68]
    salidas = [12,29,46,63]
    colores = ["🟥 Rojo", "🟩 Verde", "🟦 Azul", "🟨Amarillo"]
    tablero = []
    for i in range(1,69):
        if 1 <= i <=16:
            color = colores[0]
        elif 17 <= i <=33:
            color = colores[1]
        elif 34 <= i <=50:
            color = colores[2]
        elif 51 <= i <=68:
            color = colores[3]
        casillas = {"Casilla":i,"Color":color,"Seguro": i in seguros,"Salida": i in salidas}
        tablero.append(casillas)
    return tablero

zona_llegada = {
    "🟥 Rojo": list(range(69, 77)),
    "🟩 Verde": list(range(77, 85)),
    "🟦 Azul": list(range(85, 93)),
    "🟨Amarillo": list(range(93, 101))
}

entrada_llegada = {
    "🟥 Rojo": 68,
    "🟩 Verde": (29 + 56 - 1) % 68 + 1,
    "🟦 Azul": (46 + 56 - 1) % 68 + 1,
    "🟨Amarillo": (63 + 56 - 1) % 68 + 1
}

def crear_piezas():
    piezas = []
    colores = ["🟥 Rojo", "🟩 Verde", "🟦 Azul", "🟨Amarillo"]
    for color in colores:
        for i in range(1, 5):
            pieza = {"ID":i,"Color": color, "Casilla":0,"Salio":False, "Llego": False}
            piezas.append(pieza)
    return piezas

# LANZAMIENTO DE DADOS
def suma_dados():
    if mode == "d":
        d1 = int(input("Ingrese el valor del dado 1 (1-6): "))
        d2 = int(input("Ingrese el valor del dado 2 (1-6): "))
    else:
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
    print(f"[🎲 Lanzamiento de dados] => ({d1}, {d2})")
    return d1, d2

def obtener_salida(color):
    if color == "🟥 Rojo":
        return 12
    elif color == "🟩 Verde":
        return 29
    elif color == "🟦 Azul":
        return 46
    elif color == "🟨Amarillo":
        return 63 

def turno_jugador(color, piezas, tablero, dados):
    turno = False
    pasos = sum(dados)

    tiene_fichas_fuera = any(p["Color"] == color and p["Salio"] for p in piezas)
    puede_sacar = pasos == 5 or dados[0] == 5 or dados[1] == 5

    if puede_sacar:
        fichas_en_base = [p for p in piezas if p["Casilla"] == 0 and p["Color"] == color]
        if fichas_en_base:
            print("¡Felicidades! Has sacado un 5 y puedes sacar una pieza de la base.")
            while True:
                try:
                    escoger = int(input("Ingrese la ficha que desea sacar (1-4): "))
                except ValueError:
                    print("⚠️ Ingrese un número válido.")
                    continue
                ficha_escogida = next((p for p in fichas_en_base if p["ID"] == escoger), None)
                if ficha_escogida:
                    salida = obtener_salida(color)
                    fichas_en_salida = [p for p in piezas if p["Casilla"] == salida and p["Color"] == color]
                    if len(fichas_en_salida) >= 2:
                        print("🚫 No puedes sacar ficha: la salida está ocupada por 2 fichas de tu equipo.")
                        return tiene_fichas_fuera
                    ficha_escogida["Casilla"] = salida
                    ficha_escogida["Salio"] = True
                    return True
                else:
                    print("❌ Esa ficha no está en la base o no es válida.")
        else:
            print("Sacaste un 5, pero no tienes fichas en la base.")
            return tiene_fichas_fuera

    return tiene_fichas_fuera

def hay_bloqueo_en_rango(piezas, color, origen, destino):
    for i in range(origen + 1, destino + 1):
        fichas_en_casilla = [p for p in piezas if p["Casilla"] == i]
        if len(fichas_en_casilla) == 2 and fichas_en_casilla[0]["Color"] == fichas_en_casilla[1]["Color"]:
            return True
    return False

def aplicar_bonus(color, piezas, bonus):
    print(f"🎁 Bonus de {bonus} movimientos para {color}. Puedes aplicarlo a cualquier ficha de tu equipo.")
    while True:
        try:
            escoger = int(input("Ingrese el ID de la ficha a mover con el bonus: "))
        except ValueError:
            print("⚠️ Ingrese un número válido.")
            continue
        for p in piezas:
            if p["Color"] == color and p["Salio"] and not p["Llego"] and p["ID"] == escoger:
                nueva_pos = p["Casilla"] + bonus
                if nueva_pos <= 68:
                    p["Casilla"] = nueva_pos
                    print(f"La ficha {p['Color']} ID {p['ID']} se mueve a {nueva_pos} con el bonus.")
                else:
                    print("⚠️ No puedes usar el bonus porque sobrepasarías el tablero.")
                return
        print("Ficha inválida o no ha salido.")

def movimiento_pieza(piezas, dados, tablero, color, turno):
    if not turno:
        print("No se puede mover ninguna pieza porque no se ha sacado un 5 y no hay fichas afuera.")
        return

    pasos = sum(dados)
    print(f"Pasos a mover: {pasos}")

    while True:
        try:
            escoger = int(input("Ingrese la ficha que desea mover (1-4): "))
        except ValueError:
            print("⚠️ Debe ingresar un número válido.")
            continue

        ficha_valida = next((p for p in piezas if p["ID"] == escoger and p["Color"] == color and p["Salio"] and not p["Llego"]), None)

        if ficha_valida:
            origen = ficha_valida["Casilla"]

            #   Llegar a la meta (+10 bonus)
            if origen in zona_llegada[color]:
                idx_actual = zona_llegada[color].index(origen)
                idx_nuevo = idx_actual + pasos
                if idx_nuevo > 7:
                    print("❌ Movimiento no permitido. Debes sacar la cantidad exacta para llegar a la meta.")
                    return
                ficha_valida["Casilla"] = zona_llegada[color][idx_nuevo]
                if idx_nuevo == 7:
                    ficha_valida["Llego"] = True
                    print(f"🏁 ¡La ficha {ficha_valida['ID']} ha llegado a la meta!")
                    aplicar_bonus(color, piezas, 10)  # bonus por llegar

            else:
                nueva_posicion = origen + pasos
                entrada = entrada_llegada[color]
                if origen <= entrada < nueva_posicion:
                    pasos_en_zona = nueva_posicion - entrada
                    if pasos_en_zona > 8:
                        print("❌ Movimiento no permitido. Debes sacar la cantidad exacta para entrar a la llegada.")
                        return
                    ficha_valida["Casilla"] = zona_llegada[color][pasos_en_zona - 1]
                else:
                    if nueva_posicion > 68:
                        nueva_posicion %= 68


                    #   Bloqueo

                    if hay_bloqueo_en_rango(piezas, color, origen, nueva_posicion):
                        print("🚧 No puedes pasar: hay un bloqueo en el camino.")
                        return

                    mismas_pos = [p for p in piezas if p["Casilla"] == nueva_posicion]
                    if len(mismas_pos) == 2 and all(p["Color"] == color for p in mismas_pos):
                        print("🚫 No puedes mover: hay un bloqueo de tu equipo en esa casilla.")
                        return

                    elif len(mismas_pos) == 1:
                        otra = mismas_pos[0]
                        es_seguro = any(c["Casilla"] == nueva_posicion and (c["Seguro"] or c["Salida"]) for c in tablero)
                        
                        # ⚔️ Si come, bonus +20

                        if otra["Color"] != color and not es_seguro:
                            print(f"⚔️ Has capturado a la ficha {otra['Color']} ID {otra['ID']}!")
                            otra["Casilla"] = 0
                            otra["Salio"] = False
                            aplicar_bonus(color, piezas, 20)

                    ficha_valida["Casilla"] = nueva_posicion

            print(f"➡️ La ficha {ficha_valida['ID']} se mueve a la casilla {ficha_valida['Casilla']}")
            return ficha_valida  # retorna la ficha movida para control de pares consecutivos
        else:
            print("❌ Esa ficha no es válida para mover.")


def jugar_ludo():
    orden = ["🟥 Rojo", "🟩 Verde", "🟦 Azul", "🟨Amarillo"]
    tablero = crear_tablero()
    piezas = crear_piezas()
    pares_consecutivos = 0
    ultima_ficha_movida = None

    while True:
        color = orden[0]
        print(f"\n🔁 Turno de {color}")
        dados_actuales = suma_dados()

        
        #   saca par
        
        if dados_actuales[0] == dados_actuales[1]:
            pares_consecutivos += 1
            print("🎲 Sacaste par, repites turno.")
        else:
            pares_consecutivos = 0

        ficha_movida = movimiento_pieza(piezas, dados_actuales, tablero, color, turno_jugador(color, piezas, tablero, dados_actuales))

        
        # 3 pares consecutivos
        
        if pares_consecutivos >= 3 and ficha_movida:
            ficha_movida["Casilla"] = 0
            ficha_movida["Salio"] = False
            print("🚨 Sacaste 3 pares seguidos. Última ficha movida enviada a la cárcel (base).")
            pares_consecutivos = 0

        
        #  Victoria 
        
        fichas_equipo = [p for p in piezas if p["Color"] == color]
        if all(p["Llego"] for p in fichas_equipo):
            print(f"🏆 {color} ha ganado el juego. Todas sus fichas llegaron a meta.")
            break

        if dados_actuales[0] != dados_actuales[1]:
            orden.append(orden.pop(0))  # pasa turno solo si no sacó par

jugar_ludo()