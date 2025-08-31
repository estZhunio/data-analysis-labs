from src.operaciones import sumar, dividir

def run() -> None:
    print("sumar 2 + 3 =", sumar(2, 3))
    print("dividir 10 / 2 =", dividir(10, 2))
    try:
        print("dividir 1 / 0 =", dividir(1, 0))
    except ValueError as e:
        print("OK error esperado:", e)

if __name__ == "__main__":
    run()
