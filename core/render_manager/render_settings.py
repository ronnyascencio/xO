import maya.cmds as cmds
import os

# Configuración de calidad del render
RENDER_SETTINGS = {
    "low": {  # Configuración para pruebas
        "resolution": (960, 540),
        "samples": 2,
        "passes": False  # Solo RGBA
    },
    "production": {  # Configuración para producción
        "resolution": (1920, 1080),
        "samples": 16,
        "passes": True  # Beauty y Utility
    }
}

# Luces para Beauty Passes
BEAUTY_LIGHTS = ["HDR", "SUN", "lgtA", "lgtB", "lgtC", "lgtD", "lgtE"]

# Utility Passes (AOVs)
UTILITY_PASSES = {
    "zdepth": "Ci[depth]",
    "normal": "Nn",
    "position": "P",
    "shaderID": "id"
}


# Generar paths basados en la estructura del proyecto
def get_render_path(mode="low"):
    """
    Genera la ruta de salida de render basada en $SHOW y la estructura del proyecto.
    """
    show = os.getenv("SHOW")
    if not show:
        cmds.warning("El entorno SHOW no está configurado.")
        return None

    project_root = os.getenv("VFX", "D:/")  # Ruta base del pipeline
    project_path = os.path.join(project_root, "Project", show)

    # Extraer nombre de la escena actual
    scene_path = cmds.file(query=True, sceneName=True)
    if not scene_path:
        cmds.warning("No hay una escena abierta.")
        return None

    scene_name = os.path.splitext(os.path.basename(scene_path))[0]

    # Ruta de render final
    render_path = os.path.join(project_path, "renderData", mode, scene_name)
    os.makedirs(render_path, exist_ok=True)  # Crear directorio si no existe
    return render_path


# Configurar LPEs para Beauty y Utility Passes
def setup_lpes(render_path):
    """
    Configura los Light Path Expressions (LPEs) para Beauty y Utility passes.
    """
    # Configurar Beauty Passes por luz
    for light in BEAUTY_LIGHTS:
        lpe_beauty = f"C<{light}>.*"
        cmds.rmanAddOutput(
            name=f"beauty_{light}",
            filePrefix=f"{render_path}/{light}_beauty",
            lpe=lpe_beauty
        )
        print(f"Configurado Beauty Pass para luz: {light}")

    # Configurar Utility Passes
    for name, lpe in UTILITY_PASSES.items():
        cmds.rmanAddOutput(
            name=f"utility_{name}",
            filePrefix=f"{render_path}/{name}",
            lpe=lpe
        )
        print(f"Configurado Utility Pass: {name}")


# Configurar paths y calidad
def set_render_config(mode="low"):
    """
    Configura los paths, la calidad de render y los pases.
    """
    # Obtener configuración
    settings = RENDER_SETTINGS.get(mode)
    if not settings:
        cmds.warning(f"Modo '{mode}' no soportado.")
        return

    # Configurar RenderMan como motor de render
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "renderman", type="string")

    # Ajustar calidad
    cmds.setAttr("defaultResolution.width", settings["resolution"][0])
    cmds.setAttr("defaultResolution.height", settings["resolution"][1])
    cmds.setAttr("RenderManRenderSettings.samplingMaxSamples", settings["samples"])

    # Configurar pases
    render_path = get_render_path(mode)
    if render_path:
        setup_lpes(render_path)
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix",
                     f"{render_path}/<RenderPass>", type="string")
        print(f"Path de render configurado: {render_path}")

    cmds.confirmDialog(title="Render Settings",
                       message=f"Configuración de render aplicada: {mode.upper()}",
                       button=["OK"])
    print(f"Render settings configurados en modo: {mode}")


# Crear el shelf
def create_render_shelf():
    shelf_name = "RenderSettings"

    # Verificar si el shelf ya existe
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    # Crear el shelf
    shelf = cmds.shelfLayout(shelf_name, parent="ShelfLayout")

    # Botón para "Set Low"
    cmds.shelfButton(
        parent=shelf,
        label="Set Low",
        image="commandButton.png",  # Cambia por un icono personalizado si es necesario
        command="import maya.cmds as cmds; set_render_config('low');",
        annotation="Configurar render para pruebas (Low)"
    )

    # Botón para "Set Production"
    cmds.shelfButton(
        parent=shelf,
        label="Set Production",
        image="commandButton.png",  # Cambia por un icono personalizado si es necesario
        command="import maya.cmds as cmds; set_render_config('production');",
        annotation="Configurar render para producción"
    )

    print(f"Shelf '{shelf_name}' creado con botones.")


# Ejecutar para crear el shelf
create_render_shelf()
