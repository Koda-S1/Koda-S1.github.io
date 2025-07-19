#!/bin/bash

# Update package lists
sudo apt update

# Install Python3, pip, and PyQt6 dependencies
sudo apt install -y python3 python3-pip python3-pyqt6 python3-pyqt6.qtwebengine

# Optional: install flatpak if not installed
sudo apt install -y flatpak

# Add Flathub repo if missing
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
z