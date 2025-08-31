import pytest
from mod_simple import normalize_text, word_count, dividir

def test_normalize_text():
    assert normalize_text('  Hola  ')=='hola'
    assert normalize_text('PYTHON ')=='python'

def test_word_count():
    assert word_count('')==0
    assert word_count('   ')==0
    assert word_count('uno dos tres')==3

def test_dividir_ok():
    assert dividir(10,2)==5.0
    assert dividir(7,2)==3.5

def test_dividir_cero():
    with pytest.raises(ValueError):
        dividir(1,0)
