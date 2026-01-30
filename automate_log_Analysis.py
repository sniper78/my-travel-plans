#!/usr/bin/env python3
"""
auto_log_analyzer.py
Automates daily log analysis for security monitoring
Run as: python3 auto_log_analyzer.py /var/log/auth.log
"""

import os
import sys
import re
import json
from datetime import datetime, timedelta
from collections import Counter
import argparse

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.results = {
            'failed_attempts': [],
            'successful_logins': [],
            'suspicious_ips': [],
            'summary': {}
        }
    
    def analyze(self):
        """Main analysis function"""
        if not os.path.exists(self.log_file):
            print(f"Error: {self.log_file} not found!")
            return
        
        print(f"[*] Analyzing {self.log_file}...")
        
        patterns = {
            'failed_ssh': r'Failed password for .* from (\d+\.\d+\.\d+\.\d+)',
            'success_ssh': r'Accepted password for .* from (\d+\.\d+\.\d+\.\d+)',
            'invalid_user': r'Invalid user (\w+) from (\d+\.\d+\.\d+\.\d+)'
        }
        
        with open(self.log_file, 'r') as f:
            for line in f:
                # Check for failed SSH attempts
                failed_match = re.search(patterns['failed_ssh'], line)
                if failed_match:
                    ip = failed_match.group(1)
                    self.results['failed_attempts'].append(ip)
                
                # Check for successful logins
                success_match = re.search(patterns['success_ssh'], line)
                if success_match:
                    ip = success_match.group(1)
                    self.results['successful_logins'].append(ip)
        
        self._generate_summary()
        self._save_report()
        self._send_alert_if_needed()
    
    def _generate_summary(self):
        """Generate summary statistics"""
        total_failed = len(self.results['failed_attempts'])
        total_success = len(self.results['successful_logins'])
        
        # Find top offending IPs
        top_offenders = Counter(self.results['failed_attempts']).most_common(5)
        
        self.results['summary'] = {
            'total_failed_attempts': total_failed,
            'total_successful_logins': total_success,
            'top_offending_ips': dict(top_offenders),
            'analysis_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'log_file': self.log_file
        }
    
    def _save_report(self):
        """Save analysis to JSON report"""
        report_file = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=4)
        
        print(f"[+] Report saved to {report_file}")
    
    def _send_alert_if_needed(self):
        """Send alert if suspicious activity detected"""
        threshold = 10  # Alert if more than 10 failed attempts
        
        if self.results['summary']['total_failed_attempts'] > threshold:
            print("[!] ALERT: High number of failed login attempts detected!")
            print(f"    Total failed: {self.results['summary']['total_failed_attempts']}")
            
            # Here you could add email/SMS notification
            # self._send_email_alert()

def main():
    parser = argparse.ArgumentParser(description='Automated Log Analyzer')
    parser.add_argument('logfile', help='Path to log file')
    parser.add_argument('--schedule', action='store_true', 
                       help='Run as scheduled task')
    
    args = parser.parse_args()
    
    analyzer = LogAnalyzer(args.logfile)
    analyzer.analyze()
    
    # Print summary to console
    print("\n" + "="*50)
    print("SECURITY SUMMARY")
    print("="*50)
    for key, value in analyzer.results['summary'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    main()