from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
import os

# --- DEFINE ASSETS ---
# Include all KV files and asset folders
# Format: (Source Path, Destination Path)
added_files = [
    ('Main/', 'Main/'),
    ('assets/', 'assets/'),
    ('user_data.db', '.'),
]

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'kivymd.icon_definitions',
        'kivymd.app',
        'kivymd.uix.button',
        'kivymd.uix.card',
        'kivymd.uix.label',
        'kivymd.uix.screen',
        'kivymd.uix.boxlayout',
        'kivymd.uix.floatlayout',
        'kivymd.uix.fitimage',
        'kivymd.uix.textfield',
        'kivymd.uix.widget',
        'kivymd.uix.snackbar',
        'kivymd.uix.dialog',
        'sqlite3',
    ],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OctaTechApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Set to True if you want to see error logs in console during dev
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OctaTechApp',
)
