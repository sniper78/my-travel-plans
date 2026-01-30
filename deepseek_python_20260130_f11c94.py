#!/usr/bin/env python3
# save as network_scanner.py

import subprocess
import re

def simple_ping_sweep():
    """Basic network scanner for your lab only"""
    network = "192.168.1."  # CHANGE to your lab network
    
    print("[*] Starting lab network scan...")
    
    for host in range(1, 11):  # Only scan first 10 hosts
        ip = network + str(host)
        
        # Ping one packet with timeout
        result = subprocess.call(['ping', '-c', '1', '-W', '1', ip], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
        
        if result == 0:
            print(f"[+] Host {ip} is UP")
        else:
            print(f"[-] Host {ip} is DOWN")

if __name__ == "__main__":
    # IMPORTANT: Only run on your own lab network
    print("=== Lab Network Scanner ===")
    print("WARNING: Only use on networks you own!\n")
    
    confirm = input("Are you in your isolated lab? (yes/no): ")
    if confirm.lower() == 'yes':
        simple_ping_sweep()
    else:
        print("Aborting. Only run in your secure lab environment.")