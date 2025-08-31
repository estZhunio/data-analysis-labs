# Laboratorio 3

## Contenido
- src/operaciones.py -> version corregida con tipos y ValueError. Al inicio hay un bloque comentado con la version anterior y una nota corta de por que estaba mal.
- src/main.py -> ejemplo simple que maneja la division por cero con try/except.
- src/__init__.py -> hace que src sea un paquete y evita problemas de import.
- tests/test_operaciones.py -> pruebas que validan el comportamiento final.
- pyproject.toml -> config minima de ruff y mypy (py310 por defecto).
- requirements.txt -> ruff, mypy, pytest.
- .github/workflows/ci.yml -> CI basico (ruff, mypy, pytest).

## Como ejecutar
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
