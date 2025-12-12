# PyInstaller hook for KivyMD
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules, get_module_file_attribute
import os

# Collect all KivyMD modules, data, and binaries
datas, binaries, hiddenimports = collect_all('kivymd')

# Explicitly collect icon_definitions.py as source file
try:
    icon_def_path = get_module_file_attribute('kivymd.icon_definitions')
    if icon_def_path and os.path.exists(icon_def_path):
        # Add the icon_definitions.py file to datas so it gets bundled
        kivymd_dir = os.path.dirname(icon_def_path)
        datas.append((icon_def_path, 'kivymd'))
        print(f"[KivyMD Hook] Added icon_definitions.py from {icon_def_path}")
except Exception as e:
    print(f"[KivyMD Hook] Warning: Could not locate icon_definitions: {e}")

# Ensure icon_definitions is in hidden imports
hiddenimports += [
    'kivymd.icon_definitions',
]

# Collect all submodules to be safe
hiddenimports += collect_submodules('kivymd')

# Ensure fonts directory is included (KivyMD icons depend on fonts)
datas += collect_data_files('kivymd', includes=['**/*.ttf', '**/*.otf'])
