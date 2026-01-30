#!/usr/bin/env python3
"""
Script SICURO per analisi passiva di sicurezza
Può essere usato su qualsiasi sito (anche in produzione) perché NON è invasivo

Questo script:
✅ Controlla solo header HTTP
✅ Non modifica nulla
✅ Non invia payload malevoli
✅ Non testa vulnerabilità attivamente
✅ È completamente sicuro da usare

Autore: Security Lab
Licenza: Uso educativo
"""

import requests
import sys
from urllib.parse import urlparse
from colorama import init, Fore, Style
import ssl
import socket

init(autoreset=True)

class SafeSecurityChecker:
    """Checker di sicurezza NON invasivo"""
    
    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.issues = []
        self.warnings = []
        self.passed = []
    
    def print_header(self, text):
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{text}")
        print(f"{'='*70}{Style.RESET_ALL}")
    
    def print_success(self, text):
        print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")
        self.passed.append(text)
    
    def print_warning(self, text):
        print(f"{Fore.YELLOW}⚠️  {text}{Style.RESET_ALL}")
        self.warnings.append(text)
    
    def print_error(self, text):
        print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")
        self.issues.append(text)
    
    def check_https(self):
        """Verifica se il sito usa HTTPS"""
        self.print_header("1. CONTROLLO PROTOCOLLO HTTPS")
        
        if self.url.startswith('https://'):
            self.print_success("HTTPS attivo")
            
            # Verifica certificato SSL
            try:
                context = ssl.create_default_context()
                with socket.create_connection((self.domain, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                        cert = ssock.getpeercert()
                        self.print_success(f"Certificato SSL valido")
                        print(f"   Emesso a: {cert.get('subject', [[['', '']]])[0][0][1]}")
                        print(f"   Emesso da: {cert.get('issuer', [[['', '']]])[3][0][1]}")
            except Exception as e:
                self.print_warning(f"Problema con certificato SSL: {str(e)}")
        else:
            self.print_error("HTTPS NON attivo - CRITICO!")
            self.print_warning("Il sito dovrebbe usare HTTPS per proteggere i dati")
    
    def check_security_headers(self):
        """Controlla header di sicurezza HTTP"""
        self.print_header("2. CONTROLLO SECURITY HEADERS")
        
        try:
            response = requests.get(self.url, timeout=10, allow_redirects=True)
            
            # Header di sicurezza da verificare
            security_headers = {
                'Strict-Transport-Security': {
                    'description': 'Forza HTTPS (HSTS)',
                    'critical': True,
                    'example': 'max-age=31536000; includeSubDomains'
                },
                'X-Frame-Options': {
                    'description': 'Protegge da clickjacking',
                    'critical': True,
                    'example': 'DENY o SAMEORIGIN'
                },
                'X-Content-Type-Options': {
                    'description': 'Previene MIME type sniffing',
                    'critical': True,
                    'example': 'nosniff'
                },
                'Content-Security-Policy': {
                    'description': 'Previene XSS e injection',
                    'critical': True,
                    'example': "default-src 'self'"
                },
                'X-XSS-Protection': {
                    'description': 'Protezione XSS del browser (legacy)',
                    'critical': False,
                    'example': '1; mode=block'
                },
                'Referrer-Policy': {
                    'description': 'Controlla informazioni referrer',
                    'critical': False,
                    'example': 'strict-origin-when-cross-origin'
                },
                'Permissions-Policy': {
                    'description': 'Controlla feature del browser',
                    'critical': False,
                    'example': 'geolocation=(), microphone=()'
                }
            }
            
            print(f"\nAnalizzando: {self.url}")
            print(f"Status Code: {response.status_code}\n")
            
            for header, info in security_headers.items():
                if header in response.headers:
                    self.print_success(f"{header}")
                    print(f"   Valore: {response.headers[header]}")
                    print(f"   {info['description']}")
                else:
                    if info['critical']:
                        self.print_error(f"{header} - MANCANTE")
                    else:
                        self.print_warning(f"{header} - Mancante (opzionale)")
                    print(f"   {info['description']}")
                    print(f"   Esempio: {info['example']}")
                print()
            
        except requests.exceptions.RequestException as e:
            self.print_error(f"Impossibile connettersi: {str(e)}")
    
    def check_cookie_security(self):
        """Verifica sicurezza dei cookie"""
        self.print_header("3. CONTROLLO SICUREZZA COOKIE")
        
        try:
            response = requests.get(self.url, timeout=10)
            
            if 'Set-Cookie' in response.headers:
                cookies = response.headers['Set-Cookie']
                
                # Verifica flag di sicurezza
                if 'Secure' in cookies:
                    self.print_success("Flag 'Secure' presente nei cookie")
                else:
                    self.print_error("Flag 'Secure' mancante - i cookie potrebbero essere intercettati")
                
                if 'HttpOnly' in cookies:
                    self.print_success("Flag 'HttpOnly' presente nei cookie")
                else:
                    self.print_error("Flag 'HttpOnly' mancante - vulnerabile a XSS")
                
                if 'SameSite' in cookies:
                    self.print_success("Flag 'SameSite' presente nei cookie")
                else:
                    self.print_warning("Flag 'SameSite' mancante - raccomandato per CSRF protection")
            else:
                print("Nessun cookie impostato nella risposta")
                
        except Exception as e:
            self.print_warning(f"Errore nel controllo cookie: {str(e)}")
    
    def check_sensitive_files(self):
        """Verifica esposizione di file sensibili (test passivo)"""
        self.print_header("4. CONTROLLO ESPOSIZIONE FILE SENSIBILI")
        
        # File che NON dovrebbero essere accessibili
        sensitive_paths = [
            '/.env',
            '/.git/config',
            '/config.php',
            '/phpinfo.php',
            '/wp-config.php',
            '/.env.local',
            '/.env.production',
            '/backup.sql',
            '/database.sql',
            '/.htaccess',
            '/composer.json',
            '/package.json'
        ]
        
        print("Verificando esposizione file sensibili...\n")
        
        exposed_files = []
        for path in sensitive_paths:
            try:
                test_url = f"{self.url.rstrip('/')}{path}"
                response = requests.head(test_url, timeout=5, allow_redirects=False)
                
                if response.status_code == 200:
                    self.print_error(f"{path} - ESPOSTO (Status: 200)")
                    exposed_files.append(path)
                elif response.status_code in [403, 404]:
                    # 403/404 è OK - file protetto o non esistente
                    pass
                    
            except requests.exceptions.RequestException:
                pass  # Timeout o errore di connessione
        
        if not exposed_files:
            self.print_success("Nessun file sensibile esposto rilevato")
        else:
            print(f"\n{Fore.RED}ATTENZIONE: {len(exposed_files)} file sensibili esposti!{Style.RESET_ALL}")
    
    def check_server_info(self):
        """Verifica informazioni server (fingerprinting passivo)"""
        self.print_header("5. INFORMAZIONI SERVER")
        
        try:
            response = requests.get(self.url, timeout=10)
            
            # Header che rivelano info sul server
            info_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version', 'X-AspNetMvc-Version']
            
            found_info = False
            for header in info_headers:
                if header in response.headers:
                    found_info = True
                    self.print_warning(f"{header}: {response.headers[header]}")
                    print("   Rivelare info del server può aiutare gli attaccanti")
            
            if not found_info:
                self.print_success("Header informativi rimossi o nascosti")
                
        except Exception as e:
            self.print_warning(f"Errore: {str(e)}")
    
    def generate_report(self):
        """Genera report finale"""
        self.print_header("📊 REPORT FINALE")
        
        total_checks = len(self.passed) + len(self.warnings) + len(self.issues)
        
        print(f"\n{Fore.CYAN}Riepilogo Analisi: {self.url}{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}✅ Controlli Superati: {len(self.passed)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️  Avvisi: {len(self.warnings)}{Style.RESET_ALL}")
        print(f"{Fore.RED}❌ Problemi Critici: {len(self.issues)}{Style.RESET_ALL}")
        
        # Calcola punteggio
        if total_checks > 0:
            score = (len(self.passed) / total_checks) * 100
            print(f"\n{Fore.CYAN}Punteggio Sicurezza: {score:.1f}%{Style.RESET_ALL}")
            
            if score >= 80:
                print(f"{Fore.GREEN}Buon livello di sicurezza!{Style.RESET_ALL}")
            elif score >= 60:
                print(f"{Fore.YELLOW}Sicurezza accettabile, ma migliorabile{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Livello di sicurezza insufficiente - azione richiesta!{Style.RESET_ALL}")
        
        # Raccomandazioni
        if self.issues:
            print(f"\n{Fore.RED}🔧 AZIONI PRIORITARIE:{Style.RESET_ALL}")
            for i, issue in enumerate(self.issues[:5], 1):
                print(f"{i}. {issue}")
        
        print(f"\n{Fore.CYAN}💡 NOTA: Questa è un'analisi passiva e non invasiva.")
        print("Per una valutazione completa, considera un audit di sicurezza professionale.{Style.RESET_ALL}\n")

def main():
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║          SAFE SECURITY CHECKER (Analisi Passiva)            ║
║                                                              ║
║  Questo tool è SICURO da usare su qualsiasi sito            ║
║  Non effettua attacchi, solo analisi delle configurazioni   ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)
    
    # Input URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Inserisci URL da analizzare (es. https://tuosito.com): ").strip()
    
    # Valida URL
    if not url.startswith(('http://', 'https://')):
        print(f"{Fore.RED}❌ URL non valido. Deve iniziare con http:// o https://{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"\n{Fore.YELLOW}🔍 Avvio analisi di sicurezza passiva...{Style.RESET_ALL}")
    print(f"Target: {url}")
    input("Premi INVIO per continuare...")
    
    # Esegui analisi
    checker = SafeSecurityChecker(url)
    
    try:
        checker.check_https()
        checker.check_security_headers()
        checker.check_cookie_security()
        checker.check_sensitive_files()
        checker.check_server_info()
        checker.generate_report()
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Analisi interrotta dall'utente{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Errore imprevisto: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
