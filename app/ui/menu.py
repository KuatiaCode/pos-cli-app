
import os
from colorama import Fore, Style, init

from app.servicios.arqueo_caja import (
    obtener_caja_abierta,
    abrir_caja,
    registrar_movimiento,
    obtener_resumen_caja,
    cerrar_caja
)

init(autoreset=True)

# ==========================================
# COLORES DEL SISTEMA PyPOS
# ==========================================

AZUL = Fore.LIGHTCYAN_EX
NARANJA = Fore.LIGHTYELLOW_EX
VERDE = Fore.LIGHTGREEN_EX
ROJO = Fore.LIGHTRED_EX
BLANCO = Fore.WHITE
GRIS = Fore.LIGHTBLACK_EX

ANCHO = 54


# ==========================================
# FUNCIONES VISUALES
# ==========================================

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def linea(caracter="─"):
    print(GRIS + caracter * ANCHO)


def encabezado(titulo):
    limpiar_pantalla()

    print()
    print(AZUL + Style.BRIGHT + "╔" + "═" * (ANCHO - 2) + "╗")
    print(AZUL + Style.BRIGHT + "║" + " " * (ANCHO - 2) + "║")
    print(
        AZUL + Style.BRIGHT
        + "║" + " " * 22 + "PyPOS CLI" + " " * 23 + "║"
    )
    print(AZUL + Style.BRIGHT + "║" + " " * (ANCHO - 2) + "║")
    print(AZUL + Style.BRIGHT + "╚" + "═" * (ANCHO - 2) + "╝")

    print()
    print(AZUL + Style.BRIGHT + f"  {titulo}")
    linea()


def titulo_seccion(titulo):
    print()
    print(AZUL + Style.BRIGHT + f"  {titulo}")
    linea()


def mensaje_exito(mensaje):
    print(f"\n{VERDE}{Style.BRIGHT}  ✓ {mensaje}")


def mensaje_error(mensaje):
    print(f"\n{ROJO}{Style.BRIGHT}  ✗ {mensaje}")


def pausa():
    print()
    linea()
    input(f"{GRIS}  Presione ENTER para continuar...")


def formato_gs(valor):
    return f"{valor:,.0f}".replace(",", ".")


def mostrar_opcion(numero, descripcion):
    print(
        f"  {NARANJA}{Style.BRIGHT}{numero:>2}"
        f"{BLANCO}  {descripcion}"
    )


# ==========================================
# RESUMEN DE CAJA
# ==========================================

def mostrar_resumen(resumen):
    print()

    print(VERDE + Style.BRIGHT + "  ╔" + "═" * (ANCHO - 4) + "╗")
    print(
        VERDE + Style.BRIGHT
        + "  ║" + "       RESUMEN DE CAJA".center(ANCHO - 4) + "║"
    )
    print(VERDE + Style.BRIGHT + "  ╠" + "═" * (ANCHO - 4) + "╣")

    print(
        f"  ║  {AZUL}Número de caja: {BLANCO}"
        f"{str(resumen['id_caja']):<33}{VERDE}║"
    )

    print(VERDE + "  ╠" + "═" * (ANCHO - 4) + "╣")

    print(
        f"  ║  {BLANCO}Monto inicial:     "
        f"{VERDE}G. {formato_gs(resumen['monto_inicial']):>20}  ║"
    )

    print(
        f"  ║  {BLANCO}Total de ingresos: "
        f"{VERDE}G. {formato_gs(resumen['ingresos']):>20}  ║"
    )

    print(
        f"  ║  {BLANCO}Total de egresos:  "
        f"{ROJO}G. {formato_gs(resumen['egresos']):>20}  ║"
    )

    print(VERDE + Style.BRIGHT + "  ╠" + "═" * (ANCHO - 4) + "╣")

    print(
        f"  ║  {VERDE}{Style.BRIGHT}EFECTIVO ESPERADO: "
        f"G. {formato_gs(resumen['efectivo_esperado']):>18}  ║"
    )

    print(VERDE + Style.BRIGHT + "  ╚" + "═" * (ANCHO - 4) + "╝")


# ==========================================
# MENÚ DE ARQUEO DE CAJA
# ==========================================

