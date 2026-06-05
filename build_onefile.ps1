$ErrorActionPreference = "Stop"

Write-Host "Cleaning old build files..."
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

Write-Host "Building Dictator onefile EXE..."
pyinstaller --onefile --windowed --name Dictator main.py

Write-Host "Build complete."
Write-Host "EXE:"
Write-Host ".\dist\Dictator.exe"
