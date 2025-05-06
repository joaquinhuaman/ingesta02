import boto3
import pymysql
import csv
import os

# Leer variables de entorno
host = os.getenv("DB_HOST", "localhost")
user = os.getenv("DB_USER", "utec")
password = os.getenv("DB_PASSWORD", "utec")
database = os.getenv("DB_NAME", "testdb")
tabla = os.getenv("DB_TABLE", "employees")
bucket = os.getenv("BUCKET_NAME", "ingesta02")  # Aquí se cambia el nombre del bucket

# Conexión a MySQL
conn = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM {tabla}")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# Guardar CSV
csv_file = "salida.csv"
with open(csv_file, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

cursor.close()
conn.close()

# Subir a S3
s3 = boto3.client('s3')
s3.upload_file(csv_file, bucket, csv_file)

print("✅ Ingesta completada: datos MySQL → CSV → S3")
