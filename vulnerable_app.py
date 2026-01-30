#!/usr/bin/env python3
"""
Applicazione vulnerabile per SOLO scopi di test e apprendimento
NON USARE IN PRODUZIONE!
"""

from flask import Flask, request, render_template_string, session
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Inizializza database di test
def init_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    cursor.execute("DELETE FROM users")
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'password123', 'admin@test.com')")
    cursor.execute("INSERT INTO users VALUES (2, 'user', 'user123', 'user@test.com')")
    conn.commit()
    conn.close()

# ❌ VULNERABILE A SQL INJECTION
@app.route('/login-vulnerable', methods=['GET', 'POST'])
def login_vulnerable():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        # VULNERABILE: concatenazione diretta
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        print(f"[DEBUG] Query: {query}")
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return f"<h1>Login riuscito!</h1><p>Benvenuto {user[1]}</p>"
            else:
                return "<h1>Login fallito</h1>"
        except Exception as e:
            return f"<h1>Errore SQL</h1><pre>{str(e)}</pre>"
    
    return '''
        <h2>Login Vulnerabile (Test SQL Injection)</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <button>Login</button>
        </form>
        <p><b>Prova questi payload:</b></p>
        <ul>
            <li>Username: <code>admin' OR '1'='1</code> Password: qualsiasi</li>
            <li>Username: <code>admin'--</code> Password: qualsiasi</li>
        </ul>
    '''

# ✅ SICURO CON PREPARED STATEMENTS
@app.route('/login-secure', methods=['GET', 'POST'])
def login_secure():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        # SICURO: prepared statement con parametri
        query = "SELECT * FROM users WHERE username=? AND password=?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return f"<h1>Login riuscito!</h1><p>Benvenuto {user[1]}</p>"
        else:
            return "<h1>Login fallito</h1>"
    
    return '''
        <h2>Login Sicuro</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <button>Login</button>
        </form>
        <p>Questa versione è protetta contro SQL Injection</p>
    '''

# ❌ VULNERABILE A XSS
@app.route('/comment-vulnerable', methods=['GET', 'POST'])
def comment_vulnerable():
    if request.method == 'POST':
        comment = request.form['comment']
        # VULNERABILE: nessun escape dell'input
        return f'''
            <h2>Commento Inserito:</h2>
            <div style="border:1px solid #ccc; padding:10px">
                {comment}
            </div>
            <a href="/comment-vulnerable">Torna indietro</a>
        '''
    
    return '''
        <h2>Commenti (Vulnerabile XSS)</h2>
        <form method="POST">
            Commento: <textarea name="comment" rows="4" cols="50"></textarea><br>
            <button>Invia</button>
        </form>
        <p><b>Prova questi payload XSS:</b></p>
        <ul>
            <li><code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code></li>
            <li><code>&lt;img src=x onerror="alert('XSS')"&gt;</code></li>
            <li><code>&lt;svg onload=alert('XSS')&gt;</code></li>
        </ul>
    '''

# ✅ SICURO CONTRO XSS
@app.route('/comment-secure', methods=['GET', 'POST'])
def comment_secure():
    if request.method == 'POST':
        comment = request.form['comment']
        # SICURO: usa render_template_string che fa escape automatico
        return render_template_string('''
            <h2>Commento Inserito:</h2>
            <div style="border:1px solid #ccc; padding:10px">
                {{ comment }}
            </div>
            <a href="/comment-secure">Torna indietro</a>
        ''', comment=comment)
    
    return '''
        <h2>Commenti (Protetto XSS)</h2>
        <form method="POST">
            Commento: <textarea name="comment" rows="4" cols="50"></textarea><br>
            <button>Invia</button>
        </form>
        <p>Questa versione fa escape automatico dell'HTML</p>
    '''

# ❌ VULNERABILE A CSRF
@app.route('/transfer-vulnerable', methods=['GET', 'POST'])
def transfer_vulnerable():
    if request.method == 'POST':
        recipient = request.form['recipient']
        amount = request.form['amount']
        return f'''
            <h2>Trasferimento Eseguito!</h2>
            <p>Inviati €{amount} a {recipient}</p>
            <a href="/transfer-vulnerable">Nuovo trasferimento</a>
        '''
    
    return '''
        <h2>Trasferimento (Vulnerabile CSRF)</h2>
        <form method="POST">
            Destinatario: <input name="recipient"><br>
            Importo: <input name="amount" type="number"><br>
            <button>Trasferisci</button>
        </form>
        <p><b>Vulnerabilità:</b> Nessun token CSRF</p>
    '''

# ✅ SICURO CONTRO CSRF
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

@app.route('/transfer-secure', methods=['GET', 'POST'])
def transfer_secure():
    if request.method == 'POST':
        csrf_token = request.form.get('csrf_token')
        
        if csrf_token != session.get('csrf_token'):
            return "<h1>CSRF Token Invalido!</h1>", 403
        
        recipient = request.form['recipient']
        amount = request.form['amount']
        return f'''
            <h2>Trasferimento Eseguito!</h2>
            <p>Inviati €{amount} a {recipient}</p>
            <a href="/transfer-secure">Nuovo trasferimento</a>
        '''
    
    token = generate_csrf_token()
    return f'''
        <h2>Trasferimento (Protetto CSRF)</h2>
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{token}">
            Destinatario: <input name="recipient"><br>
            Importo: <input name="amount" type="number"><br>
            <button>Trasferisci</button>
        </form>
        <p><b>Protezione:</b> Token CSRF presente</p>
    '''

# Homepage con tutti i link
@app.route('/')
def index():
    return '''
        <h1>Applicazione di Test Sicurezza Web</h1>
        <p><b>ATTENZIONE:</b> Questa app contiene vulnerabilità intenzionali per scopi educativi!</p>
        
        <h2>SQL Injection</h2>
        <ul>
            <li><a href="/login-vulnerable">Login Vulnerabile</a></li>
            <li><a href="/login-secure">Login Sicuro</a></li>
        </ul>
        
        <h2>Cross-Site Scripting (XSS)</h2>
        <ul>
            <li><a href="/comment-vulnerable">Commenti Vulnerabili</a></li>
            <li><a href="/comment-secure">Commenti Sicuri</a></li>
        </ul>
        
        <h2>Cross-Site Request Forgery (CSRF)</h2>
        <ul>
            <li><a href="/transfer-vulnerable">Trasferimento Vulnerabile</a></li>
            <li><a href="/transfer-secure">Trasferimento Sicuro</a></li>
        </ul>
    '''

if __name__ == '__main__':
    init_db()
    print("\n" + "="*60)
    print("APPLICAZIONE DI TEST SICUREZZA WEB")
    print("="*60)
    print("\nL'applicazione sta girando su: http://127.0.0.1:5000")
    print("\nQuesta app contiene vulnerabilità INTENZIONALI per test!")
    print("NON USARE MAI questo codice in produzione!")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
