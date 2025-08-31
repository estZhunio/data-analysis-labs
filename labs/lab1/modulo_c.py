"""
    Modulo C: decoradores de validacion.
"""
from functools import wraps
from typing import Any, Callable

def _es_numero(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)

def requiere_positivos(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Revisa todos los argumentos numericos posicionales y con nombre
        for x in args:
            if _es_numero(x) and x <= 0:
                raise ValueError(f"argumento debe ser > 0: {x}")
        for k, v in kwargs.items():
            if _es_numero(v) and v <= 0:
                raise ValueError(f"{k} debe ser > 0: {v}")
        return fn(*args, **kwargs)
    return wrapper

@requiere_positivos
def calcular_descuento(precio: float, porcentaje: float) -> float:
    # porcentaje expresado como fraccion (0.2 para 20%)
    return precio * (1 - porcentaje)

@requiere_positivos
def escala(valor: float, factor: float) -> float:
    return valor * factor
