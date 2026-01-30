# Security Testing Lab - Guida Completa

## 🎯 Cosa Contiene Questo Progetto

Questo è un ambiente di test per imparare la sicurezza web, contenente:

1. **vulnerable_app.py** - Applicazione web con vulnerabilità intenzionali
2. **security_tester.py** - Script automatico per testare le vulnerabilità
3. Esempi pratici di attacchi comuni (SQL Injection, XSS, CSRF)

## ⚠️ AVVERTENZE IMPORTANTI

- **NON USARE MAI IN PRODUZIONE** - Il codice contiene vulnerabilità intenzionali
- **TESTARE SOLO LOCALMENTE** - Non testare mai su siti di altri senza permesso
- **SCOPO EDUCATIVO** - Solo per imparare la sicurezza web

## 📋 Prerequisiti

- Linux, macOS, o Windows con WSL
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

## 🚀 Setup Completo (Passo per Passo)

### 1. Prepara l'Ambiente

```bash
# Crea una directory per il progetto
mkdir security-lab
cd security-lab

# Crea ambiente virtuale Python
python3 -m venv venv

# Attiva l'ambiente virtuale
# Su Linux/macOS:
source venv/bin/activate
# Su Windows:
# venv\Scripts\activate
```

### 2. Installa le Dipendenze

```bash
# Installa i pacchetti necessari
pip install flask requests colorama

# Verifica l'installazione
pip list
```

### 3. Copia i File nel Progetto

Salva questi file nella directory `security-lab`:
- `vulnerable_app.py`
- `security_tester.py`

### 4. Rendi Eseguibili gli Script

```bash
chmod +x vulnerable_app.py
chmod +x security_tester.py
```

## 🎮 Come Utilizzare il Lab

### Metodo 1: Test Manuale (Raccomandato per Principianti)

#### Passo 1: Avvia l'Applicazione Vulnerabile

```bash
python3 vulnerable_app.py
```

Dovresti vedere:
```
============================================================
APPLICAZIONE DI TEST SICUREZZA WEB
============================================================

L'applicazione sta girando su: http://127.0.0.1:5000
...
```

#### Passo 2: Apri il Browser

Vai su: http://127.0.0.1:5000

Vedrai una homepage con link a diverse sezioni vulnerabili.

#### Passo 3: Testa le Vulnerabilità Manualmente

**Test SQL Injection:**
1. Vai su "Login Vulnerabile"
2. Prova questi username:
   - `admin' OR '1'='1`
   - `admin'--`
   - `' UNION SELECT 1,2,3,4--`
3. Password: qualsiasi cosa
4. Osserva come il login viene bypassato!

**Test XSS:**
1. Vai su "Commenti Vulnerabili"
2. Inserisci questi payload nel campo commento:
   - `<script>alert('XSS')</script>`
   - `<img src=x onerror="alert('XSS')">`
3. Invia e osserva l'esecuzione del codice JavaScript

**Test CSRF:**
1. Vai su "Trasferimento Vulnerabile"
2. Nota che non c'è alcun token di protezione
3. Il form accetta qualsiasi richiesta POST senza verifica

#### Passo 4: Confronta con Versioni Sicure

- Prova le stesse cose su "Login Sicuro", "Commenti Sicuri", etc.
- Nota come gli attacchi vengono bloccati!

### Metodo 2: Test Automatico

#### Passo 1: Avvia l'Applicazione (in un terminale)

```bash
python3 vulnerable_app.py
```

#### Passo 2: Esegui lo Scanner (in un altro terminale)

```bash
# Apri un nuovo terminale
cd security-lab
source venv/bin/activate  # Attiva l'ambiente virtuale
python3 security_tester.py
```

Lo scanner:
- Testerà automaticamente tutte le vulnerabilità
- Mostrerà risultati colorati
- Genererà un report finale

## 📊 Esempio di Output dello Scanner

