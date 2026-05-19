#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Python is required. Install Python 3, then run this again."
  exit 1
fi

if [ ! -f setup/config.json ]; then
  cp setup/config.example.json setup/config.json
  echo "Created setup/config.json from setup/config.example.json"
  echo "Edit setup/config.json, then run:"
  echo "  ./setup/setup.sh"
  exit 0
fi

$PYTHON setup/setup.py
