@echo off
chcp 65001 > nul
title AutoSGS - ปลดล็อกความปลอดภัย Windows
echo ======================================================================
echo    AutoSGS - สคริปต์ช่วยปลดล็อกความปลอดภัย Windows SmartScreen
echo ======================================================================
echo.
echo กำลังปลดล็อกการจำกัดการเข้าถึงจากอินเทอร์เน็ต (Mark of the Web)...

powershell -NoProfile -ExecutionPolicy Bypass -Command "if (Test-Path '%~dp0AutoSGS.exe') { Unblock-File -Path '%~dp0AutoSGS.exe' }; if (Test-Path '%~dp0TUNorth - AutoSGS.exe') { Unblock-File -Path '%~dp0TUNorth - AutoSGS.exe' }" 2>nul

echo.
echo [สำเร็จ] ปลดล็อกความปลอดภัยเรียบร้อยแล้ว!
echo กำลังเริ่มต้นโปรแกรม AutoSGS...
echo.

if exist "%~dp0AutoSGS.exe" (
    start "" "%~dp0AutoSGS.exe"
) else if exist "%~dp0TUNorth - AutoSGS.exe" (
    start "" "%~dp0TUNorth - AutoSGS.exe"
) else (
    echo [แจ้งเตือน] ไม่พบไฟล์ AutoSGS.exe ในโฟลเดอร์นี้ กรุณาวางสคริปต์ไว้ข้างไฟล์โปรแกรม
    pause
)
