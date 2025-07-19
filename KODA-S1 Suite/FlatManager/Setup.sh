#!/bin/bash
set -e

echo "Updating package lists..."
sudo apt update

echo "Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

echo "Installing PyQt6 and PyQt6-WebEngine..."
pip3 install --upgrade pip
pip3 install PyQt6 PyQt6-WebEngine

echo "Installing Flatpak..."
sudo apt install -y flatpak

echo "Adding Flathub repository (if missing)..."
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

APP_DIR="$HOME/FlatpakInstallerApp"
APP_SCRIPT="$APP_DIR/index.py"

echo "Downloading your PyQt6 app..."
mkdir -p "$APP_DIR"

# Adjust this URL to point to your main Python app script raw URL on GitHub
wget -O "$APP_SCRIPT" "https://raw.githubusercontent.com/Koda-S1/Koda-S1.github.io/main/KODA-S1%20Suite/FlatManager/index.py"

echo "Running the PyQt6 Flatpak Installer app..."
python3 "$APP_SCRIPT"
