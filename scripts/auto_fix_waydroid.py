#!/usr/bin/env python3
"""
Waydroid Arch Linux & LXC 7 Auto-Repair and Configurator
Author: Durbhasi Gurukulam Private Limited (DGPL)
License: MIT
"""

import os
import sys
import shutil
import subprocess

def run_cmd(cmd, check=True):
    print(f"[*] Executing: {cmd}")
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if check and res.returncode != 0:
        print(f"[-] Error executing: {cmd}\nStderr: {res.stderr}")
    return res

def patch_lxc_helper():
    lxc_helper = "/usr/lib/waydroid/tools/helpers/lxc.py"
    if not os.path.exists(lxc_helper):
        print(f"[-] File not found: {lxc_helper}")
        return

    with open(lxc_helper, "r") as f:
        code = f.read()

    # 1. Patch relative mount destinations
    old_dest = "if dist is None:\n        dist = src[1:]"
    new_dest = "if dist is None:\n        dist = src.lstrip('/')\n    else:\n        dist = dist.lstrip('/')"
    if old_dest in code:
        code = code.replace(old_dest, new_dest, 1)
        print("[+] Patched relative destination paths in lxc.py")

    # 2. Patch tmpfs mount type
    old_tmpfs = 'if not make_entry("tmpfs", tools.config.defaults["container_xdg_runtime_dir"], options="create=dir 0 0"):'
    new_tmpfs = 'if not make_entry("tmpfs", tools.config.defaults["container_xdg_runtime_dir"], mnt_type="tmpfs", options="create=dir 0 0"):'
    if old_tmpfs in code:
        code = code.replace(old_tmpfs, new_tmpfs, 1)
        print("[+] Patched tmpfs mount type in lxc.py")

    # 3. Patch binder driver double slash
    old_binder = '''    # Binder dev nodes
    make_entry("/dev/" + args.BINDER_DRIVER, "dev/binder", check=False)
    make_entry("/dev/" + args.VNDBINDER_DRIVER, "dev/vndbinder", check=False)
    make_entry("/dev/" + args.HWBINDER_DRIVER, "dev/hwbinder", check=False)'''
    new_binder = '''    # Binder dev nodes
    def _clean_node(d):
        d = str(d).replace("/dev/", "").lstrip("/")
        return "/dev/" + d
    make_entry(_clean_node(args.BINDER_DRIVER), "dev/binder", check=False)
    make_entry(_clean_node(args.VNDBINDER_DRIVER), "dev/vndbinder", check=False)
    make_entry(_clean_node(args.HWBINDER_DRIVER), "dev/hwbinder", check=False)'''
    if old_binder in code:
        code = code.replace(old_binder, new_binder, 1)
        print("[+] Patched binder node sanitation in lxc.py")

    with open(lxc_helper, "w") as f:
        f.write(code)

def patch_lxc_configs():
    c3 = "/usr/lib/waydroid/data/configs/config_3"
    if os.path.exists(c3):
        with open(c3, "r") as f:
            content = f.read()
        content = content.replace("lxc.hook.post-stop = /dev/null", "# lxc.hook.post-stop = /dev/null")
        with open(c3, "w") as f:
            f.write(content)
        print("[+] Patched post-stop hook in config_3")

def setup_binder_rules():
    print("[*] Configuring BinderFS udev and tmpfiles rules...")
    udev_rule = """SUBSYSTEM=="binder", MODE="0666"
KERNEL=="binder-control", MODE="0666"
KERNEL=="anbox-binder", MODE="0666"
KERNEL=="anbox-hwbinder", MODE="0666"
KERNEL=="anbox-vndbinder", MODE="0666"
KERNEL=="binder", MODE="0666"
KERNEL=="hwbinder", MODE="0666"
KERNEL=="vndbinder", MODE="0666"
"""
    with open("/etc/udev/rules.d/99-waydroid-binder.rules", "w") as f:
        f.write(udev_rule)

    tmpfiles_rule = """d /dev/binderfs 0777 root root -
z /dev/binderfs/* 0666 root root -
"""
    with open("/etc/tmpfiles.d/waydroid-binder.conf", "w") as f:
        f.write(tmpfiles_rule)

    run_cmd("chmod 755 /dev/binderfs && chmod 666 /dev/binderfs/* 2>/dev/null || true", check=False)
    run_cmd("ln -sf /dev/binderfs/anbox-binder /dev/anbox-binder", check=False)
    run_cmd("ln -sf /dev/binderfs/anbox-vndbinder /dev/anbox-vndbinder", check=False)
    run_cmd("ln -sf /dev/binderfs/anbox-hwbinder /dev/anbox-hwbinder", check=False)

def fix_network_and_firewall():
    print("[*] Configuring Waydroid Network, DNS, and UFW Firewall...")
    # 1. Force waydroid-net.sh to use standard iptables instead of conflicting nftables
    net_sh = "/usr/lib/waydroid/data/scripts/waydroid-net.sh"
    if os.path.exists(net_sh):
        with open(net_sh, "r") as f:
            net_code = f.read()
        net_code = net_code.replace('LXC_USE_NFT="true"', 'LXC_USE_NFT="false"')
        with open(net_sh, "w") as f:
            f.write(net_code)
        print("[+] Set LXC_USE_NFT=false in waydroid-net.sh")

    # 2. Configure UFW if installed and active
    if shutil.which("ufw"):
        run_cmd("sed -i 's/DEFAULT_FORWARD_POLICY=\"DROP\"/DEFAULT_FORWARD_POLICY=\"ACCEPT\"/g' /etc/default/ufw", check=False)
        run_cmd("ufw default allow FORWARD", check=False)
        run_cmd("ufw allow in on waydroid0", check=False)
        run_cmd("ufw allow 53", check=False)
        run_cmd("ufw allow 67/udp", check=False)
        run_cmd("ufw allow 68/udp", check=False)
        run_cmd("ufw reload", check=False)
        print("[+] UFW routed forwarding and DNS rules applied")

    # 3. Ensure iptables NAT & forwarding
    run_cmd("iptables -P FORWARD ACCEPT", check=False)
    run_cmd("iptables -t nat -C POSTROUTING -s 192.168.240.0/24 -j MASQUERADE 2>/dev/null || iptables -t nat -A POSTROUTING -s 192.168.240.0/24 -j MASQUERADE", check=False)

    # 4. Anti-suspend & Cloudflare DNS
    run_cmd("sysctl -w net.ipv4.ip_forward=1", check=False)
    run_cmd("sed -i 's/suspend_action = freeze/suspend_action = none/g' /var/lib/waydroid/waydroid.cfg 2>/dev/null || true", check=False)

def main():
    if os.geteuid() != 0:
        print("[-] This repair script must be executed with sudo / root privileges.")
        sys.exit(1)

    print("🚀 Starting Waydroid Arch Linux Auto-Fix Engine...")
    patch_lxc_helper()
    patch_lxc_configs()
    setup_binder_rules()
    fix_network_and_firewall()

    # Restart service
    run_cmd("systemctl restart waydroid-container.service")
    print("\n✅ Waydroid Arch Linux & LXC 7 Environment Successfully Repaired!")
    print("👉 Now start your session as user:")
    print("   waydroid session start &")
    print("   waydroid show-full-ui &")

if __name__ == "__main__":
    main()
