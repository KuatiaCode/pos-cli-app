
from app.database import obtener_conexion
from app.servicios.arqueo_caja import inicializar_tablas
from app.ui.menu import ejecutar_menu


if __name__ == "__main__":
    inicializar_tablas()
    ejecutar_menu()
