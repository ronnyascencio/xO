import os




vfx_path = os.getenv("VFX")
if not vfx_path:
    print("Error", "The variable 'VFX' is not configured.")

print(vfx_path)