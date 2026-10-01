@echo off
chcp 65001 > nul
echo ========================================================
echo        Building AutoSGS Portable Windows Executable
echo ========================================================

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build Single-file Portable Executable with PyInstaller
pyinstaller --noconfirm --onefile --windowed ^
    --name="TUNorth - AutoSGS" ^
    --icon="assets/icon.ico" ^
    --add-data="assets/fonts;assets/fonts" ^
    --add-data="assets/icon.ico;assets" ^
    --collect-all="customtkinter" ^
    --hidden-import="pynput.keyboard._win32" ^
    --hidden-import="pynput.mouse._win32" ^
    main.py

if %ERRORLEVEL% EQU 0 (
    if exist "dist\TUNorth - AutoSGS.exe" (
        copy /y "dist\TUNorth - AutoSGS.exe" "dist\AutoSGS.exe" > nul
    )
    echo.
    echo ========================================================
    echo  [SUCCESS] Executables created successfully:
    echo    - dist\TUNorth - AutoSGS.exe
    echo    - dist\AutoSGS.exe
    echo ========================================================
) else (
    echo.
    echo [ERROR] Build failed with error code %ERRORLEVEL%
)
