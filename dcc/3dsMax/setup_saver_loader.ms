-- setup_saver_loader.ms
-- Script de inicialización para configurar y lanzar el Saver Loader en 3ds Max

-- Definir la ruta al script de Python del Saver Loader
global saverLoaderPath = @"D:\Pipeline\xO\core\saver_loader"

-- Verificar si la ruta existe
if not doesFileExist (saverLoaderPath + "\\saver_loader.py") then (
    messageBox "Saver Loader script not found. Please verify the path in the setup script." title:"Saver Loader Error"
    return

try (
    -- Crear el menú "xO Tools" si no existe
    local xOToolsMenu = menuMan.findMenu "xO Tools"
    if xOToolsMenu == undefined then (
        local mainMenuBar = menuMan.getMainMenuBar()
        xOToolsMenu = menuMan.createMenu "xO Tools"

        -- Crear acción para lanzar el Saver Loader
        local saverLoaderActionItem = menuMan.createActionItem "SaverLoaderAction" "SaverLoaderCategory"
        saverLoaderActionItem.setMacroScript (
            "python.execute(\"" +
            "import sys; " +
            "sys.path.append('" + saverLoaderPath + "'); " +
            "from saver_loader import MainApp; " +
            "app = MainApp(); app.show()\")"
        )

        -- Agregar la acción al menú "xO Tools"
        xOToolsMenu.addItem saverLoaderActionItem -1
        mainMenuBar.addMenu xOToolsMenu mainMenuBar.numMenus
        menuMan.updateMenuBar()
        print "Saver Loader menu created successfully."
    )
) catch (
    messageBox "Error configuring the Saver Loader menu. Check your Python setup or the script path." title:"Saver Loader Error"
)

try (
    -- Lanzar automáticamente el Saver Loader al inicio
    python.execute (
        "import sys; " +
        "sys.path.append('" + saverLoaderPath + "'); " +
        "from saver_loader import MainApp; " +
        "app = MainApp(); app.show()"
    )
    print "Saver Loader launched successfully."
) catch (
    messageBox "Error launching Saver Loader. Ensure the Python environment and paths are configured correctly." title:"Saver Loader Error"
)
