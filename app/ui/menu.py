def ejecutar_menu() -> None:
    print("PyPOS CLI")
    print("Estructura inicial del proyecto.")
    print("0. Salir")

    while True:
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            print("Hasta luego.")
            return
        print("Opción no válida.")
