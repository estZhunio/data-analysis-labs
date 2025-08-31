import pytest
from src.operaciones import sumar, dividir

def test_sumar():
    assert sumar(2, 5) == 7
    assert sumar(-1, 1) == 0

def test_dividir_ok():
    assert dividir(9, 3) == 3

def test_dividir_cero():
    with pytest.raises(ValueError):
        dividir(1, 0)
