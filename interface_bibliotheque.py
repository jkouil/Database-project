import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = "bibliotheque.db"

#main frame
def show_homepage(tree, action_frame):
    # clean present view
    tree.delete(*tree.get_children())
    tree["columns"] = ["Message"]
    tree["show"] = "headings"
    tree.heading("Message", text="Bienvenue")
    tree.insert("", tk.END, values=["Bienvenue dans le système de gestion de bibliothèque"])

    for widget in action_frame.winfo_children():
        widget.destroy()

    # 2 requests in question 5
    btns = {
        "Top 3 emprunteurs": """
               SELECT a.ID, a.Nom, COUNT(e.EmpruntID) AS NbEmprunts
               FROM Adherent a
               JOIN Emprunter e ON a.ID = e.AdherentID
               GROUP BY a.Nom
               ORDER BY NbEmprunts DESC
               LIMIT 3
           """,
        "Commandes en attente": """
               SELECT c.CommandeID, l.Titre, a.Nom, a.Email, a.Telephone, c.DateCommande
               FROM Commander c
                   JOIN Livre l ON c.ISBN = l.ISBN
                   JOIN Adherent a ON c.AdherentID = a.ID
               WHERE c.Statut = 'en_attente';

           """

    }

    for label, query in btns.items():
        tk.Button(action_frame, text=label, command=lambda q=query: run_query(q, tree)).pack(side=tk.LEFT, padx=5)

        # 2 other questions in question 5
    tk.Button(action_frame, text="Recherche livre + genre", command=lambda: prompt_for_emprunteurs(tree)).pack(
        side=tk.LEFT, padx=5)

    tk.Button(action_frame, text="Retards > N jours", command=lambda: prompt_for_retards(tree)).pack(side=tk.LEFT,
                                                                                                     padx=5)

# Utilitaires

