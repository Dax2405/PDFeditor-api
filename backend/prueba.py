cadena = "aaaaaaaaalaaal"
letras = []
letras_lar = []
contador = 0
resta = 1
mayor = 0
for i in cadena:
    for j in cadena[resta:]:
        if i == j:
            break
        if j != " ":
            letras.append(j)
            contador += 1

    if contador > mayor:
        mayor = contador
        letras_lar = letras
    letras = []
    contador = 1
    resta += 1

letras
print(mayor, " ", ''.join(letras_lar))
