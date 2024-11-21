import os
import maya.cmds as cmds


def get_scene_file_path():
    # Obtener el path completo del archivo de la escena
    scene_path = cmds.file(q=True, sn=True)

    if not scene_path:
        raise RuntimeError("La escena no está guardada. Por favor guarda la escena antes de ejecutar el script.")

    print(f"Path completo de la escena: {scene_path}")

    # Normalizar el path para garantizar compatibilidad multiplataforma
    scene_path = os.path.normpath(scene_path)

    # Dividir el path en partes
    path_parts = scene_path.split(os.sep)
    print(f"Niveles del path: {path_parts}")

    # Extraer los nombres de secuencia (sequence) y shot
    sequence_name = path_parts[4]
    shot_name = path_parts[5]
    print(f"Nombre de la secuencia: {sequence_name}")
    print(f"Nombre del shot: {shot_name}")

    return sequence_name, shot_name


# Ejecutar la función
sequence_name, shot_name = get_scene_file_path()



def get_current_image_output_dir():
    # Nodo RenderManGlobals
    renderman_globals = "rmanGlobals"
    if not cmds.objExists(renderman_globals):
        raise RuntimeError(f"No se encontró el nodo {renderman_globals}. ¿Está RenderMan instalado correctamente?")

    # Verificar si el atributo 'imageOutputDir' existe
    if cmds.attributeQuery("imageOutputDir", node=renderman_globals, exists=True):
        # Obtener el valor actual
        current_output_dir = cmds.getAttr(f"{renderman_globals}.imageOutputDir")
        print(f"Valor actual de imageOutputDir: {current_output_dir}")
        return current_output_dir
    else:
        raise RuntimeError("El atributo 'imageOutputDir' no existe en RenderManGlobals.")

    scene_path = cmds.file(q=True, sn=True)

    if not scene_path:
        raise RuntimeError("La escena no está guardada. Por favor guarda la escena antes de ejecutar el script.")

    print(f"Path completo de la escena: {scene_path}")

    # Normalizar el path para garantizar compatibilidad multiplataforma
    scene_path = os.path.normpath(scene_path)

    # Dividir el path en partes
    path_parts = scene_path.split(os.sep)
    print(f"Niveles del path: {path_parts}")

    # Extraer los nombres de secuencia (sequence) y shot
    sequence_name = path_parts[4]
    shot_name = path_parts[5]
    print(f"Nombre de la secuencia: {sequence_name}")
    print(f"Nombre del shot: {shot_name}")

    return sequence_name, shot_name


    split_output_dir = current_output_dir.split("/")






# Ejecutar la función
get_current_image_output_dir()

