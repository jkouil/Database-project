import tkinter as tk
from tkinter import ttk
import psycopg2


DB_CONFIG = {
    "dbname": "bibliotheque",
    "user": "postgres",
    "password": "", 
    "host": "localhost",
    "port": 5432
}

def run_query(query, tree):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        tree.delete(*tree.get_children())
        tree["columns"] = columns
        tree["show"] = "headings"
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER)

        for row in rows:
            tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()
    except Exception as e:
        print("Erreur:", e)

root = tk.Tk()
root.title("Bibliothèque - Interface des requêtes")
root.geometry("900x500")

tree = ttk.Treeview(root)
tree.pack(fill=tk.BOTH, expand=True)

queries = {
    "Top 3 emprunteurs": """
        SELECT a.Nom, COUNT(e.EmpruntID) AS NbEmprunts
        FROM Adherent a
        JOIN Emprunter e ON a.ID = e.AdherentID
        GROUP BY a.Nom
        ORDER BY NbEmprunts DESC
        LIMIT 3;
    """,
    "Commandes en attente": """
        SELECT
            c.CommandeID,
            a.Nom AS NomAdherent,
            l.Titre AS TitreLivre,
            c.DateCommande,
            c.DateDebut,
            c.DureePrevue
        FROM Commander c
        JOIN Adherent a ON c.AdherentID = a.ID
        JOIN Livre l ON c.ISBN = l.ISBN
        WHERE c.Statut = 'en_attente';
    """,
    "Nombre de livres par genre": """
        SELECT
            g.Nom AS Genre,
            COUNT(l.ISBN) AS NbLivres
        FROM Genre g
        LEFT JOIN Livre l ON g.GenreID = l.GenreID
        GROUP BY g.Nom
        ORDER BY NbLivres DESC;
    """,
    "Top 5 livres réservés": """
        SELECT
            l.Titre,
            COUNT(c.CommandeID) AS NbCommandes
        FROM Livre l
        JOIN Commander c ON l.ISBN = c.ISBN
        GROUP BY l.Titre
        ORDER BY NbCommandes DESC
        LIMIT 5;
    """
}


button_frame = tk.Frame(root)
button_frame.pack(pady=10)

for label, query in queries.items():
    tk.Button(button_frame, text=label, command=lambda q=query: run_query(q, tree), width=30).pack(side=tk.LEFT, padx=5)

root.mainloop()
