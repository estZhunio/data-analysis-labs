"""
Estado final (corregido).

Antes (version erronea, comentada solo para documentar):

    def dividir(a: float, b):
        if b == 0:
            return None
        return a / b

Por que esta mal:
- devuelve None cuando se espera un numero -> rompe el contrato de tipos
- oculta un error de dominio (division por cero) -> deberia lanzar excepcion
"""

from typing import Union

Number = Union[int, float]

def sumar(a: Number, b: Number) -> Number:
    """Suma dos numeros y devuelve Number (int o float segun entrada)."""
    return a + b

def dividir(a: Number, b: Number) -> float:
    """Divide a entre b. Lanza ValueError si b == 0 y devuelve siempre float."""
    if b == 0:
        raise ValueError("division por cero")
    return float(a) / float(b)
