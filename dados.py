import random

def lanzar_dados_real():
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    return dado1, dado2

def lanzar_dados_desarrollador():
    while True:
        try:
            dado1 = int(input("Ingresa el valor del dado 1 (1-6): "))
            dado2 = int(input("Ingresa el valor del dado 2 (1-6): "))
            if 1 <= dado1 <= 6 and 1 <= dado2 <= 6:
                return dado1, dado2
            else:
                print("Los valores deben estar entre 1 y 6.")
        except ValueError:
            print("Por favor, ingresa números enteros.")

def main():
    modo = input("¿Modo de juego? ('real' o 'desarrollador'): ").lower()

    if modo == 'real':
        dado1, dado2 = lanzar_dados_real()
    elif modo == 'desarrollador':
        dado1, dado2 = lanzar_dados_desarrollador()
    else:
        print("Modo no válido. Usa 'real' o 'desarrollador'.")
        return

    print("Resultado: dado1 = ",dado1, "dado2 =", dado2)
    print("Suma total: ",dado1 + dado2)
    
    if dado1 == dado2:
        print("Sacaste un par. Tienes derecho a repetir turno.")

if __name__ == "__main__":
    main()
