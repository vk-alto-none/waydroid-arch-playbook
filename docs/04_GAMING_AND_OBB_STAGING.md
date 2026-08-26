# 🎮 Gaming, App Stores & OBB Staging on Waydroid

## 1. Preventing Sleep & Freeze During Gaming
By default, Waydroid enters a frozen state (`lxc-freeze`) when the Android window loses focus.
To ensure games keep running without stutter or disconnection:

```bash
# Set in /var/lib/waydroid/waydroid.cfg:
# suspend_action = none

# Set via runtime properties:
waydroid prop set persist.waydroid.suspend false
```

---

## 2. Window Modes (Single Tablet Window vs Multi-Window)
- **Single Full Android Window (Recommended for Games):**
```bash
waydroid prop set persist.waydroid.multi_windows false
waydroid prop set persist.waydroid.width 1280
waydroid prop set persist.waydroid.height 720
waydroid show-full-ui &
```
- **Multi-Window Mode (Each Android app opens as a separate Linux window):**
```bash
waydroid prop set persist.waydroid.multi_windows true
```

---

## 3. Sideloading App Stores
Installing a reliable store eliminates manual XAPK splitting:

```bash
# 1. Download APKPure
curl -L -A "Mozilla/5.0 (Android; Mobile)" -o /tmp/APKPure.apk "https://d.apkpure.net/b/APK/com.apkpure.aegon?version=latest"

# 2. Download F-Droid
curl -L -o /tmp/FDroid.apk "https://f-droid.org/F-Droid.apk"

# 3. Install into running Waydroid
waydroid app install /tmp/APKPure.apk
waydroid app install /tmp/FDroid.apk
```

---

## 4. Manual OBB Data Placement (For 2GB+ Heavy Games)
If you download `.xapk` or `.zip` manually:
1. Extract the base `.apk` and `main.<version>.<package_name>.obb`.
2. Install base APK: `waydroid app install game.apk`
3. Copy OBB directory to:
```bash
mkdir -p ~/.local/share/waydroid/data/media/0/Android/obb/<package_name>/
cp main.*.obb ~/.local/share/waydroid/data/media/0/Android/obb/<package_name>/
```

---

## 5. Fullscreen & Quick Exit Controls (KDE Plasma & Wayland)

### 🖥️ Full Screen Toggle:
Because Wayland surfaces may not respond to generic `F11` keys, use the KWin D-Bus helper script:
```bash
# Toggle fullscreen mode instantly
waydroid-fullscreen

# Or via KDE Plasma Window menu:
# Press Alt + F3 on the window -> More Actions -> Fullscreen
```

### 🚪 Clean Exit & Shutdown:
```bash
# 1. Close active session:
waydroid-exit
# (or press Alt + F4 on the Waydroid window)

# 2. Stop container background service:
sudo systemctl stop waydroid-container.service
```

---

## 6. Game Compatibility & Anti-Cheat Deep Dive (CODM vs Other Titles)

### ⚠️ Call of Duty: Mobile (CODM) Hardcoded Kill Switch
- **Symptom:** Game launches, displays Activision/MSDK splash, and immediately exits.
- **Logcat Proof:**
  ```log
  I MessageHub: GetEmulatorResolutionHeight...
  I CODMainActivity: exit Game Call
  I Process : Sending signal. PID: 3536 SIG: 9
  ```
- **Technical Post-Mortem:** Activision / Tencent Anti-Cheat (`com.tencent.tmgp.cod.CODMainActivity` & `GP7Service`) checks for official Windows GameLoop environment markers. On Linux/Waydroid/QEMU, it intentionally issues a self-terminating `SIGKILL (Signal 9)` kill switch.

### 🎮 Verified Compatible Titles on Waydroid:
- **Free Fire (`com.dts.freefireth`):** Fully operational with ARM translation.
- **PUBG Mobile / BGMI:** Compatible with device fingerprinting / Magisk.
- **Brawl Stars / Clash of Clans:** Fully functional.
- **Asphalt 9: Legends:** Smooth GPU accelerated rendering.
- **Roblox & Minecraft Android:** 100% native Wayland compatibility.
