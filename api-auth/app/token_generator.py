import models as m
import jwt
import json
from datetime import datetime, timedelta, timezone

CONFIG_PATH: str = "./token_config.json"
def token_generator(user: m.Utilisateur, config_path: str = CONFIG_PATH) -> bytes:
    """
    Génère un jeton d'accès JWT pour un utilisateur.

    Arguments :
        user : objet de type Utilisateur qui représente l'utilisateur pour lequel générer le jeton d'accès.
            config_path : chaîne de caractères qui indique le chemin d'accès au fichier de configuration contenant les paramètres de génération de jeton.

    Retour :
        access_token : objet de type bytes qui représente le jeton d'accès JWT généré.
    """
    with open(config_path) as f:
        config = json.load(f)
    
    payload = {
        "iss": config['iss'],
        "aud": "http://api-bibliotheque:5000",
        "iat": datetime.now() - timedelta(hours=1),
        "exp": datetime.now() + timedelta(minutes=config['ACCESS_TOKEN_EXPIRE_MINUTES']) - timedelta(hours=1),
        "sub": user.EmailUtilisateur,
        "nom": user.NomUtilisateur,
        "role": user.Statut
    }

    access_token = jwt.encode(payload, config['SECRET_KEY'], algorithm=config['ALGORITHMS'])
    
    return access_token