def menu_arqueo():

    while True:
        encabezado("ARQUEO DE CAJA")

        print()
        mostrar_opcion("01", "Abrir caja")
        mostrar_opcion("02", "Registrar ingreso")
        mostrar_opcion("03", "Registrar egreso")
        mostrar_opcion("04", "Consultar resumen")
        mostrar_opcion("05", "Cerrar caja")

        print()
        linea()

        print(f"  {ROJO}00{BLANCO}  Volver al menú principal")

        linea()

        opcion = input(
            f"\n  {NARANJA}Seleccione una opción: {BLANCO}"
        ).strip()

        if opcion == "0":
            return

        try:

            # ABRIR CAJA
            if opcion == "1":

                encabezado("APERTURA DE CAJA")

                titulo_seccion("DATOS DE APERTURA")

                monto = input(
                    f"\n  {BLANCO}Monto inicial: {VERDE}G. "
                ).strip().replace(",", ".")

                id_caja = abrir_caja(monto)

                mensaje_exito(
                    f"Caja N.º {id_caja} abierta correctamente."
                )

            # REGISTRAR INGRESO
            elif opcion == "2":

                encabezado("REGISTRAR INGRESO")

                titulo_seccion("DATOS DEL INGRESO")

                concepto = input(
                    f"\n  {BLANCO}Concepto: "
                ).strip()

                monto = input(
                    f"  {BLANCO}Monto: {VERDE}G. "
                ).strip().replace(",", ".")

                registrar_movimiento("Ingreso", concepto, monto)

                mensaje_exito("Ingreso registrado correctamente.")

            # REGISTRAR EGRESO
            elif opcion == "3":

                encabezado("REGISTRAR EGRESO")

                titulo_seccion("DATOS DEL EGRESO")

                concepto = input(
                    f"\n  {BLANCO}Concepto: "
                ).strip()

                monto = input(
                    f"  {BLANCO}Monto: {ROJO}G. "
                ).strip().replace(",", ".")

                registrar_movimiento("Egreso", concepto, monto)

                mensaje_exito("Egreso registrado correctamente.")

            # CONSULTAR RESUMEN
            elif opcion == "4":

                encabezado("RESUMEN DE CAJA")

                resumen = obtener_resumen_caja()

                mostrar_resumen(resumen)

            # CERRAR CAJA
            elif opcion == "5":

                encabezado("CIERRE DE CAJA")

                titulo_seccion("CIERRE Y VERIFICACIÓN")

                contado = input(
                    f"\n  {BLANCO}Efectivo contado: {VERDE}G. "
                ).strip().replace(",", ".")

                resultado = cerrar_caja(contado)

                print()
                linea()

                print(
                    f"\n  {BLANCO}Efectivo esperado: "
                    f"{VERDE}G. "
                    f"{formato_gs(resultado['efectivo_esperado'])}"
                )

                print(
                    f"  {BLANCO}Efectivo contado:  "
                    f"{AZUL}G. "
                    f"{formato_gs(resultado['efectivo_contado'])}"
                )

                print()
                linea()

                diferencia = resultado["diferencia"]

                if diferencia > 0:
                    color = VERDE
                elif diferencia < 0:
                    color = ROJO
                else:
                    color = VERDE

                print(
                    f"\n  {color}{Style.BRIGHT}"
                    f"{resultado['resultado'].upper()}: "
                    f"G. {formato_gs(abs(diferencia))}"
                )

                mensaje_exito("Caja cerrada correctamente.")

            else:

                mensaje_error("Opción no válida.")

        except ValueError as error:

            mensaje_error(str(error))

        except Exception as error:

            mensaje_error(f"Ocurrió un error: {error}")

        pausa()


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def ejecutar_menu():

    while True:

        encabezado("MENÚ PRINCIPAL")

        print()

        print(
            f"  {NARANJA}{Style.BRIGHT}01"
            f"{BLANCO}  ARQUEO DE CAJA"
        )

        print(
            f"      {GRIS}Apertura, movimientos y cierre"
        )

        print()

        print(
            f"  {ROJO}{Style.BRIGHT}00"
            f"{BLANCO}  SALIR DEL SISTEMA"
        )

        print()
        linea()

        opcion = input(
            f"\n  {NARANJA}Seleccione una opción: {BLANCO}"
        ).strip()

        if opcion == "1":

            menu_arqueo()

        elif opcion == "0":

            encabezado("FINALIZANDO SISTEMA")

            print()
            print(
                f"  {VERDE}{Style.BRIGHT}"
                "Gracias por utilizar PyPOS."
            )

            print(f"  {GRIS}Hasta pronto.")

            return

        else:

            mensaje_error("Opción no válida.")
            pausa()
