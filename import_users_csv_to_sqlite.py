import sqlite3
import csv
from datetime import datetime

# Caminho para o banco de dados SQLite
db_path = 'db.sqlite3'

# Caminho para o arquivo CSV
csv_path = 'banco_users.txt'

# Conexão com o banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define os cabeçalhos do CSV manualmente
fieldnames = [
    'password', 'last_login', 'is_superuser', 'first_name', 'last_name',
    'is_staff', 'is_active', 'date_joined', 'document', 'postal_code', 'phone',
    'birth_date', 'full_address', 'email', 'is_professor'
]

# Lê o arquivo CSV e insere os dados
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    
    # Ignora a primeira linha (cabeçalhos do arquivo original, se existirem)
    next(reader, None)
    
    for row in reader:
        try:
            # Verifica se o arquivo foi lido corretamente
            print(f"Lendo linha: {row}")
            
            cursor.execute('''
                INSERT INTO users_userprofile (
                    password, last_login, is_superuser, first_name, last_name, 
                    is_staff, is_active, date_joined, document, postal_code, phone, 
                    birth_date, full_address, email, is_professor
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['password'],
                row['last_login'] if row['last_login'] else None,
                int(row['is_superuser']),
                row['first_name'],
                row['last_name'],
                int(row['is_staff']),
                int(row['is_active']),
                row['date_joined'],
                row['document'],
                row['postal_code'],
                row['phone'],
                row['birth_date'],
                row['full_address'],
                row['email'],
                int(row['is_professor']),
            ))
        except Exception as e:
            print(f"Erro ao inserir o usuário: {e}")

# Salva as alterações e fecha a conexão
conn.commit()
conn.close()
print("Importação concluída com sucesso!")