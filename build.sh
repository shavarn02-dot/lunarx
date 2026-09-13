#!/usr/bin/env bash
# Fast cached build script for Render.com
set -o errexit

echo "==> Configuring pip cache directory..."
export PIP_CACHE_DIR="/opt/render/project/.cache/pip"
mkdir -p "$PIP_CACHE_DIR"

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing requirements with cache..."
pip install --cache-dir "$PIP_CACHE_DIR" -r requirements.txt

echo "==> Build completed successfully in fast-cache mode!"
