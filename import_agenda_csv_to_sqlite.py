import sqlite3
import csv
from datetime import datetime

# Caminho para o banco de dados SQLite
db_path = 'db.sqlite3'

# Caminho para o arquivo CSV
csv_path = '/home/vanderson/djangoPI/PJI-310/PJI-310/banco_agenda_agenda.txt'

# Conexão com o banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define os cabeçalhos do CSV manualmente
fieldnames = [
    'id', 'valor', 'data', 'hora', 'descricao',
    'created_at', 'aluno_id','professor_id','cancelado'
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
                INSERT INTO agenda_agenda (
                    id, valor, data, hora, descricao,
                    created_at, aluno_id,professor_id,cancelado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
            ''', (
                row['id'],
                row['valor'],
                row['data'],
                row['hora'],
                row['descricao'],
                row['created_at'],
                row['aluno_id'],
                row['professor_id'],
                row['cancelado'],
            ))
        except Exception as e:
            print(f"Erro ao inserir o usuário: {e}")

# Salva as alterações e fecha a conexão
conn.commit()
conn.close()