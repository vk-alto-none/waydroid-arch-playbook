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

## 📦 6. HOW TO INSTALL APKS ON WAYDROID (Path, CLI & Stores)

### 🚀 Method 1: Install from Linux Local File Path (Fastest CLI)
*Run this in your normal terminal as user `vikas` (NO sudo needed):*
```bash
# Syntax:
waydroid app install <path_to_apk>

# Examples:
waydroid app install /home/vikas/Downloads/my_game.apk
waydroid app install ~/Downloads/WhatsApp.apk
waydroid app install ./game.apk

# 💡 Dolphin File Manager Trick:
# Type "waydroid app install " in terminal (with space), drag & drop the .apk file from Dolphin into terminal, and press Enter!
```

---

### 🌐 Method 2: Direct URL Download & Install in 1-Line
```bash
# Downloads and installs any APK directly from the internet:
curl -L -A "Mozilla/5.0 (Android; Mobile)" -o /tmp/app.apk "<DIRECT_APK_URL>" && waydroid app install /tmp/app.apk
```

---

### 📂 Method 3: Copy to Android Shared Storage (Install via GUI)
```bash
# Copy APK directly into Android's internal Download folder:
cp ~/Downloads/my_app.apk ~/.local/share/waydroid/data/media/0/Download/

# Then inside Waydroid: Open "Files" or "APKPure" app -> Downloads -> Tap on APK to Install.
```

---

### 🏪 Method 4: 1-Click Install via In-App Store (APKPure / F-Droid)
- Open **APKPure** or **F-Droid** on your Waydroid screen.
- Search for any app (e.g. *Free Fire, WhatsApp, Telegram, Via Browser*).
- Click **Install** $\to$ APKPure automatically downloads and extracts APK + OBB data with zero manual effort!

---

### 🎮 Method 5: Large 2GB+ Games with OBB Files (.xapk / .zip)
```bash
# 1. Rename .xapk to .zip and extract:
unzip game.xapk -d /tmp/game_extracted/

# 2. Install base APK:
waydroid app install /tmp/game_extracted/*.apk

# 3. Stage OBB Data files into Waydroid storage:
mkdir -p ~/.local/share/waydroid/data/media/0/Android/obb/<package_name>/
cp /tmp/game_extracted/Android/obb/<package_name>/*.obb ~/.local/share/waydroid/data/media/0/Android/obb/<package_name>/
```

---

### 📋 App Management Commands

| Task | Privilege | Command / Example |
|:---|:---|:---|
| **Launch Installed App** | **User `vikas`** | `waydroid app launch <package_name>` *(e.g. `waydroid app launch com.apkpure.aegon`)* |
| **List All Installed Apps** | **User `vikas`** | `waydroid app list` |
| **Grant App Permissions** | **Superuser (`sudo`)** | `sudo waydroid shell pm grant <pkg> android.permission.RECORD_AUDIO`<br>`sudo waydroid shell pm grant <pkg> android.permission.READ_EXTERNAL_STORAGE` |
| **Force Uninstall App** | **Superuser (`sudo`)** | `sudo waydroid shell pm uninstall <pkg>` |

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
