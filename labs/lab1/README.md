# Laboratorio: funciones, metodos, excepciones y decoradores

Paquete listo para ejecutar y revisar. Contiene soluciones simples, limpias y con mensajes claros.

## Objetivos
- Practicar funciones, closures y uso de diccionarios con funciones como valores.
- Manejar excepciones, incluidas excepciones personalizadas.
- Aplicar decoradores para validar argumentos.

## Estructura
```
lab1/
│__ __init__.py
│__ modulo_a.py
│__ modulo_b.py
│__ modulo_c.py
│__ main.py
|__ README.md
```

## Requisitos
- Python 3.12
- Sistema operativo: Windows, macOS o Linux

## Instalacion rapida (opcional con venv)
```bash
# Windows (PowerShell)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version

# macOS / Linux
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

## Ejecutar
Desde la carpeta raiz del proyecto:
```bash
# Windows
python -m src.main

# macOS / Linux
python -m src.main
```

## Pruebas rapidas
Ejemplos cubren los criterios del enunciado:
- ejecutar("saludar", "Miguel") -> "Hola, Miguel"
- crear_descuento(0.10)(100) -> 90.0
- parsear_enteros(["10", "x", "3"]) -> valores [10, 3] y un error por "x"
- calcular_total(10, 3) -> 30
- calcular_descuento(100, 0.2) -> 80

## Notas
- Los modulos contienen docstrings y comentarios breves.
- No se requieren paquetes extra.
