# PyPOS CLI

Punto de venta y contabilidad por consola, desarrollado en Python 3.12 y ejecutado en Docker con persistencia SQLite.

## Ejecución

```bash
docker compose run --rm --build pos-app
```

La base de datos se guarda en `data/pos.db` del host mediante el volumen `./data:/app/data`.

## Estructura

- `app/database.py`: conexión y configuración de SQLite.
- `app/transacciones.py`: operaciones transaccionales ACID.
- `app/servicios/`: cálculos fiscales, inventario y arqueo de caja.
- `app/ui/menu.py`: menús de consola.
- `main.py`: punto de entrada.
