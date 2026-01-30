#!/usr/bin/env python3
"""
scheduled_scanner.py
Run daily automated security checks
Add to cron: 0 2 * * * /usr/bin/python3 /path/to/scheduled_scanner.py
"""

import schedule
import time
import subprocess
import os
from datetime import datetime

def daily_vulnerability_scan():
    """Daily scheduled scan"""
    print(f"[{datetime.now()}] Starting daily scan...")
    
    # Define your lab network
    lab_network = "192.168.1.0/24"  # CHANGE THIS
    
    # Run specific scans
    scans = [
        f"nmap -sP {lab_network} -oN daily_ping_scan.txt",
        "log_analyzer.py /var/log/auth.log --schedule",
        "python3 auto_log_analyzer.py /var/log/syslog"
    ]
    
    for scan in scans:
        try:
            subprocess.run(scan, shell=True, timeout=300)
            print(f"  Completed: {scan}")
        except Exception as e:
            print(f"  Failed: {scan} - Error: {e}")
    
    print(f"[{datetime.now()}] Daily scan completed\n")

def weekly_full_audit():
    """Weekly comprehensive audit"""
    print(f"[{datetime.now()}] Starting weekly audit...")
    # Add comprehensive checks here
    print(f"[{datetime.now()}] Weekly audit completed\n")

def main():
    """Schedule tasks to run automatically"""
    print("🕐 Security Automation Scheduler Started")
    print("Press Ctrl+C to stop\n")
    
    # Schedule daily scan at 2 AM
    schedule.every().day.at("02:00").do(daily_vulnerability_scan)
    
    # Schedule weekly audit on Sunday at 3 AM
    schedule.every().sunday.at("03:00").do(weekly_full_audit)
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Scheduler stopped by user")