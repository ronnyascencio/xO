import os
import sys

def create_nuke_studio_structure(project_path):
    nuke_studio_path = os.path.join(project_path, "nukeStudio")
    subfolders = ["review", "output", "cache"]
    for folder in subfolders:
        path = os.path.join(nuke_studio_path, folder)
        os.makedirs(path, exist_ok=True)
        print(f"Carpeta creada: {path}")

if __name__ == "__main__":
    project_path = sys.argv[1]
    create_nuke_studio_structure(project_path)
