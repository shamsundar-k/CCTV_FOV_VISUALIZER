#!/usr/bin/env bash
set -e
echo "Installing PyInstaller..."
uv add --dev pyinstaller

echo "Building..."
uv run pyinstaller CCTV_FOV_Visualiser.spec --clean

echo ""
echo "Done. Distribute the folder: dist/CCTV_FOV_Visualiser/"
echo "Zip it with: zip -r CCTV_FOV_Visualiser_linux.zip dist/CCTV_FOV_Visualiser/"
