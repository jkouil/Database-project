import tkinter as tk
from tkinter import ttk
import psycopg2

# 数据库连接配置
DB_CONFIG = {
    "dbname": "bibliotheque",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": 5432
}
print("查询已更新")
# 执行 SQL 查询
def run_query(query, tree):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # 清空旧内容
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

# 创建主窗口
root = tk.Tk()
root.title("Bibliotheque - Interface des requetes")
root.geometry("900x500")

# 创建表格组件
tree = ttk.Treeview(root)
tree.pack(fill=tk.BOTH, expand=True)

# 查询语句字典
# 查询语句字典
queries = {
    "Durée moyenne des emprunts": """
        SELECT
            AVG(e.DateRetourReelle - e.DateEmprunt) AS DureeMoyenne
        FROM Emprunter e
        WHERE e.DateRetourReelle IS NOT NULL;
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
    "Top 5 des livres les plus réservés": """
        SELECT
            l.Titre,
            COUNT(c.CommandeID) AS NbCommandes
        FROM Livre l
            JOIN Commander c ON l.ISBN = c.ISBN
        GROUP BY l.Titre
        ORDER BY NbCommandes DESC
        LIMIT 5;
    """,
    "Détails des réservations honorées": """
        SELECT
            c.CommandeID,
            a.Nom AS Adherent,
            l.Titre,
            c.DateDebut,
            c.DureePrevue
        FROM Commander c
            JOIN Adherent a ON c.AdherentID = a.ID
            JOIN Livre l ON c.ISBN = l.ISBN
        WHERE c.Statut = 'honoree';
    """
}


# 按钮面板
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

for label, query in queries.items():
    tk.Button(button_frame, text=label, command=lambda q=query: run_query(q, tree), width=30).pack(side=tk.LEFT, padx=5)

# 启动界面
root.mainloop()
