@echo off
REM Simple build script for Windows

echo Building Erdlinge Scripts standalone executable for Windows...

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Create build directory
if not exist dist mkdir dist

echo Building standalone executable (browser-based)...

REM Build the executable using the spec file
pyinstaller build.spec --clean --noconfirm

echo Build completed!
echo Executable location: dist\ErdlingeScripts.exe

echo.
echo To run the application:
echo   Double-click dist\ErdlingeScripts.exe
echo.
echo The application will automatically open in your default browser!

pause