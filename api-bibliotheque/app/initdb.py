import sqlite3
import json
import random
from datetime import datetime

conn = sqlite3.connect("bibliotheque.db")
cursor = conn.cursor()

def creer_tables():
    """Initialise le schéma de BDD"""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auteurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_auteur TEXT UNIQUE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT UNIQUE,
        pitch TEXT,
        auteur_id INTEGER,
        date_public DATE,
        emprunteur_id INTEGER,
        FOREIGN KEY(auteur_id) REFERENCES auteurs(id),
        FOREIGN KEY(emprunteur_id) REFERENCES utilisateurs(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_utilisateur TEXT UNIQUE
    )
    """)
    conn.commit()

def charger_donnees(fichier_json: str):
    """Charge les données depuis un JSON"""
    with open(fichier_json, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    log = []

    for livre in data:
        auteur_nom = livre["author"]
        cursor.execute("SELECT id FROM auteurs WHERE nom_auteur = ?", (auteur_nom,))
        auteur = cursor.fetchone()

        if auteur:
            auteur_id = auteur[0]
            log.append(f"auteur {auteur_nom} déjà existant")
        else:
            cursor.execute("INSERT INTO auteurs (nom_auteur) VALUES (?)", (auteur_nom,))
            auteur_id = cursor.lastrowid
            log.append(f"nouvel auteur {auteur_nom} ajouté id = {auteur_id}")

        try:
            date_public = datetime.strptime(livre["date"], "%d/%m/%Y").date()
        except ValueError:
            log.append(f"Date invalide pour le livre {livre['title']}: {livre['date']}")
            date_public = None

        try:
            cursor.execute("""
            INSERT INTO livres (titre, pitch, auteur_id, date_public)
            VALUES (?, ?, ?, ?)
            """, (livre["title"], livre["content"], auteur_id, date_public))
            log.append(f"nouveau livre {livre['title']} ajouté")
        except sqlite3.IntegrityError:
            log.append(f"livre {livre['title']} déjà existant")

    conn.commit()

    with open("log.txt", "w", encoding="utf-8") as logfile:
        logfile.write("\n".join(log))

def generer_emprunts():
    """Génère les emprunts"""
    utilisateurs = ["DarkVador", "R2D2", "RogueOne", "BobaFeth"]
    for utilisateur in utilisateurs:
        cursor.execute("INSERT OR IGNORE INTO utilisateurs (nom_utilisateur) VALUES (?)", (utilisateur,))
    
    cursor.execute("SELECT id, nom_utilisateur FROM utilisateurs")
    liste_utilisateurs = cursor.fetchall()

    cursor.execute("SELECT id, titre FROM livres")
    liste_livres = cursor.fetchall()

    log = []

    for utilisateur_id, utilisateur_nom in liste_utilisateurs:
        livres_empruntes = random.sample(liste_livres, k=random.randint(1, 4))
        for livre_id, titre in livres_empruntes:
            cursor.execute("""
            UPDATE livres
            SET emprunteur_id = ?
            WHERE id = ?
            """, (utilisateur_id, livre_id))
            log.append(f"livre {titre} emprunté par {utilisateur_nom}")
    
    conn.commit()

    with open("log.txt", "a", encoding="utf-8") as logfile:
        logfile.write("\n" + "\n".join(log))

if __name__ == "__main__":
    creer_tables()

    fichier_json = "data_books.json"
    charger_donnees(fichier_json)

    generer_emprunts()

    print("Données insérées et emprunts générés. Vérifiez le fichier log.txt.")
