"""
    Modulo de utilidades de cadenas.
"""
from typing import Optional

def normalizar(texto: str) -> str:
    return texto.strip().lower()

def es_palindromo(texto: str) -> bool:
    limpio = normalizar(texto).replace(" ", "")
    return limpio == limpio[::-1]

def cortar(texto: str, n: int) -> str:
    if n <= 0:
        raise ValueError("n debe ser positivo")
    return texto[:n]

def buscar(texto: str, sub: str) -> Optional[int]:
    idx = texto.find(sub)
    return idx if idx != -1 else None
