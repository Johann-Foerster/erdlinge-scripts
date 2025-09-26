@echo off
REM Build script for Windows

echo Building Erdlinge Scripts standalone executable for Windows...

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Create build directory
if not exist dist mkdir dist

echo Building standalone executable...

REM Build the executable using the spec file
pyinstaller build.spec --clean --noconfirm

echo Build completed!
echo Executable location: dist\ErdlingeScripts.exe

echo To run the application, double-click dist\ErdlingeScripts.exe

pause