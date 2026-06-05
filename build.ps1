$ErrorActionPreference = "Stop"

Write-Host "Cleaning old build files..."
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

Write-Host "Building Dictator..."
pyinstaller Dictator.spec

Write-Host "Build complete."
Write-Host "EXE:"
Write-Host ".\dist\Dictator\Dictator.exe"
