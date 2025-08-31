from __future__ import annotations
import csv
from pathlib import Path
from typing import Iterable, Set
REQUIRED_COLUMNS=['id','nombre','edad','ingreso']

def load_rows(path:str|Path)->list[dict[str,str]]:
    p=Path(path)
    with p.open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def check_required_columns(fieldnames:Iterable[str])->bool:
    fields:Set[str]=set(fieldnames or [])
    missing=set(REQUIRED_COLUMNS)-fields
    if missing: raise AssertionError(f'faltan columnas: {sorted(missing)}')
    return True

def validate_rows(rows):
    ids:Set[int]=set()
    for i,r in enumerate(rows, start=1):
        try:
            _id=int(r['id']); edad=int(r['edad']); ingreso=float(r['ingreso']); nombre=str(r['nombre'])
        except Exception as e:
            raise AssertionError(f'fila {i}: tipos invalidos -> {e}')
        if _id in ids: raise AssertionError(f'fila {i}: id repetido {_id}')
        ids.add(_id)
        if edad<0: raise AssertionError(f'fila {i}: edad negativa')
        if ingreso<0: raise AssertionError(f'fila {i}: ingreso negativo')
        if not nombre: raise AssertionError(f'fila {i}: nombre vacio')
    return True
