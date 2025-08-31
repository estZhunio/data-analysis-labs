# Laboratorio 3 (corregido y documentado)

Objetivo: dejar el repo listo para el profe (tests verdes) y a la vez mostrar que entendiste el problema original.

## Que contiene
- src/operaciones.py -> version **corregida** con tipado y ValueError; incluye un bloque comentado con la version "antes" y la explicacion de por que estaba mal.
- src/main.py -> maneja el error de division por cero con try/except para demo manual.
- src/__init__.py -> hace que src sea paquete; evita problemas de import.
- tests/test_operaciones.py -> pruebas que validan el comportamiento final.
- pyproject.toml -> config de ruff y mypy (py310 por defecto).
- requirements.txt -> ruff, mypy, pytest.
- .github/workflows/ci.yml -> CI con ruff, mypy y pytest.

## Ejecutar
```bash
# crear y activar venv
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# demo
python -m src.main

# tests
python -m pytest -q

# tipo y estilo
mypy --strict --explicit-package-bases src
ruff check .
ruff format --check .
```

## Documentacion de la correccion
Problema inicial (intencional): dividir devolvia None cuando b == 0. Esto es mala practica porque:
- rompe el contrato de tipos: a/b normalmente devuelve numero, no None
- oculta errores de dominio: dividir por cero es un error; debe reportarse

Solucion aplicada:
- dividir(a, b) ahora lanza ValueError si b == 0 y devuelve siempre float
- se anadieron anotaciones de tipo para claridad
- se ajusto main.py para mostrar el error esperado sin romper la demo

## Notas de compatibilidad
- Este repo usa py310 en pyproject.toml. Si corres 3.12, cambia a py312 en [tool.ruff] y [tool.mypy].
