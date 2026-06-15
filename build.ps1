$ErrorActionPreference = "Stop"

Write-Host "Cleaning old build files..."
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

Write-Host "Building SayScript..."
pyinstaller SayScript.spec

Write-Host "Build complete."
Write-Host "EXE:"
Write-Host ".\dist\SayScript\SayScript.exe"
