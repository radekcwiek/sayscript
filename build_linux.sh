#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

echo "Cleaning old build folders..."

rm -rf build
rm -rf dist

echo "Activating virtual environment..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing dependencies..."

pip install -r requirements.txt
pip install pyinstaller

echo "Building SayScript for Linux..."

pyinstaller ./SayScript.spec

echo "Build finished."
echo "Output: dist/SayScript"
