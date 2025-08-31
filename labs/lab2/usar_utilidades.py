from modulo_utilidades import normalizar, es_palindromo, cortar, buscar

def main():
    print("--- Pruebas modulo_utilidades ---")
    print(normalizar(" Hola Mundo "))
    print("es_palindromo 'radar':", es_palindromo("radar"))
    print("es_palindromo 'python':", es_palindromo("python"))
    try:
        print(cortar("hola", 0))
    except ValueError as e:
        print("OK error esperado:", e)
    print("buscar 'mun' en 'comunidad':", buscar("comunidad", "mun"))

if __name__ == "__main__":
    main()
