#!/bin/bash
set -e

echo "========================================================"
echo "        Building AutoSGS Standalone App for macOS"
echo "========================================================"

# Clean previous builds
rm -rf build dist

ICON_ARG=""
if [ -f "assets/icon.icns" ]; then
    ICON_ARG="--icon=assets/icon.icns"
fi

# PyInstaller for macOS
pyinstaller --noconfirm --onedir --windowed \
    --name="AutoSGS" \
    $ICON_ARG \
    --add-data="assets/fonts:assets/fonts" \
    --collect-all="customtkinter" \
    --hidden-import="pynput.keyboard._darwin" \
    --hidden-import="pynput.mouse._darwin" \
    main.py

echo "Creating compressed distribution archive..."
cd dist
zip -r "AutoSGS-macOS.zip" "AutoSGS.app"
cd ..

echo "========================================================"
echo " [SUCCESS] AutoSGS.app and AutoSGS-macOS.zip created in dist/"
echo "========================================================"
