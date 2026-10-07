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
    --name="AutoSGS" ^
    --icon="assets/icon.ico" ^
    --version-file="packaging\version_info.txt" ^
    --add-data="assets/fonts;assets/fonts" ^
    --add-data="assets/icon.ico;assets" ^
    --collect-all="customtkinter" ^
    --hidden-import="pynput.keyboard._win32" ^
    --hidden-import="pynput.mouse._win32" ^
    main.py

if %ERRORLEVEL% EQU 0 (
    copy /y "dist\AutoSGS.exe" "dist\TUNorth - AutoSGS.exe" > nul
    copy /y "packaging\Unblock_AutoSGS.bat" "dist\" > nul
    copy /y "packaging\คำแนะนำการเปิดใช้งาน_SmartScreen.txt" "dist\" > nul

    echo Creating portable ZIP package...
    powershell -NoProfile -Command "Compress-Archive -Path 'dist\AutoSGS.exe', 'dist\Unblock_AutoSGS.bat', 'dist\คำแนะนำการเปิดใช้งาน_SmartScreen.txt' -DestinationPath 'dist\AutoSGS-Windows-Portable.zip' -Force"

    echo.
    echo ========================================================
    echo  [SUCCESS] Executables created successfully:
    echo    - dist\AutoSGS.exe
    echo    - dist\TUNorth - AutoSGS.exe
    echo    - dist\AutoSGS-Windows-Portable.zip
    echo    - dist\Unblock_AutoSGS.bat
    echo ========================================================
) else (
    echo.
    echo [ERROR] Build failed with error code %ERRORLEVEL%
)