def get_selected_item(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Attention", "Veuillez sélectionner un élément.")
        return None
    return tree.item(selected[0])["values"]


def confirm_and_execute(data_summary, insert_func):
    if messagebox.askyesno("Confirmation", f"Confirmez-vous l'ajout des données suivantes ?\n\n{data_summary}"):
        try:
            insert_func()
            messagebox.showinfo("Succès", "Ajout effectué avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

def handle_foreign_key_error(e, missing_key_type, add_func):
    if missing_key_type.lower() in str(e).lower():
        if messagebox.askyesno("Clé étrangère manquante", f"{missing_key_type} inexistant. Voulez-vous l'ajouter ?"):
            add_func()
        return True
    return False

def run_query(query, tree):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
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
        messagebox.showerror("Erreur", str(e))

# Fonctions d'ajout

def add_genre():
    win = tk.Toplevel()
    win.title("Ajouter un genre")
    tk.Label(win, text="Nom").grid(row=0, column=0)
    entry = tk.Entry(win)
    entry.grid(row=0, column=1)

    def insert():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Genre (Nom) VALUES (?)", (entry.get().strip(),))
        conn.commit()
        conn.close()
        win.destroy()

    def on_validate():
        nom = entry.get().strip()
        if not nom:
            messagebox.showerror("Erreur", "Le nom ne peut pas être vide.")
            return
        summary = f"Nom: {nom}"
        confirm_and_execute(summary, insert)

    tk.Button(win, text="Valider", command=on_validate).grid(row=1, columnspan=2)

def add_adherent():
    win = tk.Toplevel()
    win.title("Ajouter un adhérent")
    labels = ["Nom", "Adresse", "Email", "Téléphone", "DateInscription"]
    entries = [tk.Entry(win) for _ in labels]
    for i, label in enumerate(labels):
        tk.Label(win, text=label).grid(row=i, column=0)
        entries[i].grid(row=i, column=1)

    def on_validate():
        values = [e.get().strip() for e in entries]
        if any(not v for v in values):
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        summary = "\n".join(f"{l}: {v}" for l, v in zip(labels, values))
        if not messagebox.askyesno("Confirmation", f"Confirmer l'ajout:\n\n{summary}"):
            return
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Adherent (Nom, Adresse, Email, Telephone, DateInscription) VALUES (?, ?, ?, ?, ?)", values)
        conn.commit()
        conn.close()
        win.destroy()

    tk.Button(win, text="Valider", command=on_validate).grid(row=len(labels), columnspan=2)

def add_livre():
    win = tk.Toplevel()
    win.title("Ajouter un livre")
    labels = ["ISBN", "Titre", "DatePublication", "Editeur", "GenreID", "AuteurID"]
    entries = [tk.Entry(win) for _ in labels]
    for i, label in enumerate(labels):
        tk.Label(win, text=label).grid(row=i, column=0)
        entries[i].grid(row=i, column=1)

    def on_validate():
        values = [e.get().strip() for e in entries]
        isbn, titre, datepub, editeur, genreid, auteurid = values
        if any(not v for v in values):
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        summary = "\n".join(f"{l}: {v}" for l, v in zip(labels, values))
        if not messagebox.askyesno("Confirmation", f"Confirmer l'ajout:\n\n{summary}"):
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Livre (ISBN, Titre, DatePublication, Editeur, GenreID) VALUES (?, ?, ?, ?, ?)", (isbn, titre, datepub, editeur, genreid))
            cursor.execute("INSERT INTO Ecrire (AuteurID, ISBN) VALUES (?, ?)", (auteurid, isbn))
            conn.commit()
            conn.close()
            win.destroy()
        except Exception as e:
            if handle_foreign_key_error(e, "Genre", add_genre):
                return
            if handle_foreign_key_error(e, "Auteur", add_adherent):
                return
            messagebox.showerror("Erreur", str(e))

    tk.Button(win, text="Valider", command=on_validate).grid(row=len(labels), columnspan=2)

def add_emprunt(tree):
    win = tk.Toplevel()
    win.title("Ajouter un emprunt")
    labels = ["ISBN", "AdherentID", "DateEmprunt (YYYY-MM-DD)"]
    entries = [tk.Entry(win) for _ in labels]
    for i, label in enumerate(labels):
        tk.Label(win, text=label).grid(row=i, column=0)
        entries[i].grid(row=i, column=1)

    def on_validate():
        isbn, adherent, date = [e.get().strip() for e in entries]
        if any(not v for v in [isbn, adherent, date]):
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        summary = f"ISBN: {isbn}\nAdhérent ID: {adherent}\nDate: {date} → Retour prévu +14 jours"
        if not messagebox.askyesno("Confirmation", f"Confirmer l'ajout:\n\n{summary}"):
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Emprunter (ISBN, AdherentID, DateEmprunt)
                VALUES (?, ?, ?)
            """, (isbn, adherent, date))
            conn.commit()
            conn.close()
            win.destroy()
            run_query("SELECT * FROM Emprunter", tree)
        except Exception as e:
            if handle_foreign_key_error(e, "Adherent", add_adherent):
                return
            if handle_foreign_key_error(e, "Livre", add_livre):
                return
            messagebox.showerror("Erreur", str(e))

    tk.Button(win, text="Valider", command=on_validate).grid(row=3, column=0, columnspan=2)

def add_auteur():
    win = tk.Toplevel()
    win.title("Ajouter un auteur")
    labels = ["Nom", "Nationalité", "DateNaissance (YYYY-MM-DD)", "Adresse"]
    entries = [tk.Entry(win) for _ in labels]
    for i, label in enumerate(labels):
        tk.Label(win, text=label).grid(row=i, column=0)
        entries[i].grid(row=i, column=1)

    def on_validate():
        values = [e.get().strip() for e in entries]
        if any(not v for v in values):
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        summary = "\n".join(f"{l}: {v}" for l, v in zip(labels, values))
        if not messagebox.askyesno("Confirmation", f"Confirmer l'ajout:\n\n{summary}"):
            return
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Auteur (Nom, Nationalite, DateNaissance, Adresse)
            VALUES (?, ?, ?, ?)
        """, values)
        conn.commit()
        conn.close()
        win.destroy()
        messagebox.showinfo("Succès", "Auteur ajouté avec succès.")

    tk.Button(win, text="Valider", command=on_validate).grid(row=len(labels), column=0, columnspan=2, pady=10)

def add_commande():
    win = tk.Toplevel()
    win.title("Ajouter une commande")
    labels = [
        "ISBN", "AdherentID", "DateCommande (YYYY-MM-DD)",
        "Statut (en_attente / honoree / annulee)",
        "DateDebut (YYYY-MM-DD)", "DureePrevue (en jours)"
    ]
    entries = [tk.Entry(win) for _ in labels]
    for i, label in enumerate(labels):
        tk.Label(win, text=label).grid(row=i, column=0)
        entries[i].grid(row=i, column=1)

    def on_validate():
        values = [e.get().strip() for e in entries]
        isbn, adherent_id, date_commande, statut, date_debut, duree_prevue = values
        if any(not v for v in values):
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        if statut not in ("en_attente", "honoree", "annulee"):
            messagebox.showerror("Erreur", "Statut invalide.")
            return
        summary = "\n".join(f"{l}: {v}" for l, v in zip(labels, values))
        if not messagebox.askyesno("Confirmation", f"Confirmer l'ajout:\n\n{summary}"):
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Commander (ISBN, AdherentID, DateCommande, Statut, DateDebut, DureePrevue)
                VALUES (?, ?, ?, ?, ?, ?)
            """, values)
            conn.commit()
            conn.close()
            win.destroy()
            messagebox.showinfo("Succès", "Commande ajoutée avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    tk.Button(win, text="Valider", command=on_validate).grid(row=len(labels), column=0, columnspan=2, pady=10)

# Supprimer
def delete_selected(tree, table):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Alerte", "Veuillez sélectionner une ligne à supprimer.")
        return
    item = tree.item(selected[0])["values"]
    if not messagebox.askyesno("Confirmation", f"Supprimer cette entrée ?\n\n{item}"):
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if table == "Adherent":
            cursor.execute("DELETE FROM Adherent WHERE ID = ?", (item[0],))
        elif table == "Livre":
            cursor.execute("DELETE FROM Livre WHERE ISBN = ?", (item[0],))
        elif table == "Auteur":
            cursor.execute("DELETE FROM Auteur WHERE AuteurID = ?", (item[0],))
        elif table == "Genre":
            cursor.execute("DELETE FROM Genre WHERE GenreID = ?", (item[0],))
        elif table == "Commander":
            cursor.execute("DELETE FROM Commander WHERE CommandeID = ?", (item[0],))
        elif table == "Emprunter":
            cursor.execute("DELETE FROM Emprunter WHERE EmpruntID = ?", (item[0],))
        conn.commit()
        conn.close()
        run_query(f"SELECT * FROM {table}", tree)
        messagebox.showinfo("Succès", "Entrée supprimée avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Modifier
def modify_selected(tree, table):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Alerte", "Veuillez sélectionner une ligne à modifier.")
        return
    item = tree.item(selected[0])["values"]
    win = tk.Toplevel()
    win.title(f"Modifier {table}")

    if table == "Adherent":
        labels = ["Nom", "Adresse", "Email", "Téléphone", "DateInscription"]
        id_field = ("ID", item[0])
        query = "UPDATE Adherent SET Nom=?, Adresse=?, Email=?, Telephone=?, DateInscription=? WHERE ID=?"
    elif table == "Livre":
        labels = ["Titre", "DatePublication", "Editeur", "GenreID"]
        id_field = ("ISBN", item[0])
        query = "UPDATE Livre SET Titre=?, DatePublication=?, Editeur=?, GenreID=? WHERE ISBN=?"
    elif table == "Auteur":
        labels = ["Nom", "Nationalite", "DateNaissance", "Adresse"]
        id_field = ("AuteurID", item[0])
        query = "UPDATE Auteur SET Nom=?, Nationalite=?, DateNaissance=?, Adresse=? WHERE AuteurID=?"
    elif table == "Genre":
        labels = ["Nom"]
        id_field = ("GenreID", item[0])
        query = "UPDATE Genre SET Nom=? WHERE GenreID=?"
    elif table == "Commander":
        labels = ["ISBN", "AdherentID", "DateCommande", "Statut", "DateDebut", "DureePrevue"]
        id_field = ("CommandeID", item[0])
        query = "UPDATE Commander SET ISBN=?, AdherentID=?, DateCommande=?, Statut=?, DateDebut=?, DureePrevue=? WHERE CommandeID=?"
    elif table == "Emprunter":
        labels = ["ISBN", "AdherentID", "DateEmprunt", "DateRetourReelle"]
        id_field = ("EmpruntID", item[0])
        query = "UPDATE Emprunter SET ISBN=?, AdherentID=?, DateEmprunt=?, DateRetourReelle=? WHERE EmpruntID=?"

    entries = []
    for i, label in enumerate(labels):
        tk.Label(win, text=label).grid(row=i, column=0)
        entry = tk.Entry(win)
        entry.insert(0, item[i + 1])
        entry.grid(row=i, column=1)
        entries.append(entry)

    def on_validate():
        new_values = [e.get().strip() for e in entries]
        if any(not v for v in new_values):
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        summary = "\n".join(f"{l}: {v}" for l, v in zip(labels, new_values))
        if not messagebox.askyesno("Confirmation", f"Confirmer les modifications ?\n\n{summary}"):
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(query, (*new_values, id_field[1]))
            conn.commit()
            conn.close()
            run_query(f"SELECT * FROM {table}", tree)
            win.destroy()
            messagebox.showinfo("Succès", "Entrée modifiée avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    tk.Button(win, text="Valider", command=on_validate).grid(row=len(labels), column=0, columnspan=2, pady=10)


# GUI
#this function is to select the correct book name and type
def prompt_for_emprunteurs(tree):
    popup = tk.Toplevel()
    popup.title("Recherche livre + genre")

    tk.Label(popup, text="Titre du livre :").grid(row=0, column=0)
    titre_entry = tk.Entry(popup)
    titre_entry.grid(row=0, column=1)

    tk.Label(popup, text="Genre :").grid(row=1, column=0)
    genre_entry = tk.Entry(popup)
    genre_entry.grid(row=1, column=1)

    def submit():
        titre = titre_entry.get().strip()
        genre = genre_entry.get().strip()

        if not titre and not genre:
            messagebox.showerror("Erreur", "Veuillez entrer au moins un des deux critères.")
            return


        #we could replace all the "?" by other values in params.
        query = """
            SELECT DISTINCT a.ID AS AdherentID, a.Nom, a.Email, a.Telephone,
                            e.ISBN, e.DateEmprunt, e.DateRetourReelle
            FROM Adherent a
            JOIN Emprunter e ON a.ID = e.AdherentID
            JOIN Livre l ON e.ISBN = l.ISBN
            WHERE (? IS NULL OR l.Titre = ?)
              AND (? IS NULL OR l.GenreID = (
                  SELECT GenreID FROM Genre WHERE Nom = ?
              ));
        """

        params = (titre if titre else None, titre if titre else None,
                  genre if genre else None, genre if genre else None)

        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            if not rows:
                messagebox.showinfo("Résultat", "Aucun emprunteur trouvé pour les critères donnés.")
                return


            tree.delete(*tree.get_children())
            tree["columns"] = columns
            tree["show"] = "headings"
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.CENTER)
            for row in rows:
                tree.insert("", tk.END, values=row)

            conn.close()
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    tk.Button(popup, text="Rechercher", command=submit).grid(row=2, columnspan=2, pady=5)


def prompt_for_retards(tree):
    popup = tk.Toplevel()
    popup.title("Retards > N jours")

    tk.Label(popup, text="Nombre de jours de retard minimum :").grid(row=0, column=0)
    entry = tk.Entry(popup)
    entry.grid(row=0, column=1)

    def submit():
        try:
            n = int(entry.get())
            if n < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre entier positif.")
            return

        query = f"""
            SELECT a.ID AS AdherentID, a.Nom, a.Email, a.Telephone,
                   l.ISBN, l.Titre,
                   e.DateEmprunt, e.DateRetourReelle
            FROM Emprunter e
            JOIN Adherent a ON e.AdherentID = a.ID
            JOIN Livre l ON e.ISBN = l.ISBN
            WHERE e.DateRetourReelle IS NOT NULL
              AND DATE(e.DateRetourReelle) > DATE(e.DateEmprunt, '+{14 + int(entry.get())} days')
        """

        try:
            conn = sqlite3.connect(DB_PATH)
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

            conn.close()
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    tk.Button(popup, text="Rechercher", command=submit).grid(row=1, columnspan=2, pady=5)


def build_gui():
    root = tk.Tk()
    root.title("Bibliothèque")
    root.geometry("1200x600")

    tree = ttk.Treeview(root)
    tree.pack(fill=tk.BOTH, expand=True)

    queries = {
        "Adherent": "SELECT * FROM Adherent",
        "Livre": "SELECT * FROM Livre",
        "Auteur": "SELECT * FROM Auteur",
        "Genre": "SELECT * FROM Genre",
        "Commander": "SELECT * FROM Commander",
        "Emprunter": "SELECT * FROM Emprunter"


    }

    def display_query(name):
        run_query(queries[name], tree)


        for widget in action_frame.winfo_children():
            widget.destroy()

        if name == "Adherent":
            tk.Button(action_frame, text="Ajouter Adhérent", command=add_adherent).pack(side=tk.LEFT)
            tk.Button(action_frame, text="Modifier Adhérent", command=lambda: modify_selected(tree, "Adherent")).pack(
                side=tk.LEFT)
            tk.Button(action_frame, text="Supprimer Adhérent", command=lambda: delete_selected(tree, "Adherent")).pack(
                side=tk.LEFT)

        elif name == "Livre":
            tk.Button(action_frame, text="Ajouter Livre", command=add_livre).pack(side=tk.LEFT)
            tk.Button(action_frame, text="Modifier Livre", command=lambda: modify_selected(tree, "Livre")).pack(
                side=tk.LEFT)
            tk.Button(action_frame, text="Supprimer Livre", command=lambda: delete_selected(tree, "Livre")).pack(
                side=tk.LEFT)

        elif name == "Auteur":
            tk.Button(action_frame, text="Ajouter Auteur", command=add_auteur).pack(side=tk.LEFT)
            tk.Button(action_frame, text="Modifier Auteur", command=lambda: modify_selected(tree, "Auteur")).pack(
                side=tk.LEFT)
            tk.Button(action_frame, text="Supprimer Auteur", command=lambda: delete_selected(tree, "Auteur")).pack(
                side=tk.LEFT)

        elif name == "Genre":
            tk.Button(action_frame, text="Ajouter Genre", command=add_genre).pack(side=tk.LEFT)
            tk.Button(action_frame, text="Modifier Genre", command=lambda: modify_selected(tree, "Genre")).pack(
                side=tk.LEFT)
            tk.Button(action_frame, text="Supprimer Genre", command=lambda: delete_selected(tree, "Genre")).pack(
                side=tk.LEFT)

        elif name == "Commander":
            tk.Button(action_frame, text="Ajouter Commande", command=add_commande).pack(side=tk.LEFT)
            tk.Button(action_frame, text="Modifier Commande", command=lambda: modify_selected(tree, "Commander")).pack(
                side=tk.LEFT)
            tk.Button(action_frame, text="Supprimer Commande", command=lambda: delete_selected(tree, "Commander")).pack(
                side=tk.LEFT)

        elif name == "Emprunter":
            tk.Button(action_frame, text="Ajouter Emprunt", command=lambda: add_emprunt(tree)).pack(side=tk.LEFT)
            tk.Button(action_frame, text="Modifier Emprunt", command=lambda: modify_selected(tree, "Emprunter")).pack(
                side=tk.LEFT)
            tk.Button(action_frame, text="Supprimer Emprunt", command=lambda: delete_selected(tree, "Emprunter")).pack(
                side=tk.LEFT)

    # Home page frame
    top_menu = tk.Frame(root)
    top_menu.pack(side=tk.TOP, pady=4)

    # Home button
    tk.Button(top_menu, text="Home", command=lambda: show_homepage(tree, action_frame), width=15).pack(side=tk.LEFT, padx=5)

    # check tab buttons
    for name in ["Adherent", "Livre", "Auteur", "Genre", "Commander", "Emprunter"]:
        tk.Button(top_menu, text=f"Voir {name}", command=lambda n=name: display_query(n)).pack(side=tk.LEFT, padx=2)

    # botton frame
    action_frame = tk.Frame(root)
    action_frame.pack(side=tk.BOTTOM, pady=5)



    # home page
    show_homepage(tree, action_frame)

    root.mainloop()


if __name__ == "__main__":
    build_gui()
