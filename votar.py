idade = int(input("Digite sua idade: "))
nome = str(input("Digite seu nome: "))

if idade >= 16:
    print(f"{nome}, pode votar")
else:
    print(f"{nome}, não pode votar")