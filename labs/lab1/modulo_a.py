"""
    Modulo A: funciones como valores y closures.
"""

from typing import Any, Callable, Dict

# A.1-Funciones como valores
def saludar(nombre: str) -> str:
    return f"Hola {nombre}"

def despedir(nombre: str) -> str:
    return f"Bye {nombre}"

def aplaudir(nombre: str) -> str:
    return f"Aplausos para {nombre}"

acciones: Dict[str, Callable[..., Any]] = {
    "saludar": saludar,
    "despedir": despedir,
    "aplaudir": aplaudir,
}

class AccionDesconocida(KeyError):
    pass

def ejecutar(accion: str, *args, **kwargs) -> Any:
    try:
        fn = acciones[accion]
    except KeyError as exc:
        raise AccionDesconocida(f"accion desconocida: {accion}") from exc
    return fn(*args, **kwargs)

# A.2 - Funciones internas y closures
def crear_descuento(porcentaje: float) -> Callable[[float], float]:
    """
        Devuelve una funcion que aplica un descuento fijo.
            Porcentaje: fraccion entre 0 y 1, por ejemplo 0.10 para 10%%.
    """
    def aplicar(precio: float) -> float:
        return precio * (1 - porcentaje)
    return aplicar
