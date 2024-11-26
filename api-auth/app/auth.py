import bdd as db
import models as m
import schemas as s
from fastapi import HTTPException

def challenge_auth(user: s.UserLogin) -> m.Utilisateur:
    """
    Vérifie les informations d'identification d'un utilisateur en interrogeant la base de données.

    Arguments :
        user : objet de type UserLogin qui contient l'adresse e-mail et le mot de passe de l'utilisateur à vérifier.

    Retour :
        user_challenge : objet de type Utilisateur qui correspond à l'utilisateur identifié.

    Raises:
        HTTPException: En cas d'erreur lors de l'accès à la base de données ou si l'utilisateur n'est pas trouvé.

"""
    session = db.get_db_session()
    try:
        user_challenge = session.query(m.Utilisateur).filter(
            m.Utilisateur.EmailUtilisateur == user.EmailUtilisateur, 
            m.Utilisateur.MotdepasseUtilisateur == user.MotdepasseUtilisateur
        ).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de l'accès à la base de données")
    
    if not user_challenge:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    return user_challenge

