@echo off
REM Enhanced build script for Windows

echo Building Erdlinge Scripts standalone executables for Windows...

REM Install PyInstaller and PyWebView if not already installed
pip install pyinstaller pywebview

REM Create build directory
if not exist dist mkdir dist

echo Building standard standalone executable (browser-based)...

REM Build the standard executable using the spec file
pyinstaller build.spec --clean --noconfirm

echo Building desktop executable (native window with PyWebView)...

REM Build the desktop executable using the desktop spec file
pyinstaller build_desktop.spec --clean --noconfirm

echo Build completed!
echo Standard executable location: dist\ErdlingeScripts.exe
echo Desktop executable location: dist\ErdlingeScriptsDesktop.exe

echo.
echo To run the applications:
echo   Standard (Browser) Version: Double-click dist\ErdlingeScripts.exe
echo   Desktop (Native Window) Version: Double-click dist\ErdlingeScriptsDesktop.exe
echo.
echo The desktop version provides a native window experience!

pause