
from datetime import datetime
from decimal import Decimal, InvalidOperation

from app.database import obtener_conexion


def inicializar_tablas():
    """Crea las tablas propias del módulo de arqueo."""

    conexion = obtener_conexion()

    try:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS arqueo_cajas (
                id_caja INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_apertura TEXT NOT NULL,
                fecha_cierre TEXT,
                monto_inicial REAL NOT NULL,
                efectivo_esperado REAL,
                efectivo_contado REAL,
                diferencia REAL,
                estado TEXT NOT NULL DEFAULT 'Abierta'
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS arqueo_movimientos (
                id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
                id_caja INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('Ingreso', 'Egreso')),
                concepto TEXT NOT NULL,
                monto REAL NOT NULL CHECK(monto > 0),
                fecha TEXT NOT NULL,
                FOREIGN KEY (id_caja)
                    REFERENCES arqueo_cajas(id_caja)
            )
        """)

        conexion.commit()

    finally:
        conexion.close()


def obtener_caja_abierta():
    """Devuelve la caja que se encuentra abierta."""

    conexion = obtener_conexion()
    conexion.row_factory = __import__("sqlite3").Row

    try:
        caja = conexion.execute("""
            SELECT *
            FROM arqueo_cajas
            WHERE estado = 'Abierta'
            ORDER BY id_caja DESC
            LIMIT 1
        """).fetchone()

        return dict(caja) if caja else None

    finally:
        conexion.close()


def abrir_caja(monto_inicial):
    """Registra una nueva apertura de caja."""

    try:
        monto = Decimal(str(monto_inicial))
    except (InvalidOperation, ValueError):
        raise ValueError("El monto inicial no es válido.")

    if not monto.is_finite() or monto < 0:
        raise ValueError("El monto inicial no puede ser negativo.")

    if obtener_caja_abierta():
        raise ValueError("Ya existe una caja abierta.")

    conexion = obtener_conexion()

    try:
        cursor = conexion.execute("""
            INSERT INTO arqueo_cajas (
                fecha_apertura,
                monto_inicial,
                estado
            )
            VALUES (?, ?, 'Abierta')
        """, (
            datetime.now().isoformat(timespec="seconds"),
            float(monto)
        ))

        conexion.commit()
        return cursor.lastrowid

    finally:
        conexion.close()


def registrar_movimiento(tipo, concepto, monto):
    """Registra un ingreso o egreso de caja."""

    tipo = tipo.strip().capitalize()
    concepto = concepto.strip()

    if tipo not in ("Ingreso", "Egreso"):
        raise ValueError("El tipo debe ser Ingreso o Egreso.")

    if not concepto:
        raise ValueError("Debe ingresar un concepto.")

    try:
        valor = Decimal(str(monto))
    except (InvalidOperation, ValueError):
        raise ValueError("El monto no es válido.")

    if not valor.is_finite() or valor <= 0:
        raise ValueError("El monto debe ser mayor a cero.")

    caja = obtener_caja_abierta()

    if not caja:
        raise ValueError("No hay una caja abierta.")

    conexion = obtener_conexion()

    try:
        conexion.execute("""
            INSERT INTO arqueo_movimientos (
                id_caja,
                tipo,
                concepto,
                monto,
                fecha
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            caja["id_caja"],
            tipo,
            concepto,
            float(valor),
            datetime.now().isoformat(timespec="seconds")
        ))

        conexion.commit()

    finally:
        conexion.close()


def obtener_resumen_caja():
    """Calcula los ingresos, egresos y efectivo esperado."""

    caja = obtener_caja_abierta()

    if not caja:
        raise ValueError("No hay una caja abierta.")

    conexion = obtener_conexion()

    try:
        movimientos = conexion.execute("""
            SELECT
                tipo,
                COALESCE(SUM(monto), 0) AS total
            FROM arqueo_movimientos
            WHERE id_caja = ?
            GROUP BY tipo
        """, (caja["id_caja"],)).fetchall()

        ingresos = Decimal("0")
        egresos = Decimal("0")

        for movimiento in movimientos:
            if movimiento[0] == "Ingreso":
                ingresos = Decimal(str(movimiento[1]))
            elif movimiento[0] == "Egreso":
                egresos = Decimal(str(movimiento[1]))

        inicial = Decimal(str(caja["monto_inicial"]))
        esperado = inicial + ingresos - egresos

        return {
            "id_caja": caja["id_caja"],
            "monto_inicial": float(inicial),
            "ingresos": float(ingresos),
            "egresos": float(egresos),
            "efectivo_esperado": float(esperado)
        }

    finally:
        conexion.close()


def cerrar_caja(efectivo_contado):
    """Cierra la caja y calcula el sobrante o faltante."""

    try:
        contado = Decimal(str(efectivo_contado))
    except (InvalidOperation, ValueError):
        raise ValueError("El efectivo contado no es válido.")

    if not contado.is_finite() or contado < 0:
        raise ValueError("El efectivo contado no puede ser negativo.")

    resumen = obtener_resumen_caja()

    esperado = Decimal(str(resumen["efectivo_esperado"]))
    diferencia = contado - esperado

    conexion = obtener_conexion()

    try:
        conexion.execute("""
            UPDATE arqueo_cajas
            SET fecha_cierre = ?,
                efectivo_esperado = ?,
                efectivo_contado = ?,
                diferencia = ?,
                estado = 'Cerrada'
            WHERE id_caja = ?
              AND estado = 'Abierta'
        """, (
            datetime.now().isoformat(timespec="seconds"),
            float(esperado),
            float(contado),
            float(diferencia),
            resumen["id_caja"]
        ))

        conexion.commit()

        if diferencia > 0:
            resultado = "Sobrante"
        elif diferencia < 0:
            resultado = "Faltante"
        else:
            resultado = "Sin diferencia"

        return {
            **resumen,
            "efectivo_contado": float(contado),
            "diferencia": float(diferencia),
            "resultado": resultado
        }

    finally:
        conexion.close()
