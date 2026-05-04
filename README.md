<img width="1408" height="768" alt="Gemini_Generated_Image_hvpx20hvpx20hvpx" src="https://github.com/user-attachments/assets/caaaaf99-e9d8-48e4-b7c0-8eff760eed92" />
<h1 align="center">MITM</h1>
# This tool detects users on the network, identifies the victim, and intercepts data between them and the router. The data is sent to the router by the attacker.
<h1 align="center">Features</h1>
# (Core Features) :

* 1- Stealth Injection (L2 Mode): This tool operates at the second layer of the OSI model (Data Link Layer), allowing it to craft custom data packets that are not easily detected by traditional security systems.

* 2- Unicast Targeting: Instead of flooding the network with broadcast packets, this tool sends packets directly to the victim's and router's MAC address, making the attack completely "silent."

* 3- Silent ARP Spoofing: The ability to trick devices and alter their ARP tables without triggering any warnings in environments like Scapy.

* 4- Automatic MAC Resolution: This tool automatically searches for the MAC addresses of targeted devices as soon as their IP addresses are entered, with a backup search system in case a rapid response fails.

# (Control & UI) :

* 1- Interface Selection: This tool allows you to select the network interface you want to work with (e.g., eth0, wlan0, lo) to ensure packets are sent along the correct path.

* 2- Live Injection Counter: A real-time counter displays the number of packets successfully injected into the network, updating on the same line to keep the screen clean.

* 3-Network Scanner: A built-in network scanner displays all connected devices along with their IP and MAC addresses in a structured table to facilitate target identification.

# (Stability & Safety) :

* 1- Safe ARP Restoration: When the tool is stopped (Ctrl+C), it automatically sends genuine ARP packets to properly reroute traffic, ensuring the victim's internet connection remains uninterrupted after the process is complete.

* 2- Multi-Retry Logic: A built-in system re-attempts data retrieval if the network is slow or unstable to ensure the attack continues uninterrupted.

* 3- Error Handling: An advanced error handling system prevents the tool from crashing if incorrect data is entered or if unexpected connection problems occur.

# kali Liux ✅
# Windows ✅
# Termux ✖️:
<h1 align="center">Operation commands</h1>

```
sudo apt update


```
```
sudo apt install python3 python3-pip -y
```
```
sudo pip3 install scapy
```
```
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```
```
git clone https://github.com/qorsan73/MITM
```
```
cd MITM
```
```
sudo python3 mitm.py
```

# note : 

* This command must be written before running the tool in order for the data to be passed : ``` echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward```

<h1 align="center">How to use</h1>

# Look at the video


https://github.com/user-attachments/assets/0cf430e4-d5fe-41ac-9cd4-80478f634ea9



