import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide2.QtCore import QStringListModel, QFile, QIODevice
from PySide2.QtUiTools import QUiLoader


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.dcc = os.getenv("DCC", "Maya")  # Asume Maya como predeterminado si DCC no está configurado
        print(f"[DEBUG] DCC detectado: {self.dcc}")  # Depuración: DCC activo
        self.init_ui()
        self.setup_connections()
        self.populate_shows()

    def init_ui(self):
        ui_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "ui/saver_loader.ui"))
        ui_file = QFile(ui_file_path)
        ui_file.open(QIODevice.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)
        self.setCentralWidget(self.ui)
        ui_file.close()

    def setup_connections(self):
        self.ui.cbb_show.currentTextChanged.connect(self.populate_sequences)
        self.ui.cbb_sequence.currentTextChanged.connect(self.populate_shots)
        self.ui.cbb_task.currentTextChanged.connect(self.on_task_changed)
        self.ui.btn_save.clicked.connect(self.save_file)
        self.ui.btn_open.clicked.connect(self.open_file)
        self.ui.btn_refresh.clicked.connect(self.refresh_versions)

    def get_base_path(self):
        vfx_path = os.getenv("VFX")
        if not vfx_path:
            QMessageBox.critical(self, "Error", "La variable de entorno 'VFX' no está configurada.")
            sys.exit(1)
        return os.path.join(vfx_path, "Project")

    def populate_shows(self):
        base_path = self.get_base_path()
        if not os.path.exists(base_path):
            QMessageBox.warning(self, "Error", f"No se encontró la carpeta: {base_path}")
            return

        shows = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        print(f"[DEBUG] Base Path: {base_path}")
        print(f"[DEBUG] Shows detectados: {shows}")
        self.ui.cbb_show.clear()
        self.ui.cbb_show.addItems(shows)

    def populate_sequences(self):
        show = self.ui.cbb_show.currentText()
        if not show:
            return

        base_path = self.get_base_path()
        sequences_path = os.path.join(base_path, show, "scenes")

        if not os.path.exists(sequences_path):
            QMessageBox.warning(self, "Error", f"No se encontró la carpeta: {sequences_path}")
            return

        sequences = [d for d in os.listdir(sequences_path) if os.path.isdir(os.path.join(sequences_path, d))]
        print(f"[DEBUG] Sequences Path: {sequences_path}")
        print(f"[DEBUG] Sequences detectadas: {sequences}")
        self.ui.cbb_sequence.clear()
        self.ui.cbb_sequence.addItems(sequences)

    def populate_shots(self):
        show = self.ui.cbb_show.currentText()
        sequence = self.ui.cbb_sequence.currentText()
        if not show or not sequence:
            return

        base_path = self.get_base_path()
        shots_path = os.path.join(base_path, show, "scenes", sequence)

        if not os.path.exists(shots_path):
            print(f"[DEBUG] Shots Path no encontrado: {shots_path}")
            QMessageBox.warning(self, "Error", f"No se encontró la carpeta: {shots_path}")
            return

        shots = [d for d in os.listdir(shots_path) if os.path.isdir(os.path.join(shots_path, d))]
        print(f"[DEBUG] Shots Path: {shots_path}")
        print(f"[DEBUG] Shots detectados: {shots}")
        self.ui.cbb_shot.clear()
        self.ui.cbb_shot.addItems(shots)

    def on_task_changed(self):
        task = self.ui.cbb_task.currentText()
        print(f"[DEBUG] Tarea seleccionada: {task}")

        # Para tareas específicas en Maya, habilita los campos de asset
        if self.dcc == "Maya" and task in ["Modeling", "Shading", "Look Dev", "Rigging"]:
            self.ui.cbb_asset.setEnabled(True)
            self.ui.line_assetname.setEnabled(True)
            self.ui.cb_active.setEnabled(True)
        else:
            # Desactiva los campos de asset para otras tareas
            self.ui.cbb_asset.setEnabled(False)
            self.ui.line_assetname.setEnabled(False)
            self.ui.cb_active.setEnabled(False)

        # Actualiza la información de la ruta al cambiar la tarea
        try:
            self.update_path_info()
        except Exception as e:
            print(f"[DEBUG] Error al actualizar la ruta: {e}")
            QMessageBox.warning(self, "Error", "No se pudo actualizar la ruta de guardado.")

    def get_save_path(self):
        show = self.ui.cbb_show.currentText()
        sequence = self.ui.cbb_sequence.currentText()
        shot = self.ui.cbb_shot.currentText()
        task = self.ui.cbb_task.currentText()
        base_path = self.get_base_path()

        # Verificar que 'show' y 'task' estén seleccionados
        if not show or not task:
            print("[DEBUG] Error: 'show' o 'task' no seleccionado.")
            return None

        if self.dcc == "Nuke":
            if task in ["Compositing", "Prep"]:
                if not sequence or not shot:
                    print("[DEBUG] Error: 'sequence' o 'shot' no seleccionado para Nuke.")
                    return None
                return os.path.join(base_path, show, "scenes", sequence, shot, "nuke", "script")

        elif self.dcc == "Maya":
            if task in ["Layout", "Lighting", "Tracking", "FX"]:
                if not sequence or not shot:
                    print("[DEBUG] Error: 'sequence' o 'shot' no seleccionado para Maya.")
                    return None
                return os.path.join(base_path, show, "scenes", sequence, shot, "maya")

            elif task in ["Modeling", "Shading", "Rigging", "Look Dev"]:
                asset_type = self.ui.cbb_asset.currentText()
                if not asset_type:
                    print("[DEBUG] Error: 'asset_type' no seleccionado para tareas de assets en Maya.")
                    return None
                return os.path.join(base_path, show, "assets", asset_type)

        print(f"[DEBUG] Invalid task or DCC configuration: Task={task}, DCC={self.dcc}")
        return None

    def generate_filename(self):
        version = 1
        task = self.ui.cbb_task.currentText()
        ext = ".ma" if self.dcc == "Maya" else ".nk"
        name_components = [self.ui.cbb_show.currentText()]

        if self.dcc == "Maya" and task in ["Modeling", "Shading", "Look Dev", "Rigging"]:
            name_components.append(self.ui.line_assetname.text())
        else:
            name_components.extend([self.ui.cbb_sequence.currentText(), self.ui.cbb_shot.currentText(), task])

        name_components.append(f"v{version:03}")
        filename = "_".join(name_components) + ext
        save_path = self.get_save_path()

        while os.path.exists(os.path.join(save_path, filename)):
            version += 1
            name_components[-1] = f"v{version:03}"
            filename = "_".join(name_components) + ext

        print(f"[DEBUG] Generating filename: {filename}")
        return filename

    def open_file(self):
        selected = self.ui.list_scripts_versions.currentIndex().data()
        if not selected:
            QMessageBox.warning(self, "Error", "No has seleccionado ningún archivo.")
            return

        file_path = os.path.join(self.get_save_path(), selected)

        # Abrir archivo en el DCC correspondiente
        if self.dcc == "Maya":
            import maya.cmds as cmds
            cmds.file(file_path, open=True, force=True)
        elif self.dcc == "Nuke":
            import nuke
            nuke.scriptOpen(file_path)

        QMessageBox.information(self, "Abrir", f"Abriendo archivo: {file_path}")

    def save_file(self):
        save_path = self.get_save_path()
        if not save_path:
            QMessageBox.warning(self, "Error", "No se pudo determinar la ruta de guardado.")
            return

        filename = self.generate_filename()
        file_path = os.path.join(save_path, filename)
        os.makedirs(save_path, exist_ok=True)

        if self.dcc == "Maya":
            import maya.cmds as cmds
            cmds.file(rename=file_path)
            cmds.file(save=True, type="mayaAscii")
        elif self.dcc == "Nuke":
            import nuke
            nuke.scriptSaveAs(file_path)

        QMessageBox.information(self, "Guardado", f"Archivo guardado: {file_path}")
        self.refresh_versions()

    def refresh_versions(self):
        save_path = self.get_save_path()
        print(f"[DEBUG] Refresh Versions: Save Path = {save_path}")

        if not save_path or not os.path.exists(save_path):
            self.ui.list_scripts_versions.setModel(QStringListModel())
            return

        ext = ".nk" if self.dcc == "Nuke" else ".ma"
        try:
            versions = [f for f in os.listdir(save_path) if f.endswith(ext)]
            print(f"[DEBUG] Found versions: {versions}")
        except Exception as e:
            print(f"[DEBUG] Error al listar versiones: {e}")
            versions = []

        self.ui.list_scripts_versions.setModel(QStringListModel(versions))

    def update_path_info(self):
        save_path = self.get_save_path()
        if save_path:
            print(f"[DEBUG] Ruta de guardado actual: {save_path}")
            self.refresh_versions()
        else:
            QMessageBox.warning(self, "Advertencia", "No se pudo determinar la ruta de guardado.")
            self.ui.list_scripts_versions.setModel(QStringListModel())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
