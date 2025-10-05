Projet Bibliothèque - Interface Graphique avec SQLite

Présentation Ce projet est une application graphique de gestion d'une bibliothèque utilisant Python, Tkinter et SQLite.

L'interface permet :

De consulter, ajouter, modifier et supprimer des entrées dans toutes les tables (Adherent, Livre, Auteur, Genre, Commander, Emprunter).

De répondre facilement aux questions analytiques (Top emprunteurs, Retards, etc.) via des boutons dédiés.

Le tout sans avoir besoin de manipuler directement du SQL : une vraie simplification pour l'administrateur.

Structure du projet:

projet.sql : Script SQLite de création et d’insertion initiale de la base de données.

FicherPostgre.sql : script PostgreSQL seulement pour la correction du projet

bibliotheque.db : Fichier de base de données SQLite utilisé par l'application.

Transformsqlite.py : Script Python pour transformer le fichier .sql en fichier .db.

interface_bibliotheque.py : Programme principal qui lance l'interface graphique (GUI).

Rapport.pdf: rapport qui décrit tous les détails du projet.

interface_bibliotheque.exe : permet aux utilisateur Windows de lancer le GUI directement sans utiliser python

VideoProjet2935.mov: une video qui montre l'interface GUI du projet.

Instructions d'utilisation

Base de données Vous devez disposer d'un fichier bibliotheque.db valide pour utiliser l'application.

Si vous n'avez que le fichier bibliotheque.db, vous pouvez utiliser le script suivant pour le transformer :

python Transformsqlite.py

Attention : Avant d'exécuter Transformsqlite.py, pensez à sauvegarder une copie de bibliotheque.db s'il existe déjà, pour éviter toute perte de données !

Lancer l'application Une fois que vous avez un fichier bibliotheque.db, vous pouvez démarrer l'interface graphique :

python interface_bibliotheque.py

L'application s'ouvre alors et vous pouvez naviguer :

entre les différents formulaires (Adhérents, Livres, Auteurs, etc.),

ou utiliser les boutons prédéfinis pour lancer des analyses rapides.

Environnement requis

Python 3.8 ou version supérieure

Aucun package externe n'est requis

Le projet utilise uniquement des modules standards (sqlite3, tkinter) inclus dans Python.

Remarques importantes

Toutes les opérations sur les données (ajouts, suppressions, modifications) se répercutent directement sur le fichier bibliotheque.db.

Si vous modifiez manuellement le .sql ou le .db, assurez-vous de respecter les contraintes d'intégrité (clés primaires, étrangères, etc.).

L'application active les contraintes de clés étrangères (PRAGMA foreign_keys = ON) pour garantir la cohérence des données.