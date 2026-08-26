#!/usr/bin/env bash
# Complete Waydroid Installer & Configurator for Arch Linux
# Author: Durbhasi Gurukulam Private Limited (DGPL)

set -e

if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run as root (sudo ./install_waydroid_complete.sh)"
  exit 1
fi

echo "🚀 Installing Waydroid dependencies on Arch Linux..."
pacman -Sy --needed --noconfirm waydroid lxc dnsmasq iptables python-gobject python-requests

echo "🛠️ Running Auto-Fix Engine..."
python3 "$(dirname "$0")/auto_fix_waydroid.py"

echo "⚡ Initializing Waydroid GAPPS image if not initialized..."
if [ ! -f /var/lib/waydroid/images/system.img ]; then
  waydroid init -s GAPPS
fi

systemctl enable --now waydroid-container.service
echo "✅ Installation & Setup Complete! Run 'waydroid session start' as regular user."
