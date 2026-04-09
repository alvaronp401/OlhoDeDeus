# core/database.py
import sqlite3
import os
from datetime import datetime

DB_PATH = "olhodedeus.db"

def init_db():
    """Inicializa o banco de dados com as tabelas fundamentais."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabela de Alvos (Targets)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS targets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT UNIQUE NOT NULL,
        ip_address TEXT,
        status TEXT DEFAULT 'RECON',
        os_family TEXT, -- Windows, Linux, Darwin
        os_version TEXT,
        tech_stack TEXT, -- PHP, ASP.NET, Java, etc.
        last_scan DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabela de Vulnerabilidades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vulnerabilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_id INTEGER,
        title TEXT NOT NULL,
        severity TEXT, -- CRITICAL, HIGH, MEDIUM, LOW, INFO
        description TEXT,
        remediation TEXT,
        discovery_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (target_id) REFERENCES targets (id)
    )
    ''')
    
    # Tabela de Loot (Credenciais, tokens, arquivos sensíveis)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS loot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_id INTEGER,
        type TEXT, -- CREDENTIAL, TOKEN, SENSITIVE_FILE
        data TEXT NOT NULL,
        origin TEXT, -- URL ou Ferramenta de origem
        captured_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (target_id) REFERENCES targets (id)
    )
    ''')
    
    # Tabela de Histórico de Execução
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS execution_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_id INTEGER,
        comando TEXT NOT NULL,
        output TEXT,
        exit_code INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (target_id) REFERENCES targets (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[DB_INIT] Banco de dados {DB_PATH} inicializado com sucesso.")

class DatabaseManager:
    def __init__(self):
        if not os.path.exists(DB_PATH):
            init_db()

    def get_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def get_or_create_target(self, domain):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM targets WHERE domain = ?", (domain,))
            row = cursor.fetchone()
            if row:
                return row['id']
            
            cursor.execute("INSERT INTO targets (domain) VALUES (?)", (domain,))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_target_intel(self, domain, os_family=None, os_version=None, tech_stack=None):
        target_id = self.get_or_create_target(domain)
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if os_family: cursor.execute("UPDATE targets SET os_family = ? WHERE id = ?", (os_family, target_id))
            if os_version: cursor.execute("UPDATE targets SET os_version = ? WHERE id = ?", (os_version, target_id))
            if tech_stack: cursor.execute("UPDATE targets SET tech_stack = ? WHERE id = ?", (tech_stack, target_id))
            conn.commit()
        finally:
            conn.close()

    def get_target_intel(self, domain):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT os_family, os_version, tech_stack FROM targets WHERE domain = ?", (domain,))
            row = cursor.fetchone()
            return dict(row) if row else {"os_family": "Unknown", "os_version": "N/A", "tech_stack": "N/A"}
        finally:
            conn.close()

    def save_vulnerability(self, domain, title, severity, description, remediation=""):
        target_id = self.get_or_create_target(domain)
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO vulnerabilities (target_id, title, severity, description, remediation)
                VALUES (?, ?, ?, ?, ?)
            ''', (target_id, title, severity.upper(), description, remediation))
            conn.commit()
        finally:
            conn.close()

    def save_loot(self, domain, loot_type, data, origin=""):
        target_id = self.get_or_create_target(domain)
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO loot (target_id, type, data, origin)
                VALUES (?, ?, ?, ?)
            ''', (target_id, loot_type.upper(), data, origin))
            conn.commit()
        finally:
            conn.close()

    def log_execution(self, domain, comando, output, exit_code):
        target_id = self.get_or_create_target(domain)
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO execution_history (target_id, comando, output, exit_code)
                VALUES (?, ?, ?, ?)
            ''', (target_id, comando, output, exit_code))
            cursor.execute("UPDATE targets SET last_scan = ? WHERE id = ?", (datetime.now(), target_id))
            conn.commit()
        finally:
            conn.close()

    def get_vulnerabilities(self, domain=None):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if domain:
                cursor.execute('''
                    SELECT v.* FROM vulnerabilities v
                    JOIN targets t ON v.target_id = t.id
                    WHERE t.domain = ?
                ''', (domain,))
            else:
                cursor.execute('SELECT * FROM vulnerabilities')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_loot(self, domain=None):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if domain:
                cursor.execute('''
                    SELECT l.* FROM loot l
                    JOIN targets t ON l.target_id = t.id
                    WHERE t.domain = ?
                ''', (domain,))
            else:
                cursor.execute('SELECT * FROM loot')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

db = DatabaseManager()
