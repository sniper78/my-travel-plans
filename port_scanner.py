#!/usr/bin/env python3
# basic_port_scanner.py - EDUCATIONAL USE ONLY

import socket
import time

def scan_ports(target, ports):
    """Simple port scanner for your lab machines only"""
    print(f"Scanning {target}...")
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        
        result = sock.connect_ex((target, port))
        
        if result == 0:
            print(f"Port {port}: OPEN")
        sock.close()
        
        # Be nice - add delay
        time.sleep(0.1)

# ONLY scan your own lab machines!
if __name__ == "__main__":
    # Example: Scanning localhost in your lab
    TARGET = "127.0.0.1"  # Change to your lab machine
    PORTS = [21, 22, 80, 443, 8080]  # Common ports
    
    print("=== Educational Port Scanner ===")
    print(f"Target: {TARGET}")
    print(f"Ports: {PORTS}")
    print("\nStarting scan...\n")
    
    scan_ports(TARGET, PORTS)