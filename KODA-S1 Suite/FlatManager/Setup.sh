#!/bin/bash
set -e

echo "Updating package lists..."
sudo apt update

echo "Installing essential system packages..."
sudo apt install -y python3 python3-pip python3-dev python3-setuptools python3-venv build-essential \
    libgl1-mesa-glx libglib2.0-0 libpulse0 libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-render0 \
    libxcb-shm0 libxcb-keysyms1 libxcb-randr0 libxcb-xfixes0 libxcb-sync1 libxcb-xkb1 libxkbcommon-x11-0 \
    libxkbcommon0 libx11-xcb1 libasound2 libxtst6 flatpak wget curl

echo "Upgrading pip and installing Python packages..."
pip3 install --upgrade pip
pip3 install PyQt6 PyQt6-WebEngine

echo "Adding Flathub repository (if missing)..."
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

APP_DIR="$HOME/FlatpakInstallerApp"
APP_SCRIPT="$APP_DIR/index.py"

echo "Creating application directory at $APP_DIR..."
mkdir -p "$APP_DIR"

echo "Downloading latest PyQt6 app from GitHub..."
wget -O "$APP_SCRIPT" "https://raw.githubusercontent.com/Koda-S1/Koda-S1.github.io/main/KODA-S1%20Suite/FlatManager/index.py"

echo "Running the PyQt6 Flatpak Installer app..."
python3 "$APP_SCRIPT"
