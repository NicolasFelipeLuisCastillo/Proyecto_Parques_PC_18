mode = input("Modo de juego d/j: ")

def crear_tablero():
    seguros=[5,17,22,34,39,51,56,68]
    salidas=[12,29,46,63]
    colores=["🟥 Rojo", "🟩 Verde", "🟦 Azul", "🟨Amarillo"]
    tablero=[]
    for i in range (1,69):
        if i>=1 and i <=16:
            color = colores[0]
        elif i>=17 and i <=33:
            color = colores[1]
        elif i>=34 and i <=50:
            color = colores[2] 
        elif i>=51 and i <=68:
            color = colores[3]
        casillas={"Casilla":i,"Color":color,"Seguro": True if i in seguros else False,"Salida":True if i in salidas else False}
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
    colores=["🟥 Rojo", "🟩 Verde", "🟦 Azul", "🟨Amarillo"]
    for color in colores:
        for i in range(1, 5):
            pieza = {"ID":i,"Color": color, "Casilla":0,"Salio":False, "Llego": False}
            piezas.append(pieza)
    return piezas

def suma_dados():
    import random
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

                ficha_escogida = None
                for p in fichas_en_base:
                    if p["ID"] == escoger:
                        ficha_escogida = p
                        break

                if ficha_escogida:
                    salida = obtener_salida(color)
                    fichas_en_salida = [p for p in piezas if p["Casilla"] == salida and p["Color"] == color]

                    if len(fichas_en_salida) >= 2:
                        print("🚫 No puedes sacar ficha: la salida está ocupada por 2 fichas de tu equipo.")
                        return any(p["Color"] == color and p["Salio"] for p in piezas)

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

        ficha_valida = None

        for pieza in piezas:
            if pieza["ID"] == escoger and pieza["Color"] == color and pieza["Salio"] == True and not pieza["Llego"]:
                ficha_valida = pieza
                break

        if ficha_valida:
            origen = ficha_valida["Casilla"]

            # Determinar si está en la zona final
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
                    aplicar_bonus(color, piezas, 10)
            else:
                nueva_posicion = origen + pasos

                # Verifica si entra a zona de llegada
                entrada = entrada_llegada[color]
                if origen <= entrada < nueva_posicion:
                    pasos_en_zona = nueva_posicion - entrada
                    if pasos_en_zona > 8:
                        print("❌ Movimiento no permitido. Debes sacar la cantidad exacta para entrar a la llegada.")
                        return
                    ficha_valida["Casilla"] = zona_llegada[color][pasos_en_zona - 1]
                else:
                    if nueva_posicion > 68:
                        nueva_posicion = nueva_posicion % 68

                    if hay_bloqueo_en_rango(piezas, color, origen, nueva_posicion):
                        print("🚧 No puedes pasar: hay un bloqueo en el camino entre tu posición y el destino.")
                        return

                    mismas_pos = [p for p in piezas if p["Casilla"] == nueva_posicion]

                    if len(mismas_pos) == 2 and all(p["Color"] == color for p in mismas_pos):
                        print("🚫 No puedes mover: hay un bloqueo de tu equipo en esa casilla.")
                        return

                    elif len(mismas_pos) == 1:
                        otra = mismas_pos[0]
                        es_seguro = any(c["Casilla"] == nueva_posicion and (c["Seguro"] or c["Salida"]) for c in tablero)

                        if otra["Color"] != color and not es_seguro:
                            print(f"⚔️ Has capturado a la ficha {otra['Color']} ID {otra['ID']}!")
                            otra["Casilla"] = 0
                            otra["Salio"] = False
                            aplicar_bonus(color, piezas, 20)

                    ficha_valida["Casilla"] = nueva_posicion

            print(f"La pieza {ficha_valida['Color']} con ID {ficha_valida['ID']} se mueve a la casilla {ficha_valida['Casilla']}")
            print(f"Estado actual de la pieza: {ficha_valida}")
            break
        else:
            print("❌ No se puede mover esa ficha porque no es de tu color, no ha salido o ya llegó. Intenta con otra.")

            print("❌ No se puede mover esa ficha porque no es de tu color, no ha salido o ya llegó. Intenta con otra.")

def jugar_ludo():
    orden = ["🟥 Rojo", "🟩 Verde", "🟦 Azul", "🟨Amarillo"]
    tablero = crear_tablero()
    piezas = crear_piezas()
    x="s"
    while x=="s":
        color = orden[0]
        print(f"Turno del jugador {color}")
        dados_actuales = suma_dados()
        movimiento_pieza(piezas, dados_actuales, tablero=tablero, color=color, turno=turno_jugador(color, piezas, tablero, dados_actuales))
        x=input("Continuar s/n: ")
        color = orden[0]
        orden.append(orden.pop(0))
        if x =="n":
            break

    return color

jugar_ludo()
