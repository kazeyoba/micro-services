import sqlite3

def get_db_connection() -> sqlite3.Connection:
    """Permet de récupérer une connexion sur la BDD.

    Returns:
        sqlite3.Connection: L'objet connection SQLite3
    """
    conn = sqlite3.connect("/data/bibliotheque.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_utilisateurs() -> list:
    """Renvoie la liste complète des utilisateurs.

    Returns:
        list: Les données sur la table `utilisateurs`.
    """
    conn = get_db_connection()
    utilisateurs = conn.execute("SELECT * FROM utilisateurs").fetchall()
    conn.close()
    
    data: list = [dict(u) for u in utilisateurs]
    
    return data

def get_livres() -> list:
    """Renvoie la liste complète des livres.

    Returns:
        list: Les données de la table `livres`.
    """
    conn = get_db_connection()
    livres = conn.execute("SELECT * FROM livres").fetchall()
    conn.close()
    
    data: list = [dict(l) for l in livres]
    
    return data

def get_auteurs() -> list:
    """Renvoie la liste complète des auteurs.

    Returns:
        list: Les données de la table `auteurs`.
    """
    conn = get_db_connection()
    auteurs = conn.execute("SELECT * FROM auteurs").fetchall()
    conn.close()
    
    data: list = [dict(a) for a in auteurs]
    
    return data

def get_utilisateur(utilisateur: str) -> dict:
    """Récupère les informations d'un utilisateurs (str ou int)

    Args:
        utilisateur (str): Nom ou id.

    Returns:
        dict: Données de l'utilisateurs.
    """
    conn = get_db_connection()
    try:
        utilisateur_id = int(utilisateur)
        user = conn.execute("SELECT * FROM utilisateurs WHERE id = ?", (utilisateur_id,)).fetchone()
    except ValueError:
        rows = conn.execute("SELECT * FROM utilisateurs WHERE nom_utilisateur = ?", (utilisateur,)).fetchall()
        if len(rows) == 1:
            user = rows[0]
        elif len(rows) > 1:
            conn.close()
            return {"error": "Plusieurs utilisateurs avec ce nom existent"}
        else:
            user = None
    conn.close()
    if not user:
        return {"error": "Utilisateur non trouvé"}
    return dict(user)

def get_emprunts(utilisateur_id):
    """
    Retourne la liste des emprunts pour un utilisateur donné.

    Args:
        utilisateur_id (int): L'ID de l'utilisateur.

    Returns:
        list: Une liste de dictionnaires contenant les informations des livres empruntés.
    """
    query = """
    SELECT livres.id, livres.titre, livres.pitch, livres.date_public, auteurs.nom_auteur
    FROM livres
    JOIN auteurs ON livres.auteur_id = auteurs.id
    WHERE livres.emprunteur_id = ?
    """
    conn = get_db_connection()
    emprunts = conn.execute(query, (str(utilisateur_id),)).fetchall()

    # Transformation des résultats en une liste de dictionnaires
    resultats = [
        {
            "id": livre[0],
            "titre": livre[1],
            "pitch": livre[2],
            "date_publication": livre[3],
            "auteur": livre[4]
        }
        for livre in emprunts
    ]
    return resultats


def get_livres_siecle(numero: int) -> list:
    """Recupere la liste des livres en fonction du siècle

    Args:
        numero (int): Numéro du siècle
    Returns:
        list: Les données en BDD.
    """    
    try:
        siecle = int(numero)
        start_year = (siecle - 1) * 100 + 1
        end_year = siecle * 100
    except ValueError:
        return {"error": "Siècle invalide"}
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT * FROM livres WHERE strftime('%Y', date_public) BETWEEN ? AND ?
    """, (start_year, end_year)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def ajouter_livre(livre: dict) -> dict:
    """Ajoute une entrée dans la table `livre`

    Args:
        livre (dict): La nouvelle entrée.

    Returns:
        dict: L'élément créer
    """    
    data = dict(livre)
    conn = get_db_connection()
    auteur = conn.execute("SELECT id FROM auteurs WHERE nom_auteur = ?", (data["nom_auteur"],)).fetchone()
    if not auteur:
        conn.execute("INSERT INTO auteurs (nom_auteur) VALUES (?)", (data["nom_auteur"],))
        auteur_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    else:
        auteur_id = auteur["id"]

    try:
        conn.execute("""
            INSERT INTO livres (titre, pitch, auteur_id, date_public)
            VALUES (?, ?, ?, ?)
        """, (data["titre"], data["pitch"], auteur_id, data["date_public"]))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return {"error": "Livre déjà existant"}
    conn.close()
    return {"message": "Livre ajouté avec succès"}

def ajouter_utilisateur(utilisateur: dict) -> dict:
    """Ajoute un utilisateur dans la table `utilisateurs`

    Args:
        utilisateur (dict): Utilisateur à ajouter

    Returns:
        dict: La reponse_
    """        
    data = dict(utilisateur)
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO utilisateurs (nom_utilisateur) VALUES (?)", (data["nom_utilisateur"],))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return {"error": "Utilisateur déjà existant"}
    conn.close()
    return {"message": "Utilisateur ajouté avec succès"}

def ajouter_auteur(auteur: dict) -> dict:
    """Ajoute un utilisateur dans la table `utilisateurs`

    Args:
        utilisateur (dict): Utilisateur à ajouter

    Returns:
        dict: La reponse_
    """        
    data = dict(auteur)
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO auteurs (nom_auteur) VALUES (?)", (data["nom_auteur"],))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return {"error": "Auteur déjà existant"}
    conn.close()
    return {"message": "Auteur ajouté avec succès"}

def supprimer_utilisateur(utilisateur: str) -> dict:
    """Supprime un utilisateur de la BDD.

    Args:
        utilisateur (str): ID ou nom de l'utilisateur.

    Returns:
        dict: Réponse de la requête.
    """    
    conn = get_db_connection()
    try:
        utilisateur_id = int(utilisateur)
        conn.execute("DELETE FROM utilisateurs WHERE id = ?", (utilisateur_id,))
    except ValueError:
        conn.execute("DELETE FROM utilisateurs WHERE nom_utilisateur = ?", (utilisateur,))
    conn.commit()
    conn.close()
    return {"message": "Utilisateur supprimé avec succès"}

def emprunter_livre(utilisateur_id: int, livre_id: int) -> dict:
    """Crée un emprunt

    Args:
        utilisateur_id (int): Identifiant de l'utilisateur
        livre_id (int): Identifiant du livre

    Returns:
        dict: Réponse de la requête
    """    
    conn = get_db_connection()
    conn.execute("""
        UPDATE livres SET emprunteur_id = ?
        WHERE id = ? AND emprunteur_id IS NULL
    """, (utilisateur_id, livre_id))
    conn.commit()
    conn.close()
    return {"message": "Livre emprunté avec succès"}

def rendre_livre(utilisateur_id: int, livre_id: int) -> dict:
    """Supprime l'emprunt

    Args:
        utilisateur_id (int): Identifiant de l'utilisateur
        livre_id (int): Identifiant du livre

    Returns:
        dict: Réponse de la requête.
    """    
    conn = get_db_connection()
    conn.execute("""
        UPDATE livres SET emprunteur_id = NULL
        WHERE id = ? AND emprunteur_id = ?
    """, (livre_id, utilisateur_id))
    conn.commit()
    conn.close()
    return {"message": "Livre rendu avec succès"}
