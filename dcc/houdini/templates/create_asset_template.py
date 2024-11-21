import hou

def create_asset_template():
    """Crea un template para assets en Solaris con 3Delight."""
    try:
        # Verificar o crear el nodo /stage
        stage = hou.node("/stage") or hou.node("/").createNode("stage")

        # Nodo USD para importar el asset
        usd_import = stage.createNode("usdimport", "Asset_Import")
        usd_import.parm("filepath").set("$HOUDINI_PROJECT/assets/<asset_name>/<asset_name>.usd")

        # Crear un nodo de configuración de render de 3Delight
        render_settings = stage.createNode("3delightrendersettings", "Render_Settings")

        # Crear un nodo de salida de render de 3Delight
        render_output = stage.createNode("3delightoutput", "Render_Output")
        render_output.parm("rendersettings").set(render_settings.path())

        # Organizar nodos
        stage.layoutChildren()
        hou.ui.displayMessage("Asset Template creado correctamente.")
    except Exception as e:
        hou.ui.displayMessage(f"Error al crear el template de Asset: {e}")
