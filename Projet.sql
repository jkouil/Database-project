DROP TABLE IF EXISTS Commander;
DROP TABLE IF EXISTS Emprunter;
DROP TABLE IF EXISTS Ecrire;
DROP TABLE IF EXISTS Livre;
DROP TABLE IF EXISTS Auteur;
DROP TABLE IF EXISTS Adherent;
DROP TABLE IF EXISTS Genre;

-- Table: Genre
CREATE TABLE Genre (
  GenreID SERIAL PRIMARY KEY,
  Nom VARCHAR(100) NOT NULL
);

-- Table: Livre
CREATE TABLE Livre (
  ISBN VARCHAR(20) PRIMARY KEY,
  Titre VARCHAR(200) NOT NULL,
  DatePublication DATE,
  Editeur VARCHAR(100),
  GenreID INTEGER REFERENCES Genre(GenreID)
);

-- Table: Auteur
CREATE TABLE Auteur (
  AuteurID SERIAL PRIMARY KEY,
  Nom VARCHAR(100) NOT NULL,
  Nationalite VARCHAR(50),
  DateNaissance DATE,
  Adresse TEXT
);

-- Table: Ecrire (many-to-many relationship between Auteur and Livre)
CREATE TABLE Ecrire (
  AuteurID INTEGER REFERENCES Auteur(AuteurID),
  ISBN VARCHAR(20) REFERENCES Livre(ISBN),
  PRIMARY KEY (AuteurID, ISBN)
);

-- Table: Adherent
CREATE TABLE Adherent (
  ID SERIAL PRIMARY KEY,
  Nom VARCHAR(100) NOT NULL,
  Adresse TEXT,
  Email VARCHAR(100),
  Téléphone VARCHAR(20),
  DateInscription DATE
);

-- Table: Emprunter
CREATE TABLE Emprunter (
  EmpruntID SERIAL PRIMARY KEY,
  ISBN VARCHAR(20) REFERENCES Livre(ISBN),
  AdherentID INTEGER REFERENCES Adherent(ID),
  DateEmprunt DATE NOT NULL,
  DateRetourPrévue DATE NOT NULL,
  DateRetourRéelle DATE,
  EstEnRetard BOOLEAN,
  CHECK (DateRetourRéelle IS NULL OR DateRetourRéelle > DateEmprunt),
  CHECK (DateRetourPrévue <= DateEmprunt + INTERVAL '14 days')
);

-- Table: Commander
CREATE TABLE Commander (
  CommandeID SERIAL PRIMARY KEY,
  ISBN VARCHAR(20) REFERENCES Livre(ISBN),
  AdherentID INTEGER REFERENCES Adherent(ID),
  DateCommande DATE NOT NULL,
  Statut VARCHAR(20) CHECK (Statut IN ('en_attente', 'honorée', 'annulée')),
  DateDébut DATE,
  DuréePrévue INTEGER
);


-- ===== Données d'exemple =====

-- Insertion dans Genre
INSERT INTO Genre (GenreID, Nom) VALUES
                            (1, 'Science-Fiction'),
                            (2,'Roman'),
                            (3,'Philosophie'),
                            (4,'Histoire'),
                            (5,'Poésie'),
                            (6,'Théâtre'),
                            (7,'Biographie'),
                            (8,'Fantastique'),
                            (9,'Économie'),
                            (10,'Psychologie');
