"""
    Modulo de numeros para el paquete.
"""
from .cadenas import contar_vocales  # importacion relativa

def es_par(n: int) -> bool:
    return n % 2 == 0

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n debe ser >= 0")
    if n == 0:
        return 1
    return n * factorial(n-1)

def usar_contar_vocales_en_numero(n: int) -> int:
    # Convierte numero a string y cuenta las vocales
    return contar_vocales(str(n))
