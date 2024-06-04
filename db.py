import sqlite3
from datetime import datetime

def create_connection():
    conn = sqlite3.connect('metas.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario TEXT NOT NULL,
            meta TEXT NOT NULL,
            status TEXT NOT NULL,
            data_criacao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_meta(funcionario, meta):
    conn = create_connection()
    cursor = conn.cursor()
    data_criacao = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('INSERT INTO metas (funcionario, meta, status, data_criacao) VALUES (?, ?, ?, ?)', 
                   (funcionario, meta, 'Pendente', data_criacao))
    conn.commit()
    conn.close()

def get_metas():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM metas')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_status(funcionario, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE metas SET status = ? WHERE funcionario = ?', (status, funcionario))
    conn.commit()
    conn.close()

def delete_meta(funcionario, meta):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM metas WHERE funcionario = ? AND meta = ?', (funcionario, meta))
    conn.commit()
    conn.close()

def get_metas_by_funcionario(funcionario):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM metas WHERE funcionario = ?', (funcionario,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_metas_by_date_range(start_date, end_date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM metas WHERE data_criacao BETWEEN ? AND ?', (start_date, end_date))
    rows = cursor.fetchall()
    conn.close()
    return rows

def reset_metas():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM metas')
    conn.commit()
    conn.close()
