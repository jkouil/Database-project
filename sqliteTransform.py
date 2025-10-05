import sqlite3

with open("Projet.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

conn = sqlite3.connect("bibliotheque.db")
cursor = conn.cursor()
cursor.executescript(sql_script)
conn.commit()
conn.close()
