import hou

def create_shot_template():
    """Crea un template para shots en Solaris con 3Delight."""
    try:
        # Verificar o crear el nodo /stage
        stage = hou.node("/stage") or hou.node("/").createNode("stage")

        # Importar múltiples USD Layers (assets del shot)
        asset_import = stage.createNode("usdmultifile", "Shot_Assets")
        asset_import.parm("pattern").set("$HOUDINI_PROJECT/scenes/<scene_name>/<shot_name>/*.usd")

        # Crear un dome light para iluminación global
        dome_light = stage.createNode("3delightdome", "Dome_Light")
        dome_light.parm("env_map").set("$HOUDINI_PROJECT/sourceimages/<hdri_name>.exr")

        # Crear una cámara para el shot
        camera = stage.createNode("camera", "Shot_Camera")
        camera.parm("resx").set(1920)
        camera.parm("resy").set(1080)

        # Crear un nodo de configuración de render de 3Delight
        render_settings = stage.createNode("3delightrendersettings", "Render_Settings")

        # Crear un nodo de salida de render de 3Delight
        render_output = stage.createNode("3delightoutput", "Render_Output")
        render_output.parm("rendersettings").set(render_settings.path())

        # Organizar nodos
        stage.layoutChildren()
        hou.ui.displayMessage("Shot Template creado correctamente.")
    except Exception as e:
        hou.ui.displayMessage(f"Error al crear el template de Shot: {e}")
