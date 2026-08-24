numero = float(input("Digite o número: "))
indice = int(input("Digite o índice da raiz: "))

if indice <= 0:
    print("O índice deve ser maior que zero.")
elif numero < 0 and indice % 2 == 0:
    print("Não existe raiz real de índice par para números negativos.")
else:
    if numero < 0:
        resultado = -((-numero) ** (1 / indice))
    else:
        resultado = numero ** (1 / indice)

    print(f"A raiz de índice {indice} de {numero} é {resultado}")