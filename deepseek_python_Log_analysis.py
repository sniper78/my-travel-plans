#!/usr/bin/env python3
# log_analyzer.py - Analyze your own logs for security events

import re
from collections import Counter

def analyze_auth_log():
    """Analyze /var/log/auth.log for failed attempts"""
    try:
        with open('/var/log/auth.log', 'r') as f:
            logs = f.readlines()
        
        failed_ssh = []
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        
        for line in logs:
            if 'Failed password' in line:
                # Extract IP address
                ips = re.findall(ip_pattern, line)
                if ips:
                    failed_ssh.append(ips[0])
        
        print(f"Total failed SSH attempts: {len(failed_ssh)}")
        if failed_ssh:
            print("Top offending IPs:")
            for ip, count in Counter(failed_ssh).most_common(5):
                print(f"  {ip}: {count} attempts")
    
    except FileNotFoundError:
        print("Auth log not found. Are you running as root?")

analyze_auth_log()