import os
import sys
import shutil


def ingest_plates(project_path, plates_folder):
    sourceimages_path = os.path.join(project_path, "sourceimages")
    os.makedirs(sourceimages_path, exist_ok=True)

    for filename in os.listdir(plates_folder):
        if filename.endswith(('.jpg', '.exr', '.png', '.tif')):  # Formatos admitidos
            src_file = os.path.join(plates_folder, filename)
            dest_file = os.path.join(sourceimages_path, f"plate_{filename}")
            shutil.copy2(src_file, dest_file)
            print(f"Plate copiado: {dest_file}")


if __name__ == "__main__":
    project_path = sys.argv[1]
    plates_folder = input("Ingrese la ruta de la carpeta de plates: ")
    ingest_plates(project_path, plates_folder)
