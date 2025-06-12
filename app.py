import pandas as pd

#import mysql.connector
import pymysql

# Verbindung zur MySQL-Datenbank herstellen

conn = pymysql.connect(
    host="localhost",
    port = 2222,
    user="root",
    password="root",
    database="Anwesenheitsverwaltung"
)
cursor = conn.cursor()

# Excel-Datei einlesen
excel_data = pd.read_excel("Anwesenheit.xlsx")
excel_data['Datum'] = pd.to_datetime(excel_data['Datum']).dt.strftime('%Y-%m-%d')


# Überprüfen, wie die Excel-Daten aussehen
print(excel_data.head())

# Iteration durch die Zeilen der Excel-Datei
for index, row in excel_data.iterrows():
    student_id = row['Student_ID']
    datum = row['Datum']
    status = row['Status']

# Datum in Tabelle 'Tage' einfügen, falls es nicht existiert
cursor.execute("SELECT Tag_ID FROM Tage WHERE Datum = %s", (datum,))
tag_id = cursor.fetchone()
if tag_id is None:
    cursor.execute("INSERT INTO Tage (Datum) VALUES (%s)", (datum,))
    conn.commit()
    cursor.execute("SELECT Tag_ID FROM Tage WHERE Datum = %s", (datum,))
    tag_id = cursor.fetchone()

# Anwesenheit in Tabelle 'Anwesenheit' einfügen
cursor.execute("""
    INSERT INTO Anwesenheit (Student_ID, Tag_ID, Status)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE Status = %s
""", (student_id, tag_id[0], status, status))

conn.commit()

print("Ende der Veranstaltung")
cursor.close()
conn.close()

cursor.execute("SELECT COUNT(*) FROM student WHERE Student_ID = %s", (student_id,))
result = cursor.fetchone()

if result[0] > 0:
    # Der Student_ID existiert, also führe das INSERT oder UPDATE durch
    cursor.execute("""
        INSERT INTO Anwesenheit (Student_ID, Tag_ID, Status)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE Status = %s
    """, (student_id, tag_id[0], status, status))
    conn.commit()
else:
    print(f"Student_ID {student_id} existiert nicht in der student-Tabelle!")
