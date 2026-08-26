# 📱 Waydroid Complete Operational Cheat Sheet
<!-- Clear privilege separation: [Superuser / root] vs [Regular User] -->

---

## 🟢 1. START WAYDROID (Lifecycle Start)

### 🚀 Method A: 1-Line Complete Start (Recommended)
```bash
# Starts container daemon, initializes user session, and opens Android screen:
sudo systemctl start waydroid-container && waydroid session start & sleep 2 && waydroid show-full-ui &
```

### 🛠️ Method B: Step-by-Step Manual Start
```bash
# Step 1: Start Container Daemon [Superuser / root]
sudo systemctl start waydroid-container.service

# Step 2: Start Wayland User Session [Regular User - NO sudo]
waydroid session start &

# Step 3: Open Android Tablet Screen [Regular User - NO sudo]
waydroid show-full-ui &
```

---

## 🔴 2. STOP WAYDROID (Lifecycle Stop)

### 🛑 Method A: 1-Line Complete Stop (Recommended)
```bash
# Closes UI, kills active session, and shuts down container daemon:
waydroid session stop && sudo systemctl stop waydroid-container.service
```

### 🛠️ Method B: Step-by-Step Manual Stop
```bash
# Step 1: Close Active Android GUI Session [Regular User - NO sudo]
waydroid session stop
# (or use custom helper: waydroid-exit)

# Step 2: Stop Container Daemon in Background [Superuser / root]
sudo systemctl stop waydroid-container.service
```

### 🔄 Method C: Clean Hard Reset / Restart
```bash
# Restart entire container and user session:
sudo systemctl restart waydroid-container.service && sleep 2 && waydroid session start &
```

---

## 📊 3. Status & Diagnostics

| Command | Privilege | Description |
|:---|:---|:---|
| `waydroid status` | **Regular User** | Check container, session, IP lease & Wayland display status. |
| `sudo waydroid shell` | **Superuser (`sudo`)** | Open interactive Android root bash shell. |
| `sudo waydroid logcat` | **Superuser (`sudo`)** | Stream live Android system & app logs. |
| `sudo lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- /system/bin/sh` | **Superuser (`sudo`)** | Direct low-level LXC root shell access. |
| `cat /var/lib/waydroid/waydroid.log` | **Regular User / Read** | Inspect host Waydroid daemon log. |

---

## 🎮 4. Screen, Resolution & Window Management

| Command / Action | Privilege | Description |
|:---|:---|:---|
| `waydroid-fullscreen` | **Regular User** | Toggle Fullscreen on/off instantly via KWin Wayland script. |
| Press `Alt + F3` on window $\to$ *More Actions* $\to$ *Fullscreen* | **KDE GUI** | Native KDE Plasma window management. |
| `waydroid prop set persist.waydroid.width 1920`<br>`waydroid prop set persist.waydroid.height 1080` | **Regular User** | Lock native 1080p display resolution. |
| `waydroid prop set persist.waydroid.width 0`<br>`waydroid prop set persist.waydroid.height 0` | **Regular User** | Enable dynamic window auto-resize. |
| `waydroid prop set persist.waydroid.multi_windows false` | **Regular User** | Single tablet window mode (ideal for games). |
| `waydroid prop set persist.waydroid.multi_windows true` | **Regular User** | Multi-window mode (each app as independent Linux window). |
| `waydroid prop set persist.waydroid.suspend false` | **Regular User** | Anti-Freeze / Anti-Sleep (keeps games running in background). |

---

## 📦 5. App Installation & Management

| Task | Privilege | Command / Example |
|:---|:---|:---|
| **Install Local APK** | **Regular User** | `waydroid app install ~/Downloads/APKPure.apk` |
| **Download & Install from URL** | **Regular User** | `curl -L -o /tmp/app.apk "<url>" && waydroid app install /tmp/app.apk` |
| **Launch Installed App** | **Regular User** | `waydroid app launch com.apkpure.aegon` |
| **List Installed Apps** | **Regular User** | `waydroid app list` |
| **Grant App Permissions** | **Superuser (`sudo`)** | `sudo waydroid shell pm grant <pkg> <permission>` |
| **Uninstall App** | **Superuser (`sudo`)** | `sudo waydroid shell pm uninstall <pkg>` |

---

## 🌐 6. Network & DNS Troubleshooting

```bash
# 1. Set High-Speed Cloudflare DNS [Regular User]
waydroid prop set net.dns1 1.1.1.1
waydroid prop set net.dns2 8.8.8.8

# 2. Fix UFW Firewall Blocking Traffic [Superuser / root]
sudo ufw default allow FORWARD
sudo ufw allow in on waydroid0
sudo ufw allow 53
sudo ufw reload

# 3. Enable NAT Masquerading [Superuser / root]
sudo iptables -P FORWARD ACCEPT
sudo iptables -t nat -A POSTROUTING -s 192.168.240.0/24 -j MASQUERADE

# 4. Verify Internet Connectivity inside Container [Superuser / root]
sudo lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- ping -c 2 1.1.1.1
sudo lxc-attach -P /var/lib/waydroid/lxc -n waydroid -- ping -c 2 google.com
```

---

## 📂 7. Storage, Files & OBB Paths

| Location | Path on Host Linux | Purpose |
|:---|:---|:---|
| **Android Internal Storage (`/sdcard`)** | `~/.local/share/waydroid/data/media/0/` | Photos, Downloads, documents accessible from host. |
| **Game OBB Directory** | `~/.local/share/waydroid/data/media/0/Android/obb/<package_name>/` | Staging large multi-GB game `.obb` asset packs. |
| **App Private Data** | `~/.local/share/waydroid/data/data/<package_name>/` | App databases, cache, and local files. |
| **Host Waydroid Images** | `/var/lib/waydroid/images/` | `system.img` and `vendor.img` images. |
| **Host Container Config** | `/var/lib/waydroid/waydroid.cfg` | Hardware, binder, and suspend configurations. |

---

## 🚀 8. Recommended Shell Aliases (Add to `~/.bashrc`)

```bash
# --- Waydroid Operational Aliases ---
alias wd-start="sudo systemctl start waydroid-container && waydroid session start & sleep 2 && waydroid show-full-ui &"
alias wd-stop="waydroid session stop && sudo systemctl stop waydroid-container"
alias wd-restart="sudo systemctl restart waydroid-container.service && sleep 2 && waydroid session start &"
alias wd-ui="waydroid show-full-ui &"
alias wd-status="waydroid status"
alias wd-shell="sudo waydroid shell"
alias wd-log="sudo waydroid logcat"
alias wd-fullscreen="waydroid-fullscreen"
alias wd-1080p="waydroid prop set persist.waydroid.width 1920 && waydroid prop set persist.waydroid.height 1080"
```
