import sys
import os
try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
    from PySide6.QtCore import QStringListModel, QFile, QIODevice
    from PySide6.QtUiTools import QUiLoader
    print("[DEBUG] Using PySide6")
except ImportError:
    try:
        from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox
        from PySide2.QtCore import QStringListModel, QFile, QIODevice
        from PySide2.QtUiTools import QUiLoader
        print("[DEBUG] Using PySide2")
    except ImportError as e:
        raise ImportError(f"Neither PySide6 nor PySide2 could be imported: {e}")



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
        self.ui.cbb_show.currentTextChanged.connect(self.populate_shots)
        self.ui.cbb_task.currentTextChanged.connect(self.on_task_changed)
        self.ui.btn_save.clicked.connect(self.save_file)
        self.ui.btn_open.clicked.connect(self.open_file)
        self.ui.btn_refresh.clicked.connect(self.refresh_versions)

    def get_base_path(self):
        vfx_path = os.getenv("VFX")
        if not vfx_path:
            QMessageBox.critical(self, "Error", "The variable 'VFX' is not configured.")
            sys.exit(1)
        return os.path.join(vfx_path, "Project")

    def populate_shows(self):
        base_path = self.get_base_path()
        if not os.path.exists(base_path):
            QMessageBox.warning(self, "Error", f"Directory not found: {base_path}")
            return

        shows = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        print(f"[DEBUG] Base Path: {base_path}")
        print(f"[DEBUG] Shows detected: {shows}")
        self.ui.cbb_show.clear()
        self.ui.cbb_show.addItems(shows)

    def populate_shots(self):
        """
        Busca directamente los shots en el directorio de shots de un show.
        """
        show = self.ui.cbb_show.currentText()
        if not show:
            print("[DEBUG] Error: No show selected.")
            return

        base_path = self.get_base_path()
        shots_path = os.path.join(base_path, show, "shots")  # Cambiado para apuntar directamente a shots

        if not os.path.exists(shots_path):
            print(f"[DEBUG] Shots Path not found: {shots_path}")
            QMessageBox.warning(self, "Error", f"Shots directory not found: {shots_path}")
            return

        # Busca todas las carpetas dentro de 'shots'
        shots = [d for d in os.listdir(shots_path) if os.path.isdir(os.path.join(shots_path, d))]
        print(f"[DEBUG] Shots Path: {shots_path}")
        print(f"[DEBUG] Shots detected: {shots}")
        self.ui.cbb_shot.clear()
        self.ui.cbb_shot.addItems(shots)

    def on_task_changed(self):
        task = self.ui.cbb_task.currentText()
        print(f"[DEBUG] Task selected: {task}")
        self.update_path_info()

        if self.dcc == "Maya" and task in ["Modeling", "Shading", "Look Dev", "Rigging"]:
            self.ui.cbb_asset.setEnabled(True)
            self.ui.line_assetname.setEnabled(True)
            self.ui.cb_active.setEnabled(True)
        else:
            self.ui.cbb_asset.setEnabled(False)
            self.ui.line_assetname.setEnabled(False)
            self.ui.cb_active.setEnabled(False)

    def get_save_path(self):
        """
        Generates the save path based on DCC, task, show, and shot/asset.
        """
        show = self.ui.cbb_show.currentText()
        task = self.ui.cbb_task.currentText()
        base_path = self.get_base_path()
        dcc = self.dcc

        if not show or not task:
            print("[DEBUG] Error: 'show' or 'task' not selected.")
            return None

        if task in ["Modeling", "Rigging", "Shading", "Look Dev"]:
            asset_type = self.ui.cbb_asset.currentText()
            if not asset_type:
                print("[DEBUG] Error: 'asset_type' not selected for asset tasks.")
                QMessageBox.warning(self, "Error", "Please select an asset type.")
                return None
            return os.path.join(base_path, show, "assets", asset_type)
        else:
            shot = self.ui.cbb_shot.currentText()
            if not shot:
                print("[DEBUG] Error: 'shot' not selected.")
                QMessageBox.warning(self, "Error", "Please select a shot.")
                return None
            return os.path.join(base_path, show, "shots", shot, task.lower(), dcc.lower(), "script")

    def generate_filename(self):
        """
        Generates the filename based on the convention:
        [assetname]_[task]_v[version].[ext] for assets
        [shot]_[task]_v[version].[ext] for shots
        """
        version = 1
        task = self.ui.cbb_task.currentText()
        ext = ".hiplc" if self.dcc == "Houdini" else ".ma" if self.dcc == "Maya" else ".nk"

        # Determine naming based on asset or shot
        if task in ["Modeling", "Rigging", "Shading", "Look Dev"]:
            asset_name = self.ui.line_assetname.text()
            if not asset_name:
                print("[DEBUG] Error: 'asset_name' not provided for asset tasks.")
                QMessageBox.warning(self, "Error", "Please enter a valid asset name.")
                return None
            # Asset naming convention
            filename = f"{asset_name}_{task}_v{version:03}{ext}"
        else:
            shot = self.ui.cbb_shot.currentText()
            if not shot or not task:
                print("[DEBUG] Error: 'shot' or 'task' not selected.")
                QMessageBox.warning(self, "Error", "Please select a shot and task.")
                return None
            # Shot naming convention
            filename = f"{shot}_{task}_v{version:03}{ext}"

        save_path = self.get_save_path()
        if not save_path:
            print("[DEBUG] Error: Save path could not be determined.")
            QMessageBox.warning(self, "Error", "Save path could not be determined.")
            return None

        # Increment version if filename exists
        while os.path.exists(os.path.join(save_path, filename)):
            version += 1
            if task in ["Modeling", "Rigging", "Shading", "Look Dev"]:
                filename = f"{asset_name}_{task}_v{version:03}{ext}"
            else:
                filename = f"{shot}_{task}_v{version:03}{ext}"

        print(f"[DEBUG] Generating filename: {filename}")
        return filename

    def open_file(self):
        selected = self.ui.list_scripts_versions.currentIndex().data()
        if not selected:
            QMessageBox.warning(self, "Error", "Haven't selected a file.")
            return

        file_path = os.path.join(self.get_save_path(), selected)

        if self.dcc == "Maya":
            import maya.cmds as cmds
            cmds.file(file_path, open=True, force=True)
        elif self.dcc == "Nuke":
            import nuke
            nuke.scriptOpen(file_path)
        elif self.dcc == "Houdini":
            hou.hipFile.load(file_path, suppress_save_prompt=True)

        QMessageBox.information(self, "Open", f"Opening file: {file_path}")

    def save_file(self):
        save_path = self.get_save_path()
        if not save_path:
            QMessageBox.warning(self, "Error", "Couldn't determine the save path.")
            return

        filename = self.generate_filename()
        if not filename:
            return

        file_path = os.path.join(save_path, filename)
        os.makedirs(save_path, exist_ok=True)

        print(f"[DEBUG] Saving file to: {file_path}")

        if self.dcc == "Maya":
            import maya.cmds as cmds
            cmds.file(rename=file_path)
            cmds.file(save=True, type="mayaAscii")
        elif self.dcc == "Nuke":
            import nuke
            nuke.scriptSaveAs(file_path)
        elif self.dcc == "Houdini":
            hou.hipFile.save(file_path)

        QMessageBox.information(self, "Saved", f"File Saved: {file_path}")
        self.refresh_versions()

    def refresh_versions(self):
        """
        Actualiza la lista de versiones disponibles para la tarea seleccionada en la interfaz.
        """
        save_path = self.get_save_path()
        print(f"[DEBUG] Refresh Versions: Save Path = {save_path}")

        if not save_path or not os.path.exists(save_path):
            print("[DEBUG] Save path is invalid or does not exist.")
            self.ui.list_scripts_versions.setModel(QStringListModel())
            return

        ext = ".hiplc" if self.dcc == "Houdini" else ".ma" if self.dcc == "Maya" else ".nk"
        task_filter = self.ui.cbb_task.currentText()

        try:
            versions = [
                f for f in os.listdir(save_path)
                if f.endswith(ext) and task_filter in f
            ]
            print(f"[DEBUG] Found versions filtered by task '{task_filter}': {versions}")
        except Exception as e:
            print(f"[DEBUG] Error listing versions: {e}")
            versions = []

        self.ui.list_scripts_versions.setModel(QStringListModel(versions))

    def update_path_info(self):
        save_path = self.get_save_path()
        if save_path:
            print(f"[DEBUG] Save Path: {save_path}")
            self.refresh_versions()
        else:
            QMessageBox.warning(self, "Warning", "Could not determine the save path.")
            self.ui.list_scripts_versions.setModel(QStringListModel())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())