-- Insertion dans Auteur
INSERT INTO Auteur (AuteurID, Nom, Nationalite, DateNaissance, Adresse) VALUES
    (1,'Isaac Asimov', 'Américain', '1920-01-02', 'Brooklyn, New York'),
    (2,'Albert Camus', 'Français', '1913-11-07', 'Mondovi, Algérie'),
    (3,'George Orwell', 'Britannique', '1903-06-25', 'Motihari, Inde'),
    (4,'Platon', 'Grec', '0428-01-01', 'Athènes'),
    (5,'Voltaire', 'Français', '1694-11-21', 'Paris'),
    (6,'Victor Hugo', 'Français', '1802-02-26', 'Besançon'),
    (7,'Aldous Huxley', 'Britannique', '1894-07-26', 'Godalming'),
    (8,'Robert M. Pirsig', 'Américain', '1928-09-06', 'Minneapolis'),
    (9,'Harper Lee', 'Américaine', '1926-04-28', 'Monroeville, Alabama'),
    (10,'Machiavel', 'Italien', '1469-05-03', 'Florence'),
    (11, 'Jules Michelet', 'Français', '1798-08-21', 'Paris'),
    (12, 'Stefan Zweig', 'Autrichien', '1881-11-28', 'Vienne'),
    (13, 'Bryan Ward-Perkins', 'Britannique', '1960-01-01', 'Oxford'),
    (14, 'Paul Éluard', 'Français', '1895-12-14', 'Saint-Denis'),
    (15, 'Charles Baudelaire', 'Français', '1821-04-09', 'Paris'),
    (16, 'Arthur Rimbaud', 'Français', '1854-10-20', 'Charleville'),
    (17, 'Jean Racine', 'Français', '1639-12-22', 'La Ferté-Milon'),
    (18, 'Pierre Corneille', 'Français', '1606-06-06', 'Rouen'),
    (19, 'Jean Anouilh', 'Français', '1910-06-23', 'Bordeaux'),
    (20, 'Guy de Maupassant', 'Français', '1850-08-05', 'Tourville-sur-Arques'),
    (21, 'Anne Frank', 'Allemande', '1929-06-12', 'Francfort'),
    (22, 'Michelle Obama', 'Américaine', '1964-01-17', 'Chicago'),
    (23, 'J.R.R. Tolkien', 'Britannique', '1892-01-03', 'Bloemfontein'),
    (24, 'J.K. Rowling', 'Britannique', '1965-07-31', 'Yate'),
    (25, 'Christopher Paolini', 'Américain', '1983-11-17', 'Montana'),
    (26, 'Karl Marx', 'Allemand', '1818-05-05', 'Trèves'),
    (27, 'John Maynard Keynes', 'Britannique', '1883-06-05', 'Cambridge'),
    (28, 'Steven D. Levitt', 'Américain', '1967-05-29', 'New Orleans'),
    (29, 'Richard J. Gerrig', 'Américain', '1959-01-01', 'New York'),
    (30, 'Sigmund Freud', 'Autrichien', '1856-05-06', 'Freiberg');


-- Insertion dans Livre
INSERT INTO Livre (ISBN, Titre, DatePublication, Editeur, GenreID) VALUES
    ('9780451524935', '1984', '1949-06-08', 'Secker & Warburg', 1),
    ('9782070360024', 'L''Étranger', '1942-05-01', 'Gallimard', 2),
    ('9780553293357', 'Foundation', '1951-06-01', 'Gnome Press', 1),
    ('9780140449266', 'Le Prince', '1532-01-01', 'Penguin Classics', 3),
    ('9780140449136', 'Les Misérables', '1862-01-01', 'Penguin Classics', 2),
    ('9780061122415', 'To Kill a Mockingbird', '1960-07-11', 'Harper Perennial', 2),
    ('9780141182803', 'Brave New World', '1932-01-01', 'Vintage', 1),
    ('9780140449181', 'La République', '380-01-01', 'Flammarion', 3),
    ('9780140449273', 'Candide', '1759-01-01', 'Gallimard', 2),
    ('9780385472579', 'Zen and the Art of Motorcycle Maintenance', '1974-04-01', 'HarperTorch', 3),
    ('9780679720201', 'Histoire de la Révolution française', '1847-01-01', 'Librairie Garnier Frères', 4),
    ('9782070380176', 'Le Monde d’hier', '1942-01-01', 'Stock', 4),
    ('9782070372751', 'La Chute de l’Empire romain', '1984-01-01', 'Gallimard', 4),
    ('9782020123456', 'Anthologie de la poésie française', '1998-04-01', 'Seuil', 5),
    ('9782070314974', 'Les Fleurs du mal', '1857-01-01', 'Gallimard', 5),
    ('9782253004226', 'Le Bateau ivre', '1871-01-01', 'Éditions du Seuil', 5),
    ('9782070381111', 'Phèdre', '1677-01-01', 'Gallimard', 6),
    ('9782070360534', 'Le Cid', '1637-01-01', 'Gallimard', 6),
    ('9782070360909', 'Antigone', '1944-01-01', 'La Table Ronde', 6),
    ('9782070455674', 'Une vie', '1883-01-01', 'Flammarion', 7),
    ('9782070371875', 'Journal d’Anne Frank', '1947-06-25', 'Calmann-Lévy', 7),
    ('9782070389025', 'Devenir', '2018-11-13', 'Fayard', 7),
    ('9782738112345', 'Le Seigneur des Anneaux', '1954-07-29', 'Bourgois', 8),
    ('9782070643029', 'Harry Potter à l’école des sorciers', '1997-06-26', 'Gallimard Jeunesse', 8),
    ('9782081234567', 'Eragon', '2002-08-26', 'Bayard Jeunesse', 8),
    ('9782070101010', 'Le Capital', '1867-01-01', 'Éditions Sociales', 9),
    ('9782070101027', 'Théorie générale de l’emploi, de l’intérêt et de la monnaie', '1936-01-01', 'Payot', 9),
    ('9782070101034', 'Freakonomics', '2005-01-01', 'Pearson', 9),
    ('9782070101041', 'Introduction à la psychologie', '2000-01-01', 'De Boeck', 10),
    ('9782070101058', 'L’Interprétation des rêves', '1899-01-01', 'PUF', 10);


