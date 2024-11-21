import hou
import sys
import os

# Define la ruta de saver_loader.py
pipeline_path = r"D:/Pipeline/xO/core"
if pipeline_path not in sys.path:
    sys.path.append(pipeline_path)

def saver_loader():
    """Alias para abrir la herramienta Saver Loader."""
    from saver_loader import MainApp
    app = hou.ui.mainQtWindow()
    window = MainApp()
    window.show()
