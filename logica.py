def suma_dados(mode):
    import random
    if mode == "d":
        d1 = int(input("Ingrese el valor del dado 1 (1-6): "))
        d2 = int(input("Ingrese el valor del dado 2 (1-6): "))
    else:
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
    print(f"[🎲 Lanzamiento de dados] => ({d1}, {d2})")
    return d1, d2
    
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

                for pieza in fichas_en_base:
                    if pieza["ID"] == escoger and pieza["Color"] == color:
                        print(f"Sacando la pieza {pieza['Color']} con ID {pieza['ID']} de la base.")
                        if pieza["Color"] == "🟥 Rojo":
                            pieza["Casilla"] = 12
                        elif pieza["Color"] == "🟩 Verde":
                            pieza["Casilla"] = 29
                        elif pieza["Color"] == "🟦 Azul":
                            pieza["Casilla"] = 46
                        elif pieza["Color"] == "🟨Amarillo":
                            pieza["Casilla"] = 63
                        pieza["Salio"] = True
                        return True
                print("❌ Esa ficha no está en la base o no es válida.")
        else:
            print("Sacaste un 5, pero no tienes fichas en la base.")
            return tiene_fichas_fuera  # si tiene fichas afuera, puede moverlas

    return tiene_fichas_fuera



def movimiento_pieza(piezas, dados, tablero,color,turno):
    if not turno:
        print("No se puede mover ninguna pieza porque no se ha sacado un 5.")
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
                if pieza["ID"] == escoger and pieza["Color"] == color and pieza["Salio"] == True:
                    ficha_valida = pieza
                    break

            if ficha_valida:
                nueva_posicion = ficha_valida["Casilla"] + pasos
                ficha_valida["Casilla"] = nueva_posicion
                print(f"La pieza {ficha_valida['Color']} con ID {ficha_valida['ID']} se mueve a la casilla {nueva_posicion}")
                print(f"Estado actual de la pieza: {ficha_valida}")
                break
            else:
                print("❌ No se puede mover esa ficha porque no es de tu color o no ha salido de la base. Intenta con otra.")
