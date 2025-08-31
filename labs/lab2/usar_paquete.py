import moduloextras

def main():
    print("-- Pruebas paquete --")
    print("invertir('hola'):", moduloextras.invertir("Hola"))
    print("contar_vocales('miguel'):", moduloextras.contar_vocales("miguel"))
    print("es_par(10):", moduloextras.es_par(10))
    print("factorial(5):", moduloextras.factorial(5))
    # probar importacion relativa
    from moduloextras.numeros import usar_contar_vocales_en_numero
    print("usar_contar_vocales_en_numero(2025):", usar_contar_vocales_en_numero(2025))

if __name__ == "__main__":
    main()