-- Insertion dans Ecrire
INSERT INTO Ecrire (AuteurID, ISBN) VALUES
    (1, '9780553293357'),  -- Isaac Asimov = Foundation
    (2, '9782070360024'),  -- Albert Camus = L'Étranger
    (3, '9780451524935'),  -- George Orwell = 1984
    (10, '9780140449266'), -- Machiavel = Le Prince
    (6, '9780140449136'),  -- Victor Hugo = Les Misérables
    (9, '9780061122415'),  -- Harper Lee = To Kill a Mockingbird
    (7, '9780141182803'),  -- Aldous Huxley = Brave New World
    (4, '9780140449181'),  -- Platon = La République
    (5, '9780140449273'),  -- Voltaire = Candide
    (8, '9780385472579'),  -- Robert M. Pirsig = Zen and the Art...
    (11, '9780679720201'),
    (12, '9782070380176'),
    (13, '9782070372751'),
    (14, '9782020123456'),
    (15, '9782070314974'),
    (16, '9782253004226'),
    (17, '9782070381111'),
    (18, '9782070360534'),
    (19, '9782070360909'),
    (20, '9782070455674'),
    (21, '9782070371875'),
    (22, '9782070389025'),
    (23, '9782738112345'),
    (24, '9782070643029'),
    (25, '9782081234567'),
    (26, '9782070101010'),
    (27, '9782070101027'),
    (28, '9782070101034'),
    (29, '9782070101041'),
    (30, '9782070101058');


-- Insertion dans Adherent
INSERT INTO Adherent (Nom, Adresse, Email, Téléphone, DateInscription) VALUES
    ('Jean Dupont', '123 rue Principale', 'jean@gmail.com', '514-123-4567', '2024-01-15'),
    ('Marie Tremblay', '456 avenue des Lilas', 'marie@gmail.com', '514-987-6543', '2023-10-05'),
    ('Alexandre Morin', '789 boulevard Saint-Laurent', 'alexandre.morin@gmail.com', '514-111-2222', '2023-09-10'),
    ('Sophie Gagnon', '321 rue des Pins', 'sophie.gagnon@hotmail.com', '514-333-4444', '2024-02-20'),
    ('Luc Tremblay', '654 chemin du Lac', 'luc.tremblay@gmail.com', '514-555-6666', '2023-12-01'),
    ('Émilie Lefebvre', '987 avenue Cartier', 'emilie.lefebvre@gmail.com', '514-777-8888', '2024-03-05'),
    ('Marc-André Boucher', '111 rue de la Montagne', 'marc.boucher@yahoo.ca', '514-999-0000', '2023-11-17'),
    ('Chloé Lavoie', '222 avenue Laurier', 'chloe.lavoie@gmail.com', '514-246-1357', '2023-08-22'),
    ('Thomas Nguyen', '333 rue Saint-Denis', 'thomas.nguyen@gmail.com', '514-852-9637', '2024-04-01'),
    ('Isabelle Fortin', '444 boulevard René-Lévesque', 'isabelle.fortin@gmail.com', '514-369-1470', '2023-07-19');

-- Insertion dans Emprunter
INSERT INTO Emprunter (ISBN, AdherentID, DateEmprunt, DateRetourPrévue, DateRetourRéelle, EstEnRetard) VALUES
    ('9780451524935', 1, '2025-04-01', '2025-04-15', '2025-04-16', TRUE),
    ('9782070360024', 2, '2025-04-05', '2025-04-19', NULL, FALSE),
    ('9780140449273', 1, '2025-03-15', '2025-03-29', '2025-04-01', TRUE),
    ('9780061122415', 2, '2025-04-10', '2025-04-24', NULL, FALSE),
    ('9780141182803', 1, '2025-04-12', '2025-04-26', NULL, FALSE),
    ('9780679720201', 3, '2025-03-20', '2025-04-03', '2025-04-05', TRUE),
    ('9782070314974', 4, '2025-04-02', '2025-04-16', NULL, FALSE),
    ('9782070360534', 5, '2025-03-28', '2025-04-11', '2025-04-10', FALSE),
    ('9782738112345', 6, '2025-04-01', '2025-04-15', NULL, FALSE),
    ('9782070389025', 7, '2025-04-04', '2025-04-18', '2025-04-20', TRUE);

