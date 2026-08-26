# 📱 Waydroid Complete Operational Cheat Sheet

Comprehensive quick-reference guide for managing, configuring, and troubleshooting Waydroid on Arch Linux (LXC 7, Wayland / KDE Plasma 6).

---

## ⚡ 1. Quick Start & Stop Lifecycle

| Action | Command | Notes |
|:---|:---|:---|
| **1-Command Full Launch** | `sudo systemctl start waydroid-container && waydroid session start & sleep 2 && waydroid show-full-ui &` | Boots container, user session & launches UI. |
| **Start Container Service** | `sudo systemctl start waydroid-container.service` | Starts the background LXC container daemon. |
| **Start User Session** | `waydroid session start &` | Initializes Wayland session & SurfaceFlinger bridge. |
| **Open Android GUI (Tablet Window)** | `waydroid show-full-ui &` | Shows the full Android graphical workspace. |
| **Check Live Status** | `waydroid status` | Displays container, session, IP, and display status. |
| **Quick Session Exit (CLI)** | `waydroid-exit` | Custom helper script (or `waydroid session stop`). |
| **Stop User Session** | `waydroid session stop` | Gracefully closes active Android windows and session. |
| **Stop Background Container** | `sudo systemctl stop waydroid-container.service` | Full shutdown of the LXC container. |
| **Complete Clean Restart** | `sudo systemctl restart waydroid-container.service && sleep 2 && waydroid session start &` | Hard reset of container stack. |

---

## 🎮 2. Display, Resolution & Window Management

| Feature | Command / Shortcut | Description |
|:---|:---|:---|
| **Toggle Fullscreen** | `waydroid-fullscreen` | Custom KWin Wayland toggle script. |
| **KDE Fullscreen Shortcut** | Press `Alt + F3` on window $\to$ *More Actions* $\to$ *Fullscreen* | Native KDE window management. |
| **Lock Native 1080p (1920x1080)** | `waydroid prop set persist.waydroid.width 1920`<br>`waydroid prop set persist.waydroid.height 1080` | Perfect fit for standard 1080p laptop/monitors. |
| **Dynamic Auto-Scaling** | `waydroid prop set persist.waydroid.width 0`<br>`waydroid prop set persist.waydroid.height 0` | Android dynamically resizes to window size. |
| **Single Full Window Mode (Gaming)** | `waydroid prop set persist.waydroid.multi_windows false` | All apps render inside one unified tablet window. |
| **Multi-Window Mode (Desktop Apps)** | `waydroid prop set persist.waydroid.multi_windows true` | Each Android app opens in its own Linux desktop window. |
| **Prevent Freeze / Sleep on Blur** | `waydroid prop set persist.waydroid.suspend false` | Keeps games and background downloads running when window loses focus. |

---

## 📦 3. App Management & Sideloading

| Task | Command | Example |
|:---|:---|:---|
| **Install Local APK** | `waydroid app install <path_to_apk>` | `waydroid app install ~/Downloads/APKPure.apk` |
| **Sideload APK from URL** | `curl -L -o /tmp/app.apk "<url>" && waydroid app install /tmp/app.apk` | Direct CLI download and install. |
| **Launch Installed App** | `waydroid app launch <package_name>` | `waydroid app launch com.apkpure.aegon` |
| **List Installed Apps** | `waydroid app list` | Lists all installed Android application package names. |
| **Grant App Permissions** | `sudo waydroid shell pm grant <package_name> <permission>` | `sudo waydroid shell pm grant com.dts.freefireth android.permission.RECORD_AUDIO` |
| **Uninstall App** | `sudo waydroid shell pm uninstall <package_name>` | `sudo waydroid shell pm uninstall com.example.app` |

---

## 🌐 4. Network & DNS Troubleshooting

| Problem / Task | Fix Command |
|:---|:---|
| **Inject High-Speed Cloudflare DNS** | `waydroid prop set net.dns1 1.1.1.1`<br>`waydroid prop set net.dns2 8.8.8.8` |
| **Fix UFW Firewall Dropping Traffic** | `sudo ufw default allow FORWARD`<br>`sudo ufw allow in on waydroid0`<br>`sudo ufw allow 53`<br>`sudo ufw reload` |
| **Fix Missing NAT Masquerading** | `sudo iptables -P FORWARD ACCEPT`<br>`sudo iptables -t nat -A POSTROUTING -s 192.168.240.0/24 -j MASQUERADE` |
| **Test Internet Connectivity Inside Android** | `sudo lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- ping -c 2 1.1.1.1` |
| **Test DNS Resolution Inside Android** | `sudo lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- ping -c 2 google.com` |

---

## 📂 5. Storage, Files & OBB Paths

| Location | Path on Host Linux | Purpose |
|:---|:---|:---|
| **Android Internal Storage (`/sdcard`)** | `~/.local/share/waydroid/data/media/0/` | Photos, Downloads, documents accessible from host. |
| **Game OBB Directory** | `~/.local/share/waydroid/data/media/0/Android/obb/<package_name>/` | Staging large multi-GB game `.obb` asset packs. |
| **App Private Data** | `~/.local/share/waydroid/data/data/<package_name>/` | App local databases, caches, configuration files. |
| **Host Waydroid Images** | `/var/lib/waydroid/images/` | `system.img` and `vendor.img` root filesystem images. |
| **Host Container Config** | `/var/lib/waydroid/waydroid.cfg` | Core hardware, binder, and suspend configurations. |

---

## 🔍 6. Shell Access, Logs & Diagnostics

| Tool / Target | Command |
|:---|:---|
| **Android Root Shell** | `sudo waydroid shell` |
| **Direct LXC Container Attach** | `sudo lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- /system/bin/sh` |
| **Live Android System Logcat** | `sudo waydroid logcat` (or `sudo waydroid shell logcat -v time`) |
| **Filter Crash Logs (Tombstones & Fatal)** | `sudo waydroid shell logcat -d -t 200 \| grep -iE 'fatal\|crash\|exception'` |
| **Host Waydroid Daemon Execution Logs** | `cat /var/lib/waydroid/waydroid.log` |
| **Check Live IP Lease** | `waydroid status \| grep "IP address"` |
| **1-Click Automated System Repair** | `sudo python3 /home/vikas/waydroid-arch-playbook/scripts/auto_fix_waydroid.py` |

---

## 🚀 7. Helpful Shell Aliases (Add to `~/.bashrc` or `~/.zshrc`)

```bash
# Waydroid Aliases
alias wd-start="sudo systemctl start waydroid-container && waydroid session start & sleep 2 && waydroid show-full-ui &"
alias wd-stop="waydroid session stop && sudo systemctl stop waydroid-container"
alias wd-ui="waydroid show-full-ui &"
alias wd-status="waydroid status"
alias wd-shell="sudo waydroid shell"
alias wd-log="sudo waydroid logcat"
alias wd-fullscreen="waydroid-fullscreen"
alias wd-1080p="waydroid prop set persist.waydroid.width 1920 && waydroid prop set persist.waydroid.height 1080"
```
