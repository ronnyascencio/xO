import sys


# Define el pipeline_path de manera explícita
pipeline_path = r"D:\Pipeline\xO"  # Ruta al directorio principal del pipeline
if pipeline_path not in sys.path:
    sys.path.append(pipeline_path)