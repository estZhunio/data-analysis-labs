"""
    Modulo B: manejo de excepciones.
"""
from typing import List, Tuple

# B.1 - Validacion y parseo
def parsear_enteros(entradas: list[str]) -> Tuple[list[int], list[str]]:
    valores: List[int] = []
    errores: List[str] = []
    for idx, s in enumerate(entradas):
        try:
            valores.append(int(s))
        except ValueError:
            errores.append(f"pos {idx}: '{s}' no es entero")
    return valores, errores

# B.2 - Excepciones personalizdas y raise
class CantidadInvalida(Exception):
    pass

def calcular_total(precio_unitario: float, cantidad: int) -> float:
    if cantidad <= 0:
        raise CantidadInvalida("La cantidad debe ser mayor que 0")
    if precio_unitario < 0:
        raise ValueError("El precio unitario no puede ser negativo")
    return precio_unitario * cantidad
