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

def crear_piezas():
    piezas = []
    colores=["🟥 Rojo", "🟩 Verde", "🟦 Azul", "🟨Amarillo"]
    for color in colores:
        for i in range(1, 5):
            pieza = {"ID":i,"Color": color, "Casilla":0,"Salio":False}
            piezas.append(pieza)
    return piezas