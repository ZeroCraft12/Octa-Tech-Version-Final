# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules
import os

# Get the project root directory
project_root = os.path.dirname(os.path.abspath('main.py'))

# Collect ALL KivyMD data, binaries, and submodules using collect_all
kivymd_datas, kivymd_binaries, kivymd_hiddenimports = collect_all('kivymd')

# Collect all KivyMD submodules to ensure nothing is missed
all_kivymd_submodules = collect_submodules('kivymd')

# Add project-specific data files
project_datas = [
    ('Main', 'Main'),  # Include all Main directory contents
    ('*.png', '.'),    # Include splash screen images
    ('*.db', '.'),     # Include database files
    ('*.json', '.'),   # Include JSON data files
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=kivymd_binaries,
    datas=kivymd_datas + project_datas,
    hiddenimports=[
        # Explicitly include icon_definitions (critical for KivyMD 2.0+)
        'kivymd.icon_definitions',
        'kivymd.icon_definitions.md_icons',
        # Project screens
        'Main.libs.screens.login',
        'Main.libs.screens.signup',
        'Main.libs.screens.firstpage',
        'Main.libs.screens.home',
        'Main.libs.screens.reviewscreen',
        'Main.libs.screens.tabunganscreen',
        'Main.libs.screens.rekomendasi_gadget',
        'Main.libs.screens.wishlistscreen',
        'Main.libs.screens.profilescreen',
    ] + kivymd_hiddenimports + all_kivymd_submodules,
    hookspath=['.'],  # Use custom hook in current directory
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
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
