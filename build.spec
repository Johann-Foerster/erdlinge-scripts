# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Erdlinge Scripts Standalone App (Browser version)

import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path.cwd().absolute()
print("Current Directory:", current_dir)
sys.path.insert(0, str(current_dir))

a = Analysis(
    ['standalone_app.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=[
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ErdlingeScripts',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console for startup messages
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Add icon file path here if available
)
