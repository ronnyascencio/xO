import sys
import os
import maya.cmds as cmds

# Determinar la ruta base de `open_saver_loader.py`
current_dir = os.path.dirname(__file__)

# Construir la ruta de `saver_loader.py` a partir de la ubicación actual
saver_loader_path = os.path.join(current_dir, "..", "..", "core", "saver_loader", "saver_loader.py")
saver_loader_dir = os.path.dirname(saver_loader_path)

def show_saver_loader():
    # Agregar el directorio de saver_loader al sys.path si no está incluido
    if saver_loader_dir not in sys.path:
        sys.path.append(saver_loader_dir)

    # Importa la clase de la interfaz desde saver_loader
    try:
        from saver_loader import MainApp
    except ImportError as e:
        cmds.warning(f"Error al importar saver_loader.py: {e}")
        return

    # Inicializar y mostrar la interfaz
    global main_window
    try:
        main_window.close()  # Cierra cualquier instancia anterior
    except:
        pass

    main_window = MainApp()
    main_window.show()

# Crear un menú personalizado en Maya para abrir la interfaz
def create_xo_menu():
    if not cmds.menu("xO_Menu", exists=True):
        cmds.menu("xO_Menu", label="xO", parent="MayaWindow")

    # Usar un comando de importación en cadena para asegurarnos de que funcione en el contexto de Maya
    cmds.menuItem(label="Saver Loader",
                  command="import sys; import os; "
                          f"sys.path.append(r'{saver_loader_dir}'); "
                          "from open_saver_loader import show_saver_loader; "
                          "show_saver_loader()",
                  parent="xO_Menu")

# Ejecuta el menú al iniciar Maya
create_xo_menu()

# Confirmación de que el script cargó correctamente
cmds.warning("Script open_saver_loader.py cargado y menú 'xO' creado.")
