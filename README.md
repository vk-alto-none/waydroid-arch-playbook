# 🚀 Waydroid on Arch Linux (LTS Kernel 6.x & LXC 7) — Complete Playbook & Troubleshooting Bible

A battle-tested, production-ready engineering guide, automated fix scripts, and root-cause post-mortem for running **Waydroid Android Container Subsystem** with **ARM64 Translation (`libndk`)**, **Hardware GPU Acceleration**, and **App Stores / Gaming** on **Arch Linux (Wayland & KDE Plasma 6)**.

---

## ⚡ Quick Start (Automated 1-Click Fix)

If you are setting up Waydroid on a fresh Arch Linux system or facing container start / binder errors:

```bash
git clone https://github.com/vk-alto-none/waydroid-arch-playbook.git
cd waydroid-arch-playbook
sudo python3 scripts/auto_fix_waydroid.py
```

Then start the session as your regular user:
```bash
waydroid session start &
waydroid show-full-ui &
```

---

## 📑 Documentation Index

| Guide | Description |
|:---|:---|
| 📖 [**Kernel & BinderFS Setup**](docs/01_ARCH_LINUX_KERNEL_BINDERFS.md) | Arch Linux BinderFS nodes (`/dev/binderfs/anbox-*`), udev rules, permissions, and systemd tmpfiles. |
| 🛠️ [**LXC 7 Compatibility & Code Patches**](docs/02_LXC7_WAYDROID_COMPATIBILITY.md) | Resolving LXC 7 relative path enforcement, tmpfs mount type fixes, and patching `lxc.py`. |
| ⚙️ [**ARM64 Translation (`libndk` / `libhoudini`)**](docs/03_ARM64_TRANSLATION_LIBNDK.md) | Running native ARM64 games and apps on x86_64 AMD/Intel CPUs. |
| 🎮 [**App Stores & Heavy Game (OBB) Staging**](docs/04_GAMING_AND_OBB_STAGING.md) | Sideloading APKPure, Aurora Store, F-Droid, multi-GB OBB game data, anti-freeze/anti-suspend settings. |
| 🔍 [**Troubleshooting & Error Directory**](docs/05_DEBUGGING_AND_ERROR_SOLUTIONS.md) | Comprehensive table of every error message, root-cause, and exact fix. |

---

## 🏗️ Architecture & Core Components

```
+-------------------------------------------------------------+
|                      Host Linux OS (Arch Linux)             |
|  - Kernel: 6.18+ LTS with BinderFS (/dev/binderfs/anbox-*)   |
|  - Compositor: Wayland / KDE Plasma 6 (wayland-0)           |
|  - GPU: Mesa / GBM Render Nodes (/dev/dri/renderD129)       |
+-------------------------------------------------------------+
                              │
                    D-Bus / Session Socket
                              │
+-------------------------------------------------------------+
|                      LXC 7 Container Layer                  |
|  - Image: LineageOS 18.1 (GAPPS / VANILLA)                  |
|  - Rootfs: OverlayFS (system.img + vendor.img)              |
|  - Mounts: Strict relative destinations (run/xdg, dev/binder) |
|  - ARM Engine: libndk translation (ARM64 -> x86_64)         |
+-------------------------------------------------------------+
                              │
+-------------------------------------------------------------+
|                  Android Android Subsystem                  |
|  - SurfaceFlinger / HWComposer: Wayland Surface Output       |
|  - Services: Google Play Store, APKPure, F-Droid, Games     |
+-------------------------------------------------------------+
```

---

## 🎯 Supported Features
- ✅ **LXC 7 Support:** Strips illegal leading slashes in container mount entries.
- ✅ **BinderFS Automation:** Automatically links and grants `0666` permissions to `/dev/binderfs/anbox-*`.
- ✅ **Native ARM64 Gaming:** Pre-configured with `libndk` for AMD/Intel architecture.
- ✅ **Anti-Sleep / Anti-Freeze:** Prevents Waydroid from freezing into deep sleep when switching windows.
- ✅ **GPU Passthrough:** Direct hardware acceleration via Mesa `gbm` gralloc.

---

## 📜 License
MIT License. Built with ❤️ for the Linux & Arch Community by **Durbhasi Gurukulam Private Limited (DGPL)**.
