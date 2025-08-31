from modulo_a import ejecutar, crear_descuento, AccionDesconocida
from modulo_b import parsear_enteros, calcular_total, CantidadInvalida
from modulo_c import calcular_descuento as calc_desc, escala

def demo_modulo_a():
    print("-- Modulo A --")
    print(ejecutar("saludar", "Miguel"))
    print(ejecutar("aplaudir", "Miguel"))
    try:
        ejecutar("no-existe", "Miguel")
    except AccionDesconocida as e:
        print(f"OK excepcion esperada: {e}")
    d10 = crear_descuento(0.10)
    d25 = crear_descuento(0.25)
    print("descuento 10% de 100:", d10(100))
    print("descuento 25% de 80:", d25(80))

def demo_modulo_b():
    print("\n-- Modulo B --")
    valores, errores = parsear_enteros(["10", "x", "3"])
    print("valores:", valores)
    print("errores:", errores)
    print("total 10 * 3:", calcular_total(10, 3))
    try:
        calcular_total(10, 0)
    except CantidadInvalida as e:
        print(f"OK excepcion esperada: {e}")

def demo_modulo_c():
    print("\n-- Modulo C --")
    print("calcular_descuento(100, 0.2):", calc_desc(100, 0.2))
    print("escala(5, 3):", escala(5, 3))
    try:
        calc_desc(-1, 0.2)
    except ValueError as e:
        print(f"OK excepcion esperada: {e}")

if __name__ == "__main__":
    demo_modulo_a()
    demo_modulo_b()
    demo_modulo_c()
