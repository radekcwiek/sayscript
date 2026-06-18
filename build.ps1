$ErrorActionPreference = "Stop"

Write-Host "Cleaning old build folders..."

Remove-Item -Recurse -Force .\build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .\dist -ErrorAction SilentlyContinue

Write-Host "Building SayScript..."

pyinstaller .\SayScript.spec

Write-Host "Build finished."
Write-Host "Output: dist\SayScript"