-- Insertion dans Commander
INSERT INTO Commander (ISBN, AdherentID, DateCommande, Statut, DateDébut, DuréePrévue) VALUES
    ('9780553293357', 1, '2025-04-10', 'en_attente', '2025-04-20', 7),
    ('9780451524935', 2, '2025-04-11', 'honorée', '2025-04-12', 14),
    ('9780140449136', 1, '2025-04-09', 'en_attente', '2025-04-18', 10),
    ('9780385472579', 2, '2025-04-13', 'annulée', '2025-04-15', 5),
    ('9780140449181', 1, '2025-04-14', 'honorée', '2025-04-15', 14),
    ('9782070360909', 3, '2025-04-12', 'en_attente', '2025-04-20', 7),
    ('9782070371875', 4, '2025-04-08', 'honorée', '2025-04-09', 10),
    ('9782070643029', 5, '2025-04-06', 'annulée', '2025-04-08', 5),
    ('9782070101058', 6, '2025-04-07', 'en_attente', '2025-04-15', 14),
    ('9782070101034', 7, '2025-04-03', 'honorée', '2025-04-04', 10);

-- ===== TEST QUERIES =====
-- 未归还的Emprunter
SELECT
    e.EmpruntID,
    a.Nom AS NomAdherent,
    l.Titre AS TitreLivre,
    e.DateEmprunt,
    e.DateRetourPrévue,
    e.DateRetourRéelle,
    e.EstEnRetard
FROM Emprunter e
         JOIN Adherent a ON e.AdherentID = a.ID
         JOIN Livre l ON e.ISBN = l.ISBN
WHERE e.DateRetourRéelle IS NULL;

-- 查询每位会员的借阅总数（包含历史记录）
SELECT
    a.Nom AS NomAdherent,
    COUNT(e.EmpruntID) AS TotalEmprunts
FROM Adherent a
         LEFT JOIN Emprunter e ON a.ID = e.AdherentID
GROUP BY a.Nom;

-- 查询当前仍在等待状态的预约
SELECT
    c.CommandeID,
    a.Nom AS NomAdherent,
    l.Titre AS TitreLivre,
    c.DateCommande,
    c.DateDébut,
    c.DuréePrévue
FROM Commander c
         JOIN Adherent a ON c.AdherentID = a.ID
         JOIN Livre l ON c.ISBN = l.ISBN
WHERE c.Statut = 'en_attente';

-- 查询逾期归还的借阅记录
SELECT
    e.EmpruntID,
    a.Nom,
    l.Titre,
    e.DateEmprunt,
    e.DateRetourPrévue,
    e.DateRetourRéelle
FROM Emprunter e
         JOIN Adherent a ON e.AdherentID = a.ID
         JOIN Livre l ON e.ISBN = l.ISBN
WHERE e.EstEnRetard = TRUE;

-- 查询每本书被借阅的次数
SELECT
    l.Titre,
    COUNT(e.EmpruntID) AS NbEmprunts
FROM Livre l
         LEFT JOIN Emprunter e ON l.ISBN = e.ISBN
GROUP BY l.Titre
ORDER BY NbEmprunts DESC;

-- 查询每个会员当前正在借阅的书籍（即未归还）
SELECT
    a.Nom AS NomAdherent,
    COUNT(*) AS LivresNonRendus
FROM Emprunter e
         JOIN Adherent a ON e.AdherentID = a.ID
WHERE e.DateRetourRéelle IS NULL
GROUP BY a.Nom;

-- 查询借阅记录的平均持续时间（仅统计已归还）
SELECT
    AVG(e.DateRetourRéelle - e.DateEmprunt) AS DureeMoyenne
FROM Emprunter e
WHERE e.DateRetourRéelle IS NOT NULL;

-- 查询每个类型的书籍数量
SELECT
    g.Nom AS Genre,
    COUNT(l.ISBN) AS NbLivres
FROM Genre g
         LEFT JOIN Livre l ON g.GenreID = l.GenreID
GROUP BY g.Nom
ORDER BY NbLivres DESC;

-- 查询预约数量最多的书籍
SELECT
    l.Titre,
    COUNT(c.CommandeID) AS NbCommandes
FROM Livre l
         JOIN Commander c ON l.ISBN = c.ISBN
GROUP BY l.Titre
ORDER BY NbCommandes DESC
LIMIT 5;

-- 查询所有状态为“honorée”的预约详情
SELECT
    c.CommandeID,
    a.Nom AS Adherent,
    l.Titre,
    c.DateDébut,
    c.DuréePrévue
FROM Commander c
         JOIN Adherent a ON c.AdherentID = a.ID
         JOIN Livre l ON c.ISBN = l.ISBN
WHERE c.Statut = 'honorée';

