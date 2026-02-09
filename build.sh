#!/bin/bash
set -e

echo "🔨 Building SlotSignalsBot..."

# Обновить pip
pip install --upgrade pip setuptools wheel

# Установить зависимости
pip install -r requirements.txt

echo "✅ Build completed successfully!"
