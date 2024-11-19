import sys
import os
import nuke

# Define the path to saver_loader.py
current_dir = os.path.dirname(__file__)  # Directory of menu.py
saver_loader_path = os.path.join(current_dir, "..", "..", "core", "saver_loader", "saver_loader.py")
saver_loader_dir = os.path.dirname(saver_loader_path)

# Function to open the saver/loader UI
def show_saver_loader():
    # Set DCC explicitly to Nuke
    os.environ["DCC"] = "Nuke"
    print("[DEBUG]  Saver Loader in Nuke")
    print(f"[DEBUG] Saver Loader Path: {saver_loader_path}")

    if saver_loader_dir not in sys.path:
        sys.path.append(saver_loader_dir)
        print(f"[DEBUG] Added a sys.path: {saver_loader_dir}")

    try:
        from saver_loader import MainApp  # Import the main application class
    except ImportError as e:
        nuke.message(f"Error loading saver_loader: {e}")
        print(f"[DEBUG] Error at import  saver_loader: {e}")
        return

    global main_window
    try:
        # Close any existing instance of the window
        if main_window is not None:
            main_window.close()
    except NameError:
        pass  # If main_window is not defined, it's fine to ignore

    try:
        # Initialize and show the UI
        main_window = MainApp()
        main_window.show()
    except Exception as e:
        nuke.message(f"Error initializing Saver Loader: {e}")
        print(f"[DEBUG] Error starting  MainApp: {e}")


# Add a custom menu in Nuke
menu = nuke.menu("Nuke")
custom_menu = menu.addMenu("xO")  # Add a custom menu named "xO"
custom_menu.addCommand("Saver Loader", show_saver_loader)
