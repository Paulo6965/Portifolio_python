#notas
nota1 = float(input("Digite a nota 1: "))#variavel que recebe nota1
nota2 = float(input("Digite a nota 2: "))#variavel que revebe nota2
media = (nota1 + nota2)/2

print(f"Media: {media:.2}")
if media >=6:
    print("Voce foi aprovado")

else:

    print("Voce esta reprovado")