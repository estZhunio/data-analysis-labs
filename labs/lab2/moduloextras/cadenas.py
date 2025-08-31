"""
    Modulo de cadenas para el paquete.
"""

def invertir(texto: str) -> str:
    return texto[::-1]

def contar_vocales(texto: str) -> int:
    return sum(1 for c in texto.lower() if c in "aeiou")