```
╔════════════════════════════════════════════════════════════╗
║           SECURITY VULNERABILITY SCANNER                   ║
║                                                            ║
║  ATTENZIONE: Usa solo su applicazioni di tua proprietà!   ║
╚════════════════════════════════════════════════════════════╝

Target: http://127.0.0.1:5000
Premi INVIO per iniziare la scansione...

============================================================
TEST SQL INJECTION
============================================================

Testando endpoint: http://127.0.0.1:5000/login-vulnerable

Payload: admin' OR '1'='1
Descrizione: Bypass autenticazione con OR '1'='1'
[✗] SQL INJECTION VULNERABILITÀ CONFERMATA!

...
```

## 🛡️ Vulnerabilità Testate

### 1. SQL Injection
- **Cosa è**: Inserimento di codice SQL malevolo
- **Impatto**: Accesso non autorizzato ai dati
- **Protezione**: Prepared Statements / Parametrized Queries

### 2. Cross-Site Scripting (XSS)
- **Cosa è**: Esecuzione di JavaScript malevolo
- **Impatto**: Furto di cookie, sessioni, dati sensibili
- **Protezione**: HTML escaping / Content Security Policy

### 3. Cross-Site Request Forgery (CSRF)
- **Cosa è**: Richieste forzate da siti esterni
- **Impatto**: Azioni non autorizzate per conto dell'utente
- **Protezione**: Token CSRF univoci per ogni sessione

### 4. Missing Security Headers
- **Cosa è**: Mancanza di header HTTP di sicurezza
- **Impatto**: Varie vulnerabilità (clickjacking, MIME sniffing, etc.)
- **Protezione**: Configurare correttamente i security headers

## 🔧 Troubleshooting

### Problema: "Port already in use"
```bash
# Trova il processo sulla porta 5000
sudo lsof -i :5000
# Termina il processo
kill -9 <PID>
```

### Problema: "Module not found"
```bash
# Assicurati di aver attivato l'ambiente virtuale
source venv/bin/activate
# Reinstalla le dipendenze
pip install flask requests colorama
```

### Problema: "Permission denied"
```bash
# Rendi eseguibile lo script
chmod +x vulnerable_app.py
chmod +x security_tester.py
```

## 📚 Risorse Aggiuntive per Imparare

### Documentazione Ufficiale
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Le 10 vulnerabilità più critiche
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) - Tutorial gratuiti
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### Tool Professionali (per quando sei pronto)
- **OWASP ZAP** - Scanner di vulnerabilità open source
- **Burp Suite** - Suite professionale per penetration testing
- **SQLMap** - Tool automatico per SQL injection
- **Nikto** - Scanner di vulnerabilità web

### Piattaforme di Pratica Legali
- **HackTheBox** - Macchine virtuali vulnerabili legali
- **TryHackMe** - Laboratori di sicurezza guidati
- **DVWA** - Damn Vulnerable Web Application
- **WebGoat** - Applicazione didattica di OWASP

## 🎓 Prossimi Passi

1. **Pratica con questo lab** finché non capisci ogni vulnerabilità
2. **Studia il codice** confrontando versioni vulnerabili e sicure
3. **Prova a scrivere** i tuoi payload personalizzati
4. **Esplora tool professionali** come Burp Suite Community Edition
5. **Partecipa a CTF** (Capture The Flag) per fare pratica

## ⚖️ Note Legali

- Testa **SOLO** su sistemi di tua proprietà
- Non usare mai queste tecniche senza autorizzazione scritta
- Il testing non autorizzato è **illegale** e può portare a conseguenze penali
- Questo codice è solo per **scopi educativi**

## 🤝 Best Practices per la Sicurezza

Quando sviluppi applicazioni reali:

1. ✅ Usa sempre **prepared statements** per query SQL
2. ✅ **Sanitizza** e valida tutti gli input utente
3. ✅ Implementa **token CSRF** per form sensibili
4. ✅ Configura **security headers** appropriati
5. ✅ Usa **HTTPS** per tutte le comunicazioni
6. ✅ Implementa **rate limiting** contro brute force
7. ✅ **Hash** le password con algoritmi sicuri (bcrypt, argon2)
8. ✅ Mantieni **aggiornate** tutte le dipendenze
9. ✅ Fai **code review** e **security audit** regolari
10. ✅ Segui il principio del **least privilege**

## 📝 Licenza

Questo codice è fornito "as-is" per scopi educativi.
Non utilizzare in produzione o per attività illegali.

---

**Buon apprendimento e hack etico! 🔐**
