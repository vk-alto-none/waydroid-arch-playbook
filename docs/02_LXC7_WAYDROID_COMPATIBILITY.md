# 🛠️ LXC 7 Compatibility & Code Patches for Waydroid

## 1. The LXC 7 Breaking Change: Relative Destination Paths
In LXC version 7.x, absolute paths in `lxc.mount.entry` destinations are strictly rejected:
```
lxc-start: ERROR: Ignoring mount point "/run/xdg"
lxc_mkdir_p: Read-only file system - Failed to create directory "/usr/lib/lxc/rootfs/run/xdg"
lxc_setup: Failed to setup mount entries
```

### The Root Cause:
Waydroid's `tools/helpers/lxc.py` previously generated mount entries with leading slashes:
```ini
lxc.mount.entry = tmpfs /run/xdg none create=dir 0 0
```
LXC 7 requires:
```ini
lxc.mount.entry = tmpfs run/xdg tmpfs create=dir 0 0
```

---

## 2. The `lxc.hook.post-stop = /dev/null` Bug
In LXC 7, executing `/dev/null` as a hook returns exit status `126 (Permission denied)` because `/dev/null` is not an executable ELF or shell script:
```
lxc-start: run_buffer: 569 Script exited with status 126
lxc-start: Failed to run lxc.hook.post-stop for container "waydroid"
```

### The Fix:
Remove or comment out `lxc.hook.post-stop = /dev/null` in `/usr/lib/waydroid/data/configs/config_3` and `/var/lib/waydroid/lxc/waydroid/config`.

---

## 3. The Double Slashes in Binder Mounts (`/dev//dev/binderfs/...`)
When `tools.config.defaults["binder"]` starts with `/dev/`, naive concatenation `"/dev/" + drv` generates `/dev//dev/binderfs/anbox-binder` which causes `No such file or directory` on mount.

### Python Patch (`/usr/lib/waydroid/tools/helpers/lxc.py`):
```python
def _clean_node(d):
    d = str(d).replace("/dev/", "").lstrip("/")
    return "/dev/" + d

make_entry(_clean_node(args.BINDER_DRIVER), "dev/binder", check=False)
make_entry(_clean_node(args.VNDBINDER_DRIVER), "dev/vndbinder", check=False)
make_entry(_clean_node(args.HWBINDER_DRIVER), "dev/hwbinder", check=False)
```
