# 📱 Waydroid Complete Operational Cheat Sheet
<!-- Separated by User Role: [SUPERUSER / ROOT] vs [REGULAR USER: vikas] -->

---

## 🟢 1. HOW TO START WAYDROID

### 👑 Terminal 1: As Superuser / Root (`root` / `su`)
*Run this in your Superuser terminal (or via root):*
```bash
# 1. Start the container background service
systemctl start waydroid-container.service

# (Optional: Check that container daemon is active)
systemctl status waydroid-container.service
```

### 👤 Terminal 2: As Regular User (`vikas` — NO sudo)
*Run this in your normal desktop terminal (with Wayland display):*
```bash
# 1. Start the Wayland user session in background
waydroid session start &

# 2. Wait 2 seconds, then open the Android Tablet GUI
waydroid show-full-ui &
```

---

## 🔴 2. HOW TO STOP WAYDROID

### 👤 Terminal 2: As Regular User (`vikas` — NO sudo)
*First close the graphical session:*
```bash
# 1. Stop active Android session and close windows
waydroid session stop
# (or run: waydroid-exit)
```

### 👑 Terminal 1: As Superuser / Root (`root` / `su`)
*Then shutdown the background daemon:*
```bash
# 2. Stop the container background service
systemctl stop waydroid-container.service
```

---

## 🧭 3. ANDROID NAVIGATION & KEYBOARD SHORTCUTS

| Action / Button | Keyboard Shortcut | Mouse Gesture | Description |
|:---|:---|:---|:---|
| **🏠 Go to Home Screen** | **`Windows Key` (Super / Meta)** or **`F1`** | Swipe UP from bottom edge | Instant return to Android home / launcher. |
| **🔙 Go Back (Previous Screen)** | **`Esc` (Escape)** | **Right-Click** anywhere | Goes back one step or closes active menu. |
| **📑 Recent Apps / Multitasking** | **`F2`** or **`Super + Tab`** | Swipe UP and hold | Shows all open background apps. |
| **🔔 Pull Down Notification Bar** | **`F4`** | Drag DOWN from top edge | Shows notification shade & quick toggles. |
| **💡 Wake up Screen (If Black/Blank)** | Press **`Space`** / Click Mouse | Left Click anywhere | Wakes Android from display timeout. |

### 🛑 Prevent Android Screen from Going Blank / Sleeping:
```bash
# Run this once in terminal (fixes screen turning black after inactivity):
sudo waydroid shell settings put system screen_off_timeout 2147483647
sudo waydroid shell settings put global stay_on_while_plugged_in 3
```

---

## 📊 4. Status & Diagnostics

### 👤 User `vikas` (Regular User):
```bash
# Check live status (Container state, Session, IP address, Display)
waydroid status

# Inspect host daemon log file
cat /var/lib/waydroid/waydroid.log
```

### 👑 Superuser / Root (`root` / `su`):
```bash
# Open interactive Android root bash shell
waydroid shell

# Stream live Android system & app logs
waydroid logcat

# Direct LXC container root shell
lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- /system/bin/sh

# Filter fatal crash logs / tombstones
lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- logcat -d -t 200 | grep -iE 'fatal|crash|exception'
```

---

## 🎮 5. Screen, Resolution & Gaming (User: `vikas`)

*All display properties must be set as regular user `vikas`:*

```bash
# Toggle Fullscreen On / Off (KWin Wayland)
waydroid-fullscreen
# (or press Alt + F3 on the window -> More Actions -> Fullscreen)

# Lock 1080p Resolution (1920x1080)
waydroid prop set persist.waydroid.width 1920
waydroid prop set persist.waydroid.height 1080

# Dynamic Auto-Resize (Matches window size)
waydroid prop set persist.waydroid.width 0
waydroid prop set persist.waydroid.height 0

# Single Tablet Mode (Best for games)
waydroid prop set persist.waydroid.multi_windows false

# Multi-Window Mode (Each app opens in separate Linux window)
waydroid prop set persist.waydroid.multi_windows true

# Anti-Freeze / Anti-Sleep (Keeps games running when window loses focus)
waydroid prop set persist.waydroid.suspend false
```

---

## 📦 6. App Installation & Management

### 👤 User `vikas` (Regular User):
```bash
# Install local APK file
waydroid app install ~/Downloads/app.apk

# Download & Sideload APK directly
curl -L -o /tmp/app.apk "<url>" && waydroid app install /tmp/app.apk

# Launch installed app by package name
waydroid app launch <package_name>
# Example: waydroid app launch com.apkpure.aegon

# List all installed apps
waydroid app list
```

### 👑 Superuser / Root (`root` / `su`):
```bash
# Grant app runtime permissions (Storage, Audio, etc.)
waydroid shell pm grant <package_name> android.permission.RECORD_AUDIO
waydroid shell pm grant <package_name> android.permission.READ_EXTERNAL_STORAGE

# Force uninstall an app
waydroid shell pm uninstall <package_name>
```

---

## 🌐 7. Network, Firewall & DNS Configuration

### 👤 User `vikas` (Set DNS Properties):
```bash
waydroid prop set net.dns1 1.1.1.1
waydroid prop set net.dns2 8.8.8.8
```

### 👑 Superuser / Root (UFW & IPTABLES NAT Routing):
```bash
# Allow UFW routed forwarding and DNS
ufw default allow FORWARD
ufw allow in on waydroid0
ufw allow 53
ufw reload

# Enable NAT masquerade
iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -s 192.168.240.0/24 -j MASQUERADE

# Test connectivity from inside Android container
lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- ping -c 2 1.1.1.1
lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- ping -c 2 google.com
```

---

## 📂 8. Storage, Files & OBB Paths

| Location | Path on Host Linux | Accessible By | Purpose |
|:---|:---|:---|:---|
| **Android Storage (`/sdcard`)** | `~/.local/share/waydroid/data/media/0/` | `vikas` (User) | Photos, Downloads, documents |
| **Game OBB Directory** | `~/.local/share/waydroid/data/media/0/Android/obb/<pkg>/` | `vikas` (User) | 2GB+ Game `.obb` assets |
| **App Private Data** | `~/.local/share/waydroid/data/data/<pkg>/` | `vikas` / `root` | App data, database, cache |
| **Host System Images** | `/var/lib/waydroid/images/` | `root` only | `system.img` & `vendor.img` |
| **Container Config** | `/var/lib/waydroid/waydroid.cfg` | `root` only | Core hardware & binder configs |

---

## 🛠️ 9. 1-Click Auto Repair Script (Superuser / Root)

*Run this if Waydroid container fails to start or binder is broken:*
```bash
# As Superuser / Root:
python3 /home/vikas/waydroid-arch-playbook/scripts/auto_fix_waydroid.py
```
