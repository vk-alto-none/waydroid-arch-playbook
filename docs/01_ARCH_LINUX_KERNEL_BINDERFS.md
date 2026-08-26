# 📖 Kernel & BinderFS Setup on Arch Linux

## 1. Why Arch Linux is Different
On modern Arch Linux (Kernel 6.x LTS), binder is implemented as `binderfs`.
Unlike standard Ubuntu or Android kernels where `/dev/binder` is created automatically, Arch Linux binderfs mounts at `/dev/binderfs/` with device nodes:
- `/dev/binderfs/anbox-binder`
- `/dev/binderfs/anbox-vndbinder`
- `/dev/binderfs/anbox-hwbinder`
- `/dev/binderfs/binder-control`

---

## 2. The Permission Bug (`Permission Denied` in `gbinder`)
By default, `/dev/binderfs` is mounted with `mode=0700` owned by `root`.
When user runs `waydroid session start`, `gbinder` tries to open `/dev/binderfs/anbox-binder` and gets:
```
[gbinder] ERROR: Can't open /dev/anbox-binder: Permission denied
```

### The Fix:
1. Create udev rule: `/etc/udev/rules.d/99-waydroid-binder.rules`
```udev
SUBSYSTEM=="binder", MODE="0666"
KERNEL=="binder-control", MODE="0666"
KERNEL=="anbox-binder", MODE="0666"
KERNEL=="anbox-hwbinder", MODE="0666"
KERNEL=="anbox-vndbinder", MODE="0666"
KERNEL=="binder", MODE="0666"
KERNEL=="hwbinder", MODE="0666"
KERNEL=="vndbinder", MODE="0666"
```

2. Create systemd tmpfiles rule: `/etc/tmpfiles.d/waydroid-binder.conf`
```conf
d /dev/binderfs 0777 root root -
z /dev/binderfs/* 0666 root root -
```

3. Ensure symlinks exist:
```bash
sudo ln -sf /dev/binderfs/anbox-binder /dev/anbox-binder
sudo ln -sf /dev/binderfs/anbox-vndbinder /dev/anbox-vndbinder
sudo ln -sf /dev/binderfs/anbox-hwbinder /dev/anbox-hwbinder
sudo chmod 755 /dev/binderfs
sudo chmod 666 /dev/binderfs/*
```
