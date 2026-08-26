# ⚙️ ARM64 Translation Layer (`libndk` / `libhoudini`)

## 1. Why ARM Translation is Required
Most popular Android games and modern apps are compiled exclusively for `arm64-v8a` (ARM64) architecture.
When attempting to install or run ARM64 APKs on an x86_64 CPU without a translation layer, the system encounters:
- `INSTALL_FAILED_NO_MATCHING_ABIS`
- Immediate crash / SIGILL (Illegal Instruction) on launch.

---

## 2. Choosing Between `libndk` vs `libhoudini`
- **`libndk` (Recommended for AMD CPUs & Modern Ryzen):** High stability, developed from Android NDK native bridge.
- **`libhoudini` (Recommended for Intel CPUs):** Intel's binary translation layer with SSE/AVX vector optimizations.

---

## 3. Automated Installation via `waydroid_script`

```bash
# Clone the translation injector
git clone https://github.com/casualsnek/waydroid_script /tmp/waydroid_script
cd /tmp/waydroid_script

# Setup python environment
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Install libndk (for AMD) or libhoudini (for Intel)
sudo ./venv/bin/python3 main.py install libndk
```

---

## 4. Verifying Translation Engine
Inside Waydroid container, check supported architectures:
```bash
waydroid prop get ro.product.cpu.abilist
# Output: x86_64,x86,arm64-v8a,armeabi-v7a,armeabi
```
