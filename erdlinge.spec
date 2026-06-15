# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller-Spec für das Erdlinge-Standalone-Programm.

Erzeugt eine eigenständige ausführbare Datei, die die Gradio-Oberfläche startet
und den Browser öffnet. Gradio (und einige seiner Abhängigkeiten) laden ihre
Frontend-Assets und weitere Ressourcen zur Laufzeit aus Datendateien; diese
müssen daher explizit in das Bundle aufgenommen werden.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Pakete, deren Datendateien (Templates, Frontend-Assets, version.txt, ...)
# zur Laufzeit benötigt werden.
_data_packages = [
    "gradio",
    "gradio_client",
    "safehttpx",
    "groovy",
]

datas = []
for _pkg in _data_packages:
    # ``include_py_files=True`` ist nötig, weil Gradio beim Import seine eigenen
    # Quelldateien einliest (z. B. um ``.pyi``-Stubs zu erzeugen). Ohne die
    # Python-Dateien im Bundle schlägt der Start mit FileNotFoundError fehl.
    datas += collect_data_files(_pkg, include_py_files=True)

# Eigene Module mitbündeln, damit ``app`` und die Skripte importierbar sind.
_local_modules = [
    "app.py",
    "aag_erstattungen.py",
    "abrechnungen.py",
    "ag_belastung.py",
    "lohnjournal.py",
    "kontoabgleich_gls.py",
    "kontoabgleich_paypal.py",
]
datas += [(m, ".") for m in _local_modules]

# Gradio nutzt dynamische Imports; submodules vollständig einsammeln.
hiddenimports = []
for _pkg in ["gradio", "gradio_client", "safehttpx", "groovy"]:
    hiddenimports += collect_submodules(_pkg)


a = Analysis(
    ["launcher.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="erdlinge-auswertungen",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
