from typing import Union
Number = Union[int,float]

def normalize_text(s:str)->str:
    return s.strip().lower()

def word_count(s:str)->int:
    s=s.strip(); return 0 if not s else len(s.split())

def dividir(a:Number,b:Number)->float:
    if b==0: raise ValueError('division por cero')
    return float(a)/float(b)
