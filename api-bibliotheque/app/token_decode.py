import json
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends

with open('config.json') as f:
    config = json.load(f)

SECRET = config['SECRET_API-TOKEN']
ALGORITHMS = config['ALGORITHMS']

security = HTTPBearer()

def verifierTokenAcess(credits: HTTPAuthorizationCredentials = Depends(security)):
    """
    Vérifie si un jeton d'accès est valide en utilisant le schéma d'authentification HTTP 'Authorization: Bearer {jeton}'.

    Arguments:
    - credits: objet de type HTTPAuthorizationCredentials qui contient le jeton d'accès à vérifier (dépendance de FastAPI).

    Retour:
    - payload: objet décrypté du jeton d'accès, contenant les informations sur l'utilisateur associé au jeton.
    
    Raises:
        HTTPException: En cas d'erreur de vérification du jeton (expiration, erreur de décodage, etc.).

    """
    token = credits.credentials
    audiences: list = ["http://front-bibliotheque:5000", "http://api-bibliotheque:5000"]
    
    try:
        payload = jwt.decode(token, SECRET, ALGORITHMS, audience=audiences)
        if payload is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Signature Error: {str(e)}")
    except jwt.InvalidAlgorithmError as e:
        raise HTTPException(status_code=401, detail=f"Not HS256: {str(e)}")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalide token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erreur inconnue: {str(e)}")

    return payload