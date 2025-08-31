# Laboratorio 2: modulos, paquetes y anotaciones de tipado

Este laboratorio demuestra:
- Creacion de modulos con funciones coherentes.
- Organizacion en paquetes con importaciones absolutas y relativas.
- Uso opcional de anotaciones de tipado.

## Estructura
```
lab2/
├─ modulo_utilidades.py
├─ usar_utilidades.py
├─ paquete/
│  ├─ __init__.py
│  ├─ cadenas.py
│  └─ numeros.py
├─ usar_paquete.py
└─ README.md
```

## Ejecucion
- Probar modulo individual:
  ```bash
  python usar_utilidades.py
  ```
- Probar paquete:
  ```bash
  python usar_paquete.py
  ```

## Notas
- modulo_utilidades.py -> ofrece API de cadenas basicas.
- moduloextras/ -> contiene dos modulos: cadenas y numeros. __init__.py reexporta funciones clave.
- Se muestran importaciones absolutas y relativas.
- Anotaciones de tipado ilustradas en algunas funciones